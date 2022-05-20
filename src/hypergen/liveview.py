d = dict

from hypergen.hypergen import *
from hypergen.context import context as c
from hypergen.template import *

import datetime, json
from contextlib import contextmanager

from django.http.response import HttpResponse, HttpResponseRedirect
from django.utils.dateparse import parse_date, parse_datetime, parse_time
from django.conf import settings
from django.templatetags.static import static

__all__ = ["command", "call_js", "callback", "THIS", "is_ajax", "LiveviewPlugin"]

### liveview is a plugin to hypergen ###

class LiveviewPlugin:
    @contextmanager
    def context(self):
        with c(at="hypergen", event_handler_callbacks={}, event_handler_callback_strs=[], commands=[]):
            command("hypergen.setClientState", 'hypergen.eventHandlerCallbacks', c.hypergen.event_handler_callbacks)

    def element_children_prepend(self, element, children):
        if type(element) is head:
            return (
                script(src=static("hypergen/hypergen.min.js")),
                raw("<script type='application/json' id='hypergen-apply-commands-data'>{}</script>".format(
                dumps(c.hypergen.commands))),
                # script(dumps(c.hypergen.commands), type_='application/json', id_='hypergen-apply-commands-data'),
                script("""
                    ready(() =>
                        window.applyCommands(JSON.parse(
                            document.getElementById('hypergen-apply-commands-data').textContent, reviver)))
                """),
            )

        return tuple()

### constants ###

class THIS(object):
    pass

def is_ajax(request=None):
    if request is None:
        request = c.request

    return request.META.get('HTTP_X_REQUESTED_WITH', None) == 'XMLHttpRequest'

TARGET_ID_ERR = """
No "target_id" set! It sets where the content of a callback will be rendered to.
"target_id" must be set by either:

- Prefered! setting it as an attribute on the base_template:
    def my_base_template():
        with div(class_="so-base", id_="base"):
            yield

    my_base_template.target_id = "base"


- setting it as a keyword argument to the @hypergen_view and/or @hypergen_callback decorators:
    @hypergen_callback(target_id="base")
    def my_callback(request):
        ....

  The reason it can be set on @hypergen_view's as well is to make partial loading work. Views with the same
  base_template and target_id's supports partial loading between them.

- setting it manually on context.hypergen["target_id"]:
    @hypergen_callback(target_id=OMIT)
    def my_callback(request):
        with context(target_id="base", at="hypergen"):
            ...
""".strip()

def hypergen_response(html_or_commands_or_http_response, status=None):
    value = html_or_commands_or_http_response
    if isinstance(value, HttpResponseRedirect):
        if is_ajax():
            return HttpResponse(dumps([["hypergen.redirect", value["Location"]]]), status=status,
                content_type='application/json')
        else:
            return value
    elif isinstance(value, HttpResponse):
        assert status is None
        assert not is_ajax()
        return value
    elif type(value) in (list, tuple):
        assert is_ajax()
        return HttpResponse(dumps(value), status=status, content_type='application/json')
    elif type(value) in (str, str):
        assert not is_ajax()
        return HttpResponse(value, status=status)
    else:
        raise Exception("Invalid response value: {}".format(repr(value)))

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

### Actions happening on the frontend  ###

def callback(url_or_view, *cb_args, **kwargs):
    debounce = kwargs.pop("debounce", 0)
    confirm_ = kwargs.pop("confirm", False)
    blocks = kwargs.pop("blocks", False)
    upload_files = kwargs.pop("upload_files", False)
    event_matches = kwargs.pop("event_matches", False)
    clear = kwargs.pop("clear", False)
    meta = kwargs.pop("meta", {})
    assert not kwargs, "Invalid callback kwarg(s): {}".format(repr(kwargs))

    if callable(url_or_view):
        assert hasattr(url_or_view, "reverse") and callable(
            url_or_view.reverse), "Must have a reverse() attribute {}".format(url_or_view)
        url = url_or_view.reverse()
    else:
        url = url_or_view

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

    to_html.hypergen_callback_signature = "callback", (url_or_view,) + cb_args, kwargs

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

# Serialization
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

class StringWithMeta(object):
    def __init__(self, value, meta):
        self.value = value
        self.meta = meta

    def __str__(self):
        return force_text(self.value)

    def __unicode__(self):
        return force_text(self.value)

    def __iter__(self):
        return iter(self.value)

    def __add__(self, other):
        return self.value + other

    def __iadd__(self, other):
        return self.value + other
