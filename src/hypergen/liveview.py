d = dict
from django.urls.base import resolve
from hypergen.hypergen import *
from hypergen.hypergen import wrap2, make_string, t, check_perms, autourl_register
from hypergen.context import context as c
from hypergen.hypergen import metastr
from hypergen.template import *

import datetime, json
from contextlib import contextmanager
from functools import wraps

from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.utils.dateparse import parse_date, parse_datetime, parse_time
from django.conf import settings
from django.templatetags.static import static

__all__ = [
    "command", "call_js", "callback", "THIS", "LiveviewPlugin", "dumps", "loads", "ActionPlugin", "liveview",
    "action", "NO_PERM_REQUIRED"]

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
    def wrap_element_init(self, element, children, attrs):
        # Default js_value_func and js_coerce_funcs values.
        if attrs.get("contenteditable", False) is True:
            element.js_value_func = attrs.pop("js_value_func", "hypergen.read.contenteditable")
        else:
            element.js_value_func = attrs.pop("js_value_func", "hypergen.read.value")

        coerce_to = attrs.pop("coerce_to", None)
        if coerce_to is not None:
            try:
                element.js_coerce_func = COERCE[coerce_to]
            except KeyError:
                raise Exception("coerce must be one of: {}".format(list(COERCE.keys())))
        else:
            element.js_coerce_func = attrs.pop("js_coerce_func", None)

        # Some elements have special liveview features.
        if isinstance(element, input_):
            # Coerce and value func based on input type.
            element.js_value_func = attrs.pop("js_value_func",
                JS_VALUE_FUNCS.get(attrs.get("type_", "text"), "hypergen.read.value"))
            if element.js_coerce_func is None:
                element.js_coerce_func = attrs.pop("js_coerce_func",
                    JS_COERCE_FUNCS.get(attrs.get("type_", "text"), None))
        elif isinstance(element, a):
            # Partial loading.
            href = attrs.get("href", None)
            if type(href) is metastr:
                base_template1 = href.meta.get("base_template", None)
                if base_template1 is not None:
                    if base_template1 is c.hypergen.get("partial_base_template", None):
                        attrs["onclick"] = "hypergen.partialLoad(event, '{}', true)".format(href)

        # Content of base_element.__init__ method runs here
        yield

class LiveviewPlugin(LiveviewPluginBase):
    @contextmanager
    def context(self):
        with c(at="hypergen", event_handler_callbacks={}, event_handler_callback_strs=[], commands=[]):
            yield

    def process_html(self, html):
        def template():
            raw("<!--hypergen_liveview_media-->")
            script(src=static("hypergen/v2/hypergen.min.js"))
            script(dumps(c.hypergen.commands), type_='application/json', id_='hypergen-apply-commands-data')
            script("""
                hypergen.ready(() => hypergen.applyCommands(JSON.parse(document.getElementById(
                    'hypergen-apply-commands-data').textContent, hypergen.reviver)))
            """)
            raw("</body>")  # We are replacing existing </body>

        assert "</body>" in html, "liveview needs a body() tag to work, but got: " + html
        assert html.count("</body>") == 1, "Ooops, multiple </body> tags found. There can be only one!"
        command("hypergen.setClientState", 'hypergen.eventHandlerCallbacks', c.hypergen.event_handler_callbacks)

        # Partial loading.
        path = c.request.get_full_path()
        command("history.replaceState", d(callback_url=path), "", path)

        return html.replace("</body>", hypergen(template))

class ActionPlugin(LiveviewPluginBase):
    def __init__(self, /, *, target_id=None, base_view=None):
        self.target_id = target_id
        self.base_view = base_view

    @contextmanager
    def context(self):
        with c(at="hypergen", event_handler_callbacks={}, event_handler_callback_strs=[], commands=[],
            target_id=self.target_id):
            yield

    def process_html(self, html):
        command("hypergen.setClientState", 'hypergen.eventHandlerCallbacks', c.hypergen.event_handler_callbacks)
        target_id = c.hypergen.get("target_id", None)
        if target_id:
            command("hypergen.morph", target_id, html)

        return html

    def func_after(self):
        if self.base_view:
            referer_resolver_match = resolve(c.request.META["HTTP_X_PATHNAME"])
            # TODO: Check for HttpResponseredirect here?
            self.base_view.original_func(c.request, *referer_resolver_match.args, **referer_resolver_match.kwargs)

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

def callback(url, *cb_args, debounce=0, confirm_=False, blocks=False, upload_files=False, clear=False, headers=None,
    meta=None, when=None):
    if meta is None:
        meta = {}
    if headers is None:
        headers = {}

    if getattr(url, "is_hypergen_action", False) is True:
        url = url.reverse()

    def to_html(element, k, v):
        def fix_this(x):
            return element if x is THIS else x

        element.ensure_id()
        cmd = command(
            "hypergen.callback", url, [fix_this(x) for x in cb_args],
            d(debounce=debounce, confirm_=confirm_, blocks=blocks, uploadFiles=upload_files, clear=clear,
            elementId=element.attrs["id_"], debug=settings.DEBUG, meta=meta, headers=headers), return_=True)
        cmd_id = "{}__{}".format(element.attrs["id_"], k)

        c.hypergen.event_handler_callbacks[cmd_id] = cmd

        when_str = ", " + dumps(when).replace('"', "'") if when else ""
        return [" ", t(k), '="', "hypergen.event(event, '{}'{})".format(cmd_id, when_str), '"']

    signature = {
        k: v for k, v in d(debounce=debounce, confirm_=confirm_, blocks=blocks, upload_files=upload_files,
        clear=clear, meta=meta, when=when).items() if v}
    to_html.hypergen_callback_signature = "callback", (url,) + cb_args, signature

    return to_html

