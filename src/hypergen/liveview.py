d = dict
from django.urls.base import reverse
from hypergen.hypergen import *
from hypergen.hypergen import wrap2, make_string, t, check_perms, autourl_register
from hypergen.context import context as c
from hypergen.template import *

import datetime, json
from contextlib import contextmanager, ExitStack
from functools import wraps

from django.http.response import HttpResponse, HttpResponseRedirect
from django.utils.dateparse import parse_date, parse_datetime, parse_time
from django.conf import settings
from django.templatetags.static import static

__all__ = [
    "command", "call_js", "callback", "THIS", "LiveviewPlugin", "dumps", "loads", "CallbackPlugin", "view",
    "callback_view", "NO_PERM_REQUIRED"]

### constants ###

class THIS(object):
    pass

NO_PERM_REQUIRED = "__NO_PERM_REQUIRED__"

COERCE = {str: "hypergen.coerce.str", int: "hypergen.coerce.int", float: "hypergen.coerce.float"}

JS_VALUE_FUNCS = d(
    checkbox="hypergen.read.checked",
    radio="hypergen.read.radio",
    file="hypergen.read.file",
)

JS_COERCE_FUNCS = dict(
    month="hypergen.coerce.month",
    number="hypergen.coerce.int",
    range="hypergen.coerce.float",
    week="hypergen.coerce.week",
    date="hypergen.coerce.date",
    time="hypergen.coerce.time",
)

JS_COERCE_FUNCS["datetime-local"] = "hypergen.coerce.datetime"

### liveview is a plugin to hypergen ###

class LiveviewPluginBase:
    @contextmanager
    def context(self):
        with c(at="hypergen", event_handler_callbacks={}, event_handler_callback_strs=[], commands=[]):
            yield

    @contextmanager
    def wrap_element_init(self, element, childrem, attrs):
        # Default js_value_func and js_coerce_funcs values.
        element.js_value_func = attrs.pop("js_value_func", "hypergen.read.value")
        coerce_to = attrs.pop("coerce_to", None)
        if coerce_to is not None:
            try:
                element.js_coerce_func = COERCE[coerce_to]
            except KeyError:
                raise Exception("coerce must be one of: {}".format(list(COERCE.keys())))
        else:
            element.js_coerce_func = attrs.pop("js_coerce_func", None)

        # Content of base_element.__init__ method runs here
        yield

        # Some elements have special liveview features.
        if isinstance(element, input_):
            # Coerce and value func based on input type.
            element.js_value_func = attrs.pop("js_value_func",
                JS_VALUE_FUNCS.get(attrs.get("type_", "text"), "hypergen.read.value"))
            if element.js_coerce_func is None:
                element.js_coerce_func = attrs.pop("js_coerce_func",
                    JS_COERCE_FUNCS.get(attrs.get("type_", "text"), None))
        elif isinstance(element, a):
            # Partial loading
            # TODO: Do partial loading without StringWithMeta which is a bit sucky.
            # href = attrs.get("href")
            # base_template1 = href.meta.get("base_template", None)
            # if base_template1 is not None:
            #     base_template2 = getattr(c, "base_template", None)
            #     if base_template1 == base_template2:
            #         # Partial loading is possible.
            #         attrs["onclick"] = "hypergen.callback('{}', [], {{'event': event}})".format(href)
            pass

class LiveviewPlugin(LiveviewPluginBase):
    def process_html(self, html):
        def template():
            raw("<!--hypergen_liveview_media-->")
            if "hypergen/hypergen.min." not in html:
                script(src=static("hypergen/hypergen.min.js"))

            script(dumps(c.hypergen.commands), type_='application/json', id_='hypergen-apply-commands-data')
            script("""
                ready(() => window.applyCommands(JSON.parse(document.getElementById(
                    'hypergen-apply-commands-data').textContent, reviver)))
            """)
            raw("</body>")  # We are replacing existing </body>

        assert "</body>" in html, "liveview needs a body() tag to work, but got: " + html

        command("hypergen.setClientState", 'hypergen.eventHandlerCallbacks', c.hypergen.event_handler_callbacks)

        return html.replace("</body>", hypergen(template))

class CallbackPlugin(LiveviewPluginBase):
    def __init__(self, /, *, target_id=None):
        self.target_id = target_id

    def process_html(self, html):
        command("hypergen.setClientState", 'hypergen.eventHandlerCallbacks', c.hypergen.event_handler_callbacks)
        if self.target_id:
            command("hypergen.morph", self.target_id, html)

        return html

### Commands happening on the frontend  ###

def command(javascript_func_path, *args, **kwargs):
    prepend = kwargs.pop("prepend", False)
    return_ = kwargs.pop("return_", False)
    item = [javascript_func_path] + list(args)
    if return_:
        return item
    elif prepend:
        c.hypergen.commands.insert(0, item)
    else:
        c.hypergen.commands.append(item)

