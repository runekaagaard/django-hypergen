# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)

import string, sys
from threading import local
from contextlib import contextmanager
from collections import OrderedDict
from functools import wraps
from copy import deepcopy
from types import GeneratorType

from django.urls.base import reverse_lazy
from django.http.response import HttpResponse

import freedom
from freedom.utils import insert
from freedom.core import context

### Python 2+3 compatibility ###

if sys.version_info.major > 2:
    from html import escape
    letters = string.ascii_letters

    def items(x):
        return x.items()

else:
    from cgi import escape
    letters = string.letters
    str = unicode

    def items(x):
        return x.iteritems()


### Globals ###

state = local()
UPDATE = 1


### Control ###
def hypergen(func, *args, **kwargs):
    kwargs = deepcopy(kwargs)
    auto_id = kwargs.pop("auto_id", True)
    try:
        if "request" in context:  # TODO
            state.html = []
            state.liveview = True
            state.id_counter = base65_counter() if auto_id else None
            state.id_prefix = kwargs.pop(
                "id_prefix", (freedom.loads(context.request.body)["id_prefix"]
                              if context.request.is_ajax() else ""))
            state.auto_id = auto_id
            # Key/value store sent to the frontend.
            state.kv = {}
            state.target_id = kwargs.pop("target_id", "__main__")
            state.commands = []
            func(*args, **kwargs)
            html = "".join(
                str(x()) if callable(x) else str(x) for x in state.html)
            if state.kv:
                state.commands.append([
                    "./freedom", ["setEventHandlerCache"],
                    [state.target_id, state.kv]
                ])
            if not context.request.is_ajax():
                s = '<script>window.applyCommands({})</script>'.format(
                    freedom.dumps(state.commands))
                pos = html.find("</head")
                html = insert(html, s, pos)
                return HttpResponse(html)
            else:
                state.commands.append(
                    ["./freedom", ["morph"], [state.target_id, html]])
                return state.commands

    finally:
        state.html = []
        state.id_counter = None
        state.id_prefix = ""
        state.auto_id = False
        state.liveview = False
        state.kv = {}
        state.target_id = None
        state.commands = []

    return html


# hypergen(lambda: None)


class LiveviewHttpResponse(HttpResponse):
    def __init__(self, commands):
        pass


def liveview(request, func, *args, **kwargs):
    html = hypergen(
        func,
        *args,
        auto_id=True,
        id_prefix=freedom.loads(request.body)["id_prefix"]
        if request.is_ajax() else "",
        liveview=True,
        **kwargs)


class SkipException(Exception):
    pass


@contextmanager
def skippable():
    try:
        yield
    except SkipException:
        pass


### Building HTML, internal API ###


def _element_start_1(tag, attrs, into):
    attrs = _sort_attrs(attrs)
    raw(("<", tag), into=into)
    return attrs


def _element_start_2(k, v, into):
    k = t(k).rstrip("_").replace("_", "-")
    if type(v) is bool:
        if v is True:
            raw((" ", k), into=into)
    elif k == "style" and type(v) in (dict, OrderedDict):
        raw((" ", k, '="', ";".join(
            t(k1) + ":" + t(v1) for k1, v1 in items(v)), '"'),
            into=into)
    else:
        raw((" ", k, '="', t(v), '"'), into=into)


def _element_start_3(children, into, void, sep):
    if void:
        raw(("/"), into=into)
    raw(('>', ), into=into)
    write(*children, into=into, sep=sep)


def element_start(*args, **kwargs):
    return control_element_start(*args, **kwargs)


def element_end(tag, children, into=None, sep="", void=False):
    if void is False:
        write(*children, into=into, sep=sep)
        raw(("</", t(tag), ">"), into=into)


def element(tag, children, into=None, sep="", void=False, **attrs):
    element_start(tag, children, into=into, sep=sep, void=void, **attrs)
    element_end(tag, [], into=into, void=void)


def element_ret(tag, children, sep="", void=False, **attrs):
    into = Blob()
    element(tag, children, into=into, sep=sep, void=void, **attrs)
    return into


def element_con(tag, children, into=None, sep="", void=False, **attrs):
    element = element_start(
        tag, children, into=into, sep=sep, void=void, **attrs)
    yield element
    element_end(tag, [], into=into, void=void)


def element_dec(tag, children, into=None, sep="", void=False, **attrs):
    def _(f):
        @wraps(f)
        def __(*args, **kwargs):
            element_start(
                tag, children, into=into, sep=sep, void=void, **attrs)
            f(*args, **kwargs)
            element_end(tag, [], into=into, void=void)

        return __

    return _


### Building HTML, public API ###