def call_js(command_path, *cb_args):
    def to_html(element, k, v):
        def fix_this(x):
            return element if x is THIS else x

        element.ensure_id()
        cmd = command(command_path, *[fix_this(x) for x in cb_args], return_=True)
        cmd_id = "{}__{}".format(element.attrs["id_"], k)
        c.hypergen.event_handler_callbacks[cmd_id] = cmd

        return [" ", t(k), '="', "hypergen.event(event, '{}')".format(cmd_id), '"']

    return to_html

### Decorators for better QOL ###

@wrap2
def liveview(func, /, *, path=None, re_path=None, base_template=None, perm=None, any_perm=False, login_url=None,
    raise_exception=False, redirect_field_name=None, autourl=True, partial=True, target_id=None, appstate=None):
    if perm != NO_PERM_REQUIRED:
        assert perm, "perm is a required keyword argument"
    if target_id is None:
        target_id = getattr(base_template, "target_id", None)
    if base_template and partial and not target_id:
        raise Exception("{}: Partial loading requires a target_id. Either as a kwarg or"
            " an attribute on the base_template function.".format(func))
    partial_base_template = base_template if partial else None

    original_func = func

    @wraps(func)
    def _(request, *args, **kwargs):
        # Ensure correct permissions
        ok, response_redirect, matched_perms = check_perms(request, perm, login_url=login_url,
            raise_exception=raise_exception, any_perm=any_perm, redirect_field_name=redirect_field_name)
        if ok is not True:
            return response_redirect

        if partial and request.META.get("HTTP_X_HYPERGEN_PARTIAL", None) == "1":
            with c(at="hypergen", matched_perms=matched_perms, partial_base_template=partial_base_template):
                commands = hypergen(
                    func, request, *args, **kwargs, settings=d(action=True, returns=COMMANDS, target_id=target_id,
                    appstate=appstate, namespace=_.reverse.hypergen_namespace))

                return HttpResponse(dumps(commands), status=200, content_type='application/json')
        else:
            with c(at="hypergen", matched_perms=matched_perms, partial_base_template=partial_base_template):
                html = hypergen(
                    func, request, *args, **kwargs, settings=d(liveview=True, base_template=base_template,
                    appstate=appstate, namespace=_.reverse.hypergen_namespace))
                return HttpResponse(html)

    if autourl:
        assert not all((path, re_path)), "Only one of path and re_path must be set when autourl=True"
        autourl_register(_, base_template=base_template, path=path, re_path=re_path)

    _.original_func = original_func

    return _

@wrap2
def action(func, /, *, path=None, re_path=None, base_template=None, target_id=None, perm=None, any_perm=False,
    autourl=True, partial=True, base_view=None, appstate=None):
    if perm != NO_PERM_REQUIRED:
        assert perm, "perm is a required keyword argument"
    if target_id is None:
        target_id = getattr(base_template, "target_id", None)
    if base_template and partial and not target_id:
        raise Exception("{}: Partial loading requires a target_id. Either as a kwarg or"
            " an attribute on the base_template function.".format(func))
    partial_base_template = base_template if partial else None

    @wraps(func)
    def _(request, *args, **kwargs):
        # Ensure correct permissions
        ok, __, matched_perms = check_perms(request, perm, any_perm=any_perm)
        if ok is not True:
            return HttpResponseForbidden()

        action_args = loads(request.POST["hypergen_data"])["args"]

        with c(at="hypergen", matched_perms=matched_perms, partial_base_template=partial_base_template):
            full = hypergen(
                func, request, *action_args, **kwargs, settings=d(action=True, returns=FULL, target_id=target_id,
                appstate=appstate, namespace=_.reverse.hypergen_namespace, base_view=base_view))
            if isinstance(full["func_result"], HttpResponseRedirect):
                # Allow to return a redirect response directly from an action.
                return HttpResponse(dumps([["hypergen.redirect", full["func_result"]["Location"]]]), status=302,
                    content_type='application/json')
            elif isinstance(full["func_result"], HttpResponse):
                return full["func_result"]
            else:
                return HttpResponse(dumps(full["context"]["hypergen"]["commands"]), status=200,
                    content_type='application/json')

    if autourl:
        assert not all((path, re_path)), "Only one of path= or re_path= must be set when autourl=True"
        autourl_register(_, base_template=base_template, path=path, re_path=re_path)

    _.is_hypergen_action = True

    return _

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
        return ["_", "element_value", [o.js_value_func, o.js_coerce_func, o.attrs["id_"]]]
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