def callback(url, *cb_args, **kwargs):
    debounce = kwargs.pop("debounce", 0)
    confirm_ = kwargs.pop("confirm", False)
    blocks = kwargs.pop("blocks", False)
    upload_files = kwargs.pop("upload_files", False)
    event_matches = kwargs.pop("event_matches", False)
    clear = kwargs.pop("clear", False)
    meta = kwargs.pop("meta", {})
    assert not kwargs, "Invalid callback kwarg(s): {}".format(repr(kwargs))

    def to_html(element, k, v):
        def fix_this(x):
            return element if x is THIS else x

        element.ensure_id()
        cmd = command(
            "hypergen.callback", url, [fix_this(x) for x in cb_args],
            d(debounce=debounce, confirm_=confirm_, blocks=blocks, uploadFiles=upload_files, clear=clear,
            elementId=element.attrs["id_"].v, debug=settings.DEBUG, meta=meta), return_=True)
        cmd_id = "{}__{}".format(element.attrs["id_"].v, k)

        c.hypergen.event_handler_callbacks[cmd_id] = cmd

        if event_matches:
            em = ", {}".format(escape(dumps(event_matches)))
        else:
            em = ""
        return [" ", t(k), '="', "e(event,'{}'{})".format(cmd_id, em), '"']

    to_html.hypergen_callback_signature = "callback", (url,) + cb_args, kwargs

    return to_html

def call_js(command_path, *cb_args):
    def to_html(element, k, v):
        def fix_this(x):
            return element if x is THIS else x

        element.ensure_id()
        cmd = command(command_path, *[fix_this(x) for x in cb_args], return_=True)
        cmd_id = "{}__{}".format(element.attrs["id_"].v, k)
        c.hypergen.event_handler_callbacks[cmd_id] = cmd

        return [" ", t(k), '="', "e(event, '{}')".format(cmd_id), '"']

    return to_html

### Decorators for better QOL ###

@wrap2
def view(func, /, *, path=None, re_path=None, base_template=None, perm=None, any_perm=False, login_url=None,
    raise_exception=False, redirect_field_name=None, autourl=True):
    if perm != NO_PERM_REQUIRED:
        assert perm, "perm= is a required keyword argument"

    @wraps(func)
    def _(request, *args, **kwargs):
        # Ensure correct permissions
        ok, response_redirect, matched_perms = check_perms(request, perm, login_url=login_url,
            raise_exception=raise_exception, any_perm=any_perm, redirect_field_name=redirect_field_name)
        if ok is not True:
            return response_redirect

        with c(at="hypergen", matched_perms=matched_perms):
            html = hypergen(func, request, *args, **kwargs, hypergen=d(liveview=True, base_template=base_template))
            return HttpResponse(html)

    if autourl:
        assert not all((path, re_path)), "Only one of path= or re_path= must be set when autourl=True"
        autourl_register(_, base_template=base_template, path=path, re_path=re_path)

    return _

def callback_view():
    pass

### Serialization ###

ENCODINGS = {
    datetime.date: lambda o: {"_": ["date", str(o)]},
    datetime.datetime: lambda o: {"_": ["datetime", str(o)]},
    tuple: lambda o: {"_": ["tuple", list(o)]},
    set: lambda o: {"_": ["set", list(o)]},
    frozenset: lambda o: {"_": ["frozenset", list(o)]},
    range: lambda o: {"_": ["range", [o.start, o.stop, o.step]]},}

def encoder(o):
    assert not hasattr(o, "reverse"), "Should not happen"
    if issubclass(type(o), base_element):
        assert o.attrs.get("id_", False), "Missing id_"
        return ["_", "element_value", [o.js_value_func, o.js_coerce_func, o.attrs["id_"].v]]
    elif hasattr(o, "__weakref__"):
        # Lazy strings and urls.
        # TODO: still needed?
        return make_string(o)
    fn = ENCODINGS.get(type(o), None)
    if fn:
        return fn(o)
    else:
        raise TypeError(repr(o) + " is not JSON serializable")

DECODINGS = {
    "float": float,
    "date": parse_date,
    "datetime": parse_datetime,
    "time": parse_time,
    "tuple": tuple,
    "set": set,
    "frozenset": frozenset,
    "range": lambda v: range(*v),}

def decoder(o):
    _ = o.get("_", None)
    if _ is None or type(_) is not list or len(_) != 2:
        return o

    datatype, value = _
    fn = DECODINGS.get(datatype, None)
    if fn:
        return fn(value)
    else:

        raise Exception("Unknown datatype, {}".format(datatype))

def dumps(data, default=encoder, indent=None):
    result = json.dumps(data, default=default, separators=(',', ':'), indent=indent)

    return result

def loads(data):
    return json.loads(data, object_hook=decoder)