def _write(_t, children, **kwargs):
    into = kwargs.get("into", None)
    if into is None:
        into = state.html
    sep = _t(kwargs.get("sep", ""))

    for x in children:
        if x is None:
            continue
        elif type(x) is Blob:
            into.extend(x)
        elif type(x) in (list, tuple, GeneratorType):
            _write(_t, list(x), into=into, sep=sep)
        elif callable(x):
            into.append(x)
        else:
            into.append(_t(x))
        if sep:
            into.append(sep)
    if sep and children:
        into.pop()


def write(*children, **kwargs):
    _write(t, children, **kwargs)


def raw(*children, **kwargs):
    _write(lambda x: x, children, **kwargs)


### Django helpers ###
def callback(func):
    func.hypergen_callback_url = reverse_lazy(
        "freedom:callback", args=[".".join((func.__module__, func.__name__))])

    func.hypergen_is_callback = True

    return func


### Misc ###


def _sort_attrs(attrs):
    # For testing only, subject to change.
    if attrs.pop("_sort_attrs", False):
        attrs = OrderedDict((k, attrs[k]) for k in sorted(attrs.keys()))
        if "style" in attrs and type(attrs["style"]) is dict:
            attrs["style"] = OrderedDict(
                (k, attrs["style"][k]) for k in sorted(attrs["style"].keys()))

    return attrs


def t(s, quote=True):
    return escape(str(s), quote=quote)


class Blob(object):
    def __init__(self, html=None, meta=None):
        self.html = html if html is not None else []
        self.meta = meta

    def append(self, x):
        return self.html.append(x)

    def extend(self, x):
        return self.html.extend(x)

    def pop(self, n=-1):
        return self.html.pop(n)

    def __getitem__(self, index):
        return self.html[index]


def base65_counter():
    # THX: https://stackoverflow.com/a/49710563/164449
    abc = letters + string.digits + "-_:"
    base = len(abc)
    i = -1
    while True:
        i += 1
        num = i
        output = abc[num % base]  # rightmost digit

        while num >= base:
            num //= base  # move to next digit to the left
            output = abc[num % base] + output  # this digit

        yield output


### Form elements and liveview ###
class THIS(object):
    pass


NON_SCALARS = set((list, dict, tuple))


def _callback(args, this, debounce=0):
    func = args[0]
    assert callable(func), ("First callback argument must be a callable, got "
                            "{}.".format(repr(func)))
    args = args[1:]

    args2 = []
    for arg in args:
        if type(arg) in NON_SCALARS:
            state.kv[id(arg)] = arg
            args2.append(
                freedom.quote("H.e['{}'][{}]".format(state.target_id, id(
                    arg))))
        else:
            args2.append(arg)

    return "H.cb({})".format(
        freedom.dumps(
            [func.hypergen_callback_url] + list(args2),
            unquote=True,
            escape=True,
            this=this))


def control_element_start(tag,
                          children,
                          lazy=False,
                          into=None,
                          void=False,
                          sep="",
                          add_to=None,
                          js_cb="H.cbs.s",
                          **attrs):
    # TODO: Clean up this function. Only auto-id things with event handlers.
    assert "add_to" not in attrs
    if state.auto_id and "id_" not in attrs:
        attrs["id_"] = state.id_prefix + next(state.id_counter)

    attrs = _element_start_1(tag, attrs, into)

    meta = {}
    if state.liveview is True:
        meta["this"] = "{}('{}')".format(js_cb, attrs["id_"])
        meta["id"] = attrs["id_"]
        meta["js_cb"] = js_cb
    if into is not None:
        into.meta = meta
    for k, v in items(attrs):
        if state.liveview is True and k.startswith("on") and type(v) in (
                list, tuple):
            tmp1 = v
            tmp2 = lambda: _callback(tmp1, meta["this"])
            raw(" ", k, '="', into=into)
            raw(tmp2 if lazy else tmp2(), into=into)
            raw('"', into=into)
        else:
            _element_start_2(k, v, into)

    _element_start_3(children, into, void, sep)

    blob = Blob(into, meta)
    if add_to is not None:
        add_to.append(blob)
    return blob


def control_element(tag,
                    children,
                    lazy=False,
                    into=None,
                    void=False,
                    sep="",
                    add_to=None,
                    **attrs):
    blob = control_element_start(
        tag,
        children,
        lazy=lazy,
        into=into,
        void=void,
        sep="",
        add_to=add_to,
        **attrs)
    element_end(tag, [], into=into, void=void)
    return blob


def control_element_ret(tag,
                        children,
                        lazy=False,
                        into=None,
                        void=False,
                        sep="",
                        add_to=None,
                        **attrs):
    into = Blob()
    control_element_start(
        tag,
        children,
        lazy=lazy,
        into=into,
        void=void,
        sep="",
        add_to=add_to,
        **attrs)
    return into


def control_element_ret2(tag,
                         children,
                         lazy=False,
                         into=None,
                         void=False,
                         sep="",
                         add_to=None,
                         **attrs):
    into = Blob()
    control_element(
        tag,
        children,
        lazy=lazy,
        into=into,
        void=void,
        sep="",
        add_to=add_to,
        **attrs)
    return into


### Input ###

INPUT_TYPES = dict(
    checkbox="H.cbs.c",
    month="H.cbs.i",
    number="H.cbs.i",
    range="H.cbs.f",
    week="H.cbs.i")


def input_(**attrs):
    return control_element(
        "input", [],
        void=True,
        js_cb=INPUT_TYPES.get(attrs.get("type_", "text"), "H.cbs.s"),
        **attrs)


def input_ret(**attrs):
    return control_element_ret("input", [], **attrs)


input_.r = input_ret

### Select ###


def _js_cb_select(attrs):
    type_ = attrs.pop("js_cb", None)
    if type_ is str:
        attrs["js_cb"] = "H.cbs.s"
    elif type_ is int:
        attrs["js_cb"] = "H.cbs.i"
    elif type_ is float:
        attrs["js_cb"] = "H.cbs.f"
    elif type_ is None:
        attrs["js_cb"] = "H.cbs.g"
    else:
        raise Exception(
            "Bad coercion, {}. Only str, unicode, int and float are"
            " supported")


def select_sta(*children, **attrs):
    _js_cb_select(attrs)
    return control_element_start("select", children, **attrs)


def select_end(*children, **kwargs):
    return element_end("select", children, **kwargs)


def select_ret(*children, **attrs):
    _js_cb_select(attrs)
    return control_element_ret("select", children, **attrs)


@contextmanager
def select_con(*children, **attrs):
    _js_cb_select(attrs)
    for x in control_element_con("select", children, **attrs):
        yield x


def select_dec(*children, **attrs):
    _js_cb_select(attrs)
    return control_element_dec("select", children, **attrs)


def select(*children, **attrs):
    _js_cb_select(attrs)
    return control_element("select", children, **attrs)


select.s = select_sta
select.e = select_end
select.r = select_ret
select.c = select_con
select.d = select_dec


### Textarea ###
def _js_cb_textarea(attrs):
    attrs["js_cb"] = attrs.get("js_cb", "H.cbs.t")


def textarea_sta(*children, **attrs):
    _js_cb_textarea(attrs)
    return control_element_start("textarea", children, **attrs)


def textarea_end(*children, **attrs):
    _js_cb_textarea(attrs)
    return element_end("textarea", children, **attrs)


def textarea_ret(*children, **attrs):
    _js_cb_textarea(attrs)
    # TODO FIX!
    return control_element_ret2("textarea", children, **attrs)


@contextmanager
def textarea_con(*children, **attrs):
    _js_cb_textarea(attrs)
    for x in control_element_con("textarea", children, **attrs):
        yield x


def textarea_dec(*children, **attrs):
    _js_cb_textarea(attrs)
    return control_element_dec("textarea", children, **attrs)


def textarea(*children, **attrs):
    _js_cb_textarea(attrs)
    return control_element("textarea", children, **attrs)


textarea.s = textarea_sta
textarea.e = textarea_end
textarea.r = textarea_ret
textarea.c = textarea_con
textarea.d = textarea_dec

### Special tags ###


def doctype(type_="html"):
    raw("<!DOCTYPE ", type_, ">")


### TEMPLATE-ELEMENT ###
def div_sta(*children, **attrs):
    return element_start("div", children, **attrs)


def div_end(*children, **kwargs):
    return element_end("div", children, **kwargs)


def div_ret(*children, **kwargs):
    return element_ret("div", children, **kwargs)


@contextmanager
def div_con(*children, **attrs):
    for x in element_con("div", children, **attrs):
        yield x


def div_dec(*children, **attrs):
    return element_dec("div", children, **attrs)


def div(*children, **attrs):
    return element("div", children, **attrs)


div.s = div_sta
div.e = div_end
div.r = div_ret
div.c = div_con
div.d = div_dec


### TEMPLATE-ELEMENT ###
### TEMPLATE-VOID-ELEMENT ###
def link(*children, **attrs):
    return element("link", children, void=True, **attrs)


def link_ret(*children, **attrs):
    return element_ret("link", children, void=True, **attrs)


link.r = link_ret

### TEMPLATE-VOID-ELEMENT ###

### RENDERED-ELEMENTS ###

### RENDERED-VOID-ELEMENTS ###
