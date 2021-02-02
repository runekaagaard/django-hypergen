# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)

import string, sys
from threading import local
from contextlib import contextmanager
from collections import OrderedDict
from functools import wraps
from copy import deepcopy
from types import GeneratorType

from contextlib2 import ContextDecorator
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
                if pos != -1:
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

    def __str__(self):
        return "".join(str(x) for x in self.html)

    def __unicode__(self):
        return "".join([str(x) for x in self.html])


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
DELETED = ""


class div(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is div:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("div", children, **attrs))
        super(div, self).__init__()

    def __enter__(self):
        element_start("div", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("div", [])

    def __str__(self):

        blob = element_ret("div", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


div.r = div
div.c = div
div.d = div


### TEMPLATE-ELEMENT ###
### TEMPLATE-VOID-ELEMENT ###
def link(*children, **attrs):
    return element("link", children, void=True, **attrs)


def link_ret(*children, **attrs):
    return element_ret("link", children, void=True, **attrs)


link.r = link_ret
### TEMPLATE-VOID-ELEMENT ###


DELETED = ""


class a(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is a:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("a", children, **attrs))
        super(a, self).__init__()

    def __enter__(self):
        element_start("a", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("a", [])

    def __str__(self):

        blob = element_ret("a", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


a.r = a
a.c = a
a.d = a



DELETED = ""


class abbr(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is abbr:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("abbr", children, **attrs))
        super(abbr, self).__init__()

    def __enter__(self):
        element_start("abbr", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("abbr", [])

    def __str__(self):

        blob = element_ret("abbr", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


abbr.r = abbr
abbr.c = abbr
abbr.d = abbr



DELETED = ""


class acronym(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is acronym:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("acronym", children, **attrs))
        super(acronym, self).__init__()

    def __enter__(self):
        element_start("acronym", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("acronym", [])

    def __str__(self):

        blob = element_ret("acronym", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


acronym.r = acronym
acronym.c = acronym
acronym.d = acronym



DELETED = ""


class address(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is address:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("address", children, **attrs))
        super(address, self).__init__()

    def __enter__(self):
        element_start("address", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("address", [])

    def __str__(self):

        blob = element_ret("address", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


address.r = address
address.c = address
address.d = address



DELETED = ""


class applet(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is applet:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("applet", children, **attrs))
        super(applet, self).__init__()

    def __enter__(self):
        element_start("applet", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("applet", [])

    def __str__(self):

        blob = element_ret("applet", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


applet.r = applet
applet.c = applet
applet.d = applet



DELETED = ""


class article(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is article:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("article", children, **attrs))
        super(article, self).__init__()

    def __enter__(self):
        element_start("article", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("article", [])

    def __str__(self):

        blob = element_ret("article", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


article.r = article
article.c = article
article.d = article



DELETED = ""


class aside(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is aside:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("aside", children, **attrs))
        super(aside, self).__init__()

    def __enter__(self):
        element_start("aside", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("aside", [])

    def __str__(self):

        blob = element_ret("aside", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


aside.r = aside
aside.c = aside
aside.d = aside



DELETED = ""


class audio(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is audio:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("audio", children, **attrs))
        super(audio, self).__init__()

    def __enter__(self):
        element_start("audio", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("audio", [])

    def __str__(self):

        blob = element_ret("audio", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


audio.r = audio
audio.c = audio
audio.d = audio



DELETED = ""


class b(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is b:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("b", children, **attrs))
        super(b, self).__init__()

    def __enter__(self):
        element_start("b", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("b", [])

    def __str__(self):

        blob = element_ret("b", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


b.r = b
b.c = b
b.d = b



DELETED = ""


class basefont(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is basefont:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("basefont", children, **attrs))
        super(basefont, self).__init__()

    def __enter__(self):
        element_start("basefont", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("basefont", [])

    def __str__(self):

        blob = element_ret("basefont", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


basefont.r = basefont
basefont.c = basefont
basefont.d = basefont



DELETED = ""


class bdi(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is bdi:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("bdi", children, **attrs))
        super(bdi, self).__init__()

    def __enter__(self):
        element_start("bdi", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("bdi", [])

    def __str__(self):

        blob = element_ret("bdi", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


bdi.r = bdi
bdi.c = bdi
bdi.d = bdi



DELETED = ""


class bdo(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is bdo:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("bdo", children, **attrs))
        super(bdo, self).__init__()

    def __enter__(self):
        element_start("bdo", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("bdo", [])

    def __str__(self):

        blob = element_ret("bdo", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


bdo.r = bdo
bdo.c = bdo
bdo.d = bdo



DELETED = ""


class big(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is big:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("big", children, **attrs))
        super(big, self).__init__()

    def __enter__(self):
        element_start("big", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("big", [])

    def __str__(self):

        blob = element_ret("big", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


big.r = big
big.c = big
big.d = big



DELETED = ""


class blockquote(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is blockquote:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("blockquote", children, **attrs))
        super(blockquote, self).__init__()

    def __enter__(self):
        element_start("blockquote", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("blockquote", [])

    def __str__(self):

        blob = element_ret("blockquote", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


blockquote.r = blockquote
blockquote.c = blockquote
blockquote.d = blockquote



DELETED = ""


class body(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is body:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("body", children, **attrs))
        super(body, self).__init__()

    def __enter__(self):
        element_start("body", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("body", [])

    def __str__(self):

        blob = element_ret("body", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


body.r = body
body.c = body
body.d = body



DELETED = ""


class button(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is button:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("button", children, **attrs))
        super(button, self).__init__()

    def __enter__(self):
        element_start("button", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("button", [])

    def __str__(self):

        blob = element_ret("button", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


button.r = button
button.c = button
button.d = button



DELETED = ""


class canvas(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is canvas:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("canvas", children, **attrs))
        super(canvas, self).__init__()

    def __enter__(self):
        element_start("canvas", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("canvas", [])

    def __str__(self):

        blob = element_ret("canvas", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


canvas.r = canvas
canvas.c = canvas
canvas.d = canvas



DELETED = ""


class caption(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is caption:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("caption", children, **attrs))
        super(caption, self).__init__()

    def __enter__(self):
        element_start("caption", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("caption", [])

    def __str__(self):

        blob = element_ret("caption", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


caption.r = caption
caption.c = caption
caption.d = caption



DELETED = ""


class center(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is center:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("center", children, **attrs))
        super(center, self).__init__()

    def __enter__(self):
        element_start("center", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("center", [])

    def __str__(self):

        blob = element_ret("center", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


center.r = center
center.c = center
center.d = center



DELETED = ""


class cite(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is cite:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("cite", children, **attrs))
        super(cite, self).__init__()

    def __enter__(self):
        element_start("cite", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("cite", [])

    def __str__(self):

        blob = element_ret("cite", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


cite.r = cite
cite.c = cite
cite.d = cite



DELETED = ""


class code(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is code:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("code", children, **attrs))
        super(code, self).__init__()

    def __enter__(self):
        element_start("code", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("code", [])

    def __str__(self):

        blob = element_ret("code", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode_(self):
        return self.__str__()


code.r = code
code.c = code
code.d = code



DELETED = ""


class colgroup(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is colgroup:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("colgroup", children, **attrs))
        super(colgroup, self).__init__()

    def __enter__(self):
        element_start("colgroup", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("colgroup", [])

    def __str__(self):

        blob = element_ret("colgroup", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


colgroup.r = colgroup
colgroup.c = colgroup
colgroup.d = colgroup



DELETED = ""


class data(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is data:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("data", children, **attrs))
        super(data, self).__init__()

    def __enter__(self):
        element_start("data", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("data", [])

    def __str__(self):

        blob = element_ret("data", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


data.r = data
data.c = data
data.d = data



DELETED = ""


class datalist(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is datalist:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("datalist", children, **attrs))
        super(datalist, self).__init__()

    def __enter__(self):
        element_start("datalist", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("datalist", [])

    def __str__(self):

        blob = element_ret("datalist", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


datalist.r = datalist
datalist.c = datalist
datalist.d = datalist



DELETED = ""


class dd(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is dd:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("dd", children, **attrs))
        super(dd, self).__init__()

    def __enter__(self):
        element_start("dd", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("dd", [])

    def __str__(self):

        blob = element_ret("dd", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


dd.r = dd
dd.c = dd
dd.d = dd



DELETED = ""


class del_(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is del_:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("del", children, **attrs))
        super(del_, self).__init__()

    def __enter__(self):
        element_start("del", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("del", [])

    def __str__(self):

        blob = element_ret("del", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


del_.r = del_
del_.c = del_
del_.d = del_



DELETED = ""


class details(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is details:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("details", children, **attrs))
        super(details, self).__init__()

    def __enter__(self):
        element_start("details", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("details", [])

    def __str__(self):

        blob = element_ret("details", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


details.r = details
details.c = details
details.d = details



DELETED = ""


class dfn(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is dfn:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("dfn", children, **attrs))
        super(dfn, self).__init__()

    def __enter__(self):
        element_start("dfn", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("dfn", [])

    def __str__(self):

        blob = element_ret("dfn", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


dfn.r = dfn
dfn.c = dfn
dfn.d = dfn



DELETED = ""


class dialog(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is dialog:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("dialog", children, **attrs))
        super(dialog, self).__init__()

    def __enter__(self):
        element_start("dialog", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("dialog", [])

    def __str__(self):

        blob = element_ret("dialog", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


dialog.r = dialog
dialog.c = dialog
dialog.d = dialog



DELETED = ""


class dir_(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is dir_:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("dir", children, **attrs))
        super(dir_, self).__init__()

    def __enter__(self):
        element_start("dir", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("dir", [])

    def __str__(self):

        blob = element_ret("dir", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


dir_.r = dir_
dir_.c = dir_
dir_.d = dir_



DELETED = ""


class dl(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is dl:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("dl", children, **attrs))
        super(dl, self).__init__()

    def __enter__(self):
        element_start("dl", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("dl", [])

    def __str__(self):

        blob = element_ret("dl", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


dl.r = dl
dl.c = dl
dl.d = dl



DELETED = ""


class dt(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is dt:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("dt", children, **attrs))
        super(dt, self).__init__()

    def __enter__(self):
        element_start("dt", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("dt", [])

    def __str__(self):

        blob = element_ret("dt", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


dt.r = dt
dt.c = dt
dt.d = dt



DELETED = ""


class em(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is em:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("em", children, **attrs))
        super(em, self).__init__()

    def __enter__(self):
        element_start("em", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("em", [])

    def __str__(self):

        blob = element_ret("em", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


em.r = em
em.c = em
em.d = em



DELETED = ""


class fieldset(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is fieldset:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("fieldset", children, **attrs))
        super(fieldset, self).__init__()

    def __enter__(self):
        element_start("fieldset", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("fieldset", [])

    def __str__(self):

        blob = element_ret("fieldset", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


fieldset.r = fieldset
fieldset.c = fieldset
fieldset.d = fieldset



DELETED = ""


class figcaption(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is figcaption:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("figcaption", children, **attrs))
        super(figcaption, self).__init__()

    def __enter__(self):
        element_start("figcaption", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("figcaption", [])

    def __str__(self):

        blob = element_ret("figcaption", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


figcaption.r = figcaption
figcaption.c = figcaption
figcaption.d = figcaption



DELETED = ""


class figure(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is figure:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("figure", children, **attrs))
        super(figure, self).__init__()

    def __enter__(self):
        element_start("figure", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("figure", [])

    def __str__(self):

        blob = element_ret("figure", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


figure.r = figure
figure.c = figure
figure.d = figure



DELETED = ""


class font(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is font:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("font", children, **attrs))
        super(font, self).__init__()

    def __enter__(self):
        element_start("font", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("font", [])

    def __str__(self):

        blob = element_ret("font", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


font.r = font
font.c = font
font.d = font



DELETED = ""


class footer(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is footer:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("footer", children, **attrs))
        super(footer, self).__init__()

    def __enter__(self):
        element_start("footer", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("footer", [])

    def __str__(self):

        blob = element_ret("footer", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


footer.r = footer
footer.c = footer
footer.d = footer



DELETED = ""


class form(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is form:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("form", children, **attrs))
        super(form, self).__init__()

    def __enter__(self):
        element_start("form", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("form", [])

    def __str__(self):

        blob = element_ret("form", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


form.r = form
form.c = form
form.d = form



DELETED = ""


class frame(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is frame:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("frame", children, **attrs))
        super(frame, self).__init__()

    def __enter__(self):
        element_start("frame", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("frame", [])

    def __str__(self):

        blob = element_ret("frame", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


frame.r = frame
frame.c = frame
frame.d = frame



DELETED = ""


class frameset(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is frameset:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("frameset", children, **attrs))
        super(frameset, self).__init__()

    def __enter__(self):
        element_start("frameset", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("frameset", [])

    def __str__(self):

        blob = element_ret("frameset", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


frameset.r = frameset
frameset.c = frameset
frameset.d = frameset



DELETED = ""


class h1(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is h1:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("h1", children, **attrs))
        super(h1, self).__init__()

    def __enter__(self):
        element_start("h1", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("h1", [])

    def __str__(self):

        blob = element_ret("h1", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


h1.r = h1
h1.c = h1
h1.d = h1



DELETED = ""


class h2(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is h2:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("h2", children, **attrs))
        super(h2, self).__init__()

    def __enter__(self):
        element_start("h2", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("h2", [])

    def __str__(self):

        blob = element_ret("h2", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


h2.r = h2
h2.c = h2
h2.d = h2



DELETED = ""


class h3(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is h3:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("h3", children, **attrs))
        super(h3, self).__init__()

    def __enter__(self):
        element_start("h3", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("h3", [])

    def __str__(self):

        blob = element_ret("h3", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


h3.r = h3
h3.c = h3
h3.d = h3



DELETED = ""


class h4(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is h4:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("h4", children, **attrs))
        super(h4, self).__init__()

    def __enter__(self):
        element_start("h4", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("h4", [])

    def __str__(self):

        blob = element_ret("h4", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


h4.r = h4
h4.c = h4
h4.d = h4



DELETED = ""


class h5(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is h5:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("h5", children, **attrs))
        super(h5, self).__init__()

    def __enter__(self):
        element_start("h5", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("h5", [])

    def __str__(self):

        blob = element_ret("h5", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


h5.r = h5
h5.c = h5
h5.d = h5



DELETED = ""


class h6(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is h6:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("h6", children, **attrs))
        super(h6, self).__init__()

    def __enter__(self):
        element_start("h6", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("h6", [])

    def __str__(self):

        blob = element_ret("h6", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


h6.r = h6
h6.c = h6
h6.d = h6



DELETED = ""


class head(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is head:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("head", children, **attrs))
        super(head, self).__init__()

    def __enter__(self):
        element_start("head", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("head", [])

    def __str__(self):

        blob = element_ret("head", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


head.r = head
head.c = head
head.d = head



DELETED = ""


class header(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is header:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("header", children, **attrs))
        super(header, self).__init__()

    def __enter__(self):
        element_start("header", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("header", [])

    def __str__(self):

        blob = element_ret("header", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


header.r = header
header.c = header
header.d = header



DELETED = ""


class html(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is html:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("html", children, **attrs))
        super(html, self).__init__()

    def __enter__(self):
        element_start("html", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("html", [])

    def __str__(self):

        blob = element_ret("html", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


html.r = html
html.c = html
html.d = html



DELETED = ""


class i(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is i:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("i", children, **attrs))
        super(i, self).__init__()

    def __enter__(self):
        element_start("i", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("i", [])

    def __str__(self):

        blob = element_ret("i", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


i.r = i
i.c = i
i.d = i



DELETED = ""


class iframe(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is iframe:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("iframe", children, **attrs))
        super(iframe, self).__init__()

    def __enter__(self):
        element_start("iframe", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("iframe", [])

    def __str__(self):

        blob = element_ret("iframe", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


iframe.r = iframe
iframe.c = iframe
iframe.d = iframe



DELETED = ""


class ins(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is ins:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("ins", children, **attrs))
        super(ins, self).__init__()

    def __enter__(self):
        element_start("ins", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("ins", [])

    def __str__(self):

        blob = element_ret("ins", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


ins.r = ins
ins.c = ins
ins.d = ins



DELETED = ""


class kbd(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is kbd:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("kbd", children, **attrs))
        super(kbd, self).__init__()

    def __enter__(self):
        element_start("kbd", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("kbd", [])

    def __str__(self):

        blob = element_ret("kbd", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


kbd.r = kbd
kbd.c = kbd
kbd.d = kbd



DELETED = ""


class label(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is label:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("label", children, **attrs))
        super(label, self).__init__()

    def __enter__(self):
        element_start("label", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("label", [])

    def __str__(self):

        blob = element_ret("label", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


label.r = label
label.c = label
label.d = label



DELETED = ""


class legend(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is legend:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("legend", children, **attrs))
        super(legend, self).__init__()

    def __enter__(self):
        element_start("legend", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("legend", [])

    def __str__(self):

        blob = element_ret("legend", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


legend.r = legend
legend.c = legend
legend.d = legend



DELETED = ""


class li(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is li:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("li", children, **attrs))
        super(li, self).__init__()

    def __enter__(self):
        element_start("li", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("li", [])

    def __str__(self):

        blob = element_ret("li", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


li.r = li
li.c = li
li.d = li



DELETED = ""


class main(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is main:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("main", children, **attrs))
        super(main, self).__init__()

    def __enter__(self):
        element_start("main", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("main", [])

    def __str__(self):

        blob = element_ret("main", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


main.r = main
main.c = main
main.d = main



DELETED = ""


class map_(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is map_:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("map", children, **attrs))
        super(map_, self).__init__()

    def __enter__(self):
        element_start("map", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("map", [])

    def __str__(self):

        blob = element_ret("map", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


map_.r = map_
map_.c = map_
map_.d = map_



DELETED = ""


class mark(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is mark:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("mark", children, **attrs))
        super(mark, self).__init__()

    def __enter__(self):
        element_start("mark", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("mark", [])

    def __str__(self):

        blob = element_ret("mark", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


mark.r = mark
mark.c = mark
mark.d = mark



DELETED = ""


class meter(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is meter:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("meter", children, **attrs))
        super(meter, self).__init__()

    def __enter__(self):
        element_start("meter", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("meter", [])

    def __str__(self):

        blob = element_ret("meter", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


meter.r = meter
meter.c = meter
meter.d = meter



DELETED = ""


class nav(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is nav:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("nav", children, **attrs))
        super(nav, self).__init__()

    def __enter__(self):
        element_start("nav", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("nav", [])

    def __str__(self):

        blob = element_ret("nav", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


nav.r = nav
nav.c = nav
nav.d = nav



DELETED = ""


class noframes(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is noframes:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("noframes", children, **attrs))
        super(noframes, self).__init__()

    def __enter__(self):
        element_start("noframes", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("noframes", [])

    def __str__(self):

        blob = element_ret("noframes", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


noframes.r = noframes
noframes.c = noframes
noframes.d = noframes



DELETED = ""


class noscript(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is noscript:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("noscript", children, **attrs))
        super(noscript, self).__init__()

    def __enter__(self):
        element_start("noscript", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("noscript", [])

    def __str__(self):

        blob = element_ret("noscript", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


noscript.r = noscript
noscript.c = noscript
noscript.d = noscript



DELETED = ""


class object_(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is object_:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("object", children, **attrs))
        super(object_, self).__init__()

    def __enter__(self):
        element_start("object", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("object", [])

    def __str__(self):

        blob = element_ret("object", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


object_.r = object_
object_.c = object_
object_.d = object_



DELETED = ""


class ol(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is ol:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("ol", children, **attrs))
        super(ol, self).__init__()

    def __enter__(self):
        element_start("ol", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("ol", [])

    def __str__(self):

        blob = element_ret("ol", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


ol.r = ol
ol.c = ol
ol.d = ol



DELETED = ""


class optgroup(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is optgroup:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("optgroup", children, **attrs))
        super(optgroup, self).__init__()

    def __enter__(self):
        element_start("optgroup", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("optgroup", [])

    def __str__(self):

        blob = element_ret("optgroup", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


optgroup.r = optgroup
optgroup.c = optgroup
optgroup.d = optgroup



DELETED = ""


class option(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is option:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("option", children, **attrs))
        super(option, self).__init__()

    def __enter__(self):
        element_start("option", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("option", [])

    def __str__(self):

        blob = element_ret("option", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


option.r = option
option.c = option
option.d = option



DELETED = ""


class output(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is output:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("output", children, **attrs))
        super(output, self).__init__()

    def __enter__(self):
        element_start("output", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("output", [])

    def __str__(self):

        blob = element_ret("output", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


output.r = output
output.c = output
output.d = output



DELETED = ""


class p(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is p:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("p", children, **attrs))
        super(p, self).__init__()

    def __enter__(self):
        element_start("p", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("p", [])

    def __str__(self):

        blob = element_ret("p", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


p.r = p
p.c = p
p.d = p



DELETED = ""


class picture(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is picture:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("picture", children, **attrs))
        super(picture, self).__init__()

    def __enter__(self):
        element_start("picture", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("picture", [])

    def __str__(self):

        blob = element_ret("picture", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


picture.r = picture
picture.c = picture
picture.d = picture



DELETED = ""


class pre(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is pre:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("pre", children, **attrs))
        super(pre, self).__init__()

    def __enter__(self):
        element_start("pre", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("pre", [])

    def __str__(self):

        blob = element_ret("pre", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


pre.r = pre
pre.c = pre
pre.d = pre



DELETED = ""


class progress(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is progress:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("progress", children, **attrs))
        super(progress, self).__init__()

    def __enter__(self):
        element_start("progress", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("progress", [])

    def __str__(self):

        blob = element_ret("progress", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


progress.r = progress
progress.c = progress
progress.d = progress



DELETED = ""


class q(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is q:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("q", children, **attrs))
        super(q, self).__init__()

    def __enter__(self):
        element_start("q", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("q", [])

    def __str__(self):

        blob = element_ret("q", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


q.r = q
q.c = q
q.d = q



DELETED = ""


class rp(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is rp:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("rp", children, **attrs))
        super(rp, self).__init__()

    def __enter__(self):
        element_start("rp", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("rp", [])

    def __str__(self):

        blob = element_ret("rp", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


rp.r = rp
rp.c = rp
rp.d = rp



DELETED = ""


class rt(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is rt:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("rt", children, **attrs))
        super(rt, self).__init__()

    def __enter__(self):
        element_start("rt", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("rt", [])

    def __str__(self):

        blob = element_ret("rt", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


rt.r = rt
rt.c = rt
rt.d = rt



DELETED = ""


class ruby(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is ruby:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("ruby", children, **attrs))
        super(ruby, self).__init__()

    def __enter__(self):
        element_start("ruby", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("ruby", [])

    def __str__(self):

        blob = element_ret("ruby", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


ruby.r = ruby
ruby.c = ruby
ruby.d = ruby



DELETED = ""


class s(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is s:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("s", children, **attrs))
        super(s, self).__init__()

    def __enter__(self):
        element_start("s", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("s", [])

    def __str__(self):

        blob = element_ret("s", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


s.r = s
s.c = s
s.d = s



DELETED = ""


class samp(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is samp:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("samp", children, **attrs))
        super(samp, self).__init__()

    def __enter__(self):
        element_start("samp", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("samp", [])

    def __str__(self):

        blob = element_ret("samp", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


samp.r = samp
samp.c = samp
samp.d = samp



DELETED = ""


class script(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is script:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("script", children, **attrs))
        super(script, self).__init__()

    def __enter__(self):
        element_start("script", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("script", [])

    def __str__(self):

        blob = element_ret("script", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


script.r = script
script.c = script
script.d = script



DELETED = ""


class section(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is section:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("section", children, **attrs))
        super(section, self).__init__()

    def __enter__(self):
        element_start("section", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("section", [])

    def __str__(self):

        blob = element_ret("section", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


section.r = section
section.c = section
section.d = section



DELETED = ""


class small(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is small:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("small", children, **attrs))
        super(small, self).__init__()

    def __enter__(self):
        element_start("small", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("small", [])

    def __str__(self):

        blob = element_ret("small", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


small.r = small
small.c = small
small.d = small



DELETED = ""


class span(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is span:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("span", children, **attrs))
        super(span, self).__init__()

    def __enter__(self):
        element_start("span", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("span", [])

    def __str__(self):

        blob = element_ret("span", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


span.r = span
span.c = span
span.d = span



DELETED = ""


class strike(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is strike:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("strike", children, **attrs))
        super(strike, self).__init__()

    def __enter__(self):
        element_start("strike", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("strike", [])

    def __str__(self):

        blob = element_ret("strike", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


strike.r = strike
strike.c = strike
strike.d = strike



DELETED = ""


class strong(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is strong:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("strong", children, **attrs))
        super(strong, self).__init__()

    def __enter__(self):
        element_start("strong", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("strong", [])

    def __str__(self):

        blob = element_ret("strong", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


strong.r = strong
strong.c = strong
strong.d = strong



DELETED = ""


class style(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is style:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("style", children, **attrs))
        super(style, self).__init__()

    def __enter__(self):
        element_start("style", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("style", [])

    def __str__(self):

        blob = element_ret("style", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


style.r = style
style.c = style
style.d = style



DELETED = ""


class sub(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is sub:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("sub", children, **attrs))
        super(sub, self).__init__()

    def __enter__(self):
        element_start("sub", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("sub", [])

    def __str__(self):

        blob = element_ret("sub", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


sub.r = sub
sub.c = sub
sub.d = sub



DELETED = ""


class summary(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is summary:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("summary", children, **attrs))
        super(summary, self).__init__()

    def __enter__(self):
        element_start("summary", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("summary", [])

    def __str__(self):

        blob = element_ret("summary", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


summary.r = summary
summary.c = summary
summary.d = summary



DELETED = ""


class sup(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is sup:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("sup", children, **attrs))
        super(sup, self).__init__()

    def __enter__(self):
        element_start("sup", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("sup", [])

    def __str__(self):

        blob = element_ret("sup", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


sup.r = sup
sup.c = sup
sup.d = sup



DELETED = ""


class svg(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is svg:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("svg", children, **attrs))
        super(svg, self).__init__()

    def __enter__(self):
        element_start("svg", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("svg", [])

    def __str__(self):

        blob = element_ret("svg", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


svg.r = svg
svg.c = svg
svg.d = svg



DELETED = ""


class table(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is table:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("table", children, **attrs))
        super(table, self).__init__()

    def __enter__(self):
        element_start("table", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("table", [])

    def __str__(self):

        blob = element_ret("table", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


table.r = table
table.c = table
table.d = table



DELETED = ""


class tbody(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is tbody:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("tbody", children, **attrs))
        super(tbody, self).__init__()

    def __enter__(self):
        element_start("tbody", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("tbody", [])

    def __str__(self):

        blob = element_ret("tbody", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


tbody.r = tbody
tbody.c = tbody
tbody.d = tbody



DELETED = ""


class td(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is td:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("td", children, **attrs))
        super(td, self).__init__()

    def __enter__(self):
        element_start("td", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("td", [])

    def __str__(self):

        blob = element_ret("td", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


td.r = td
td.c = td
td.d = td



DELETED = ""


class template(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is template:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("template", children, **attrs))
        super(template, self).__init__()

    def __enter__(self):
        element_start("template", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("template", [])

    def __str__(self):

        blob = element_ret("template", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


template.r = template
template.c = template
template.d = template



DELETED = ""


class tfoot(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is tfoot:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("tfoot", children, **attrs))
        super(tfoot, self).__init__()

    def __enter__(self):
        element_start("tfoot", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("tfoot", [])

    def __str__(self):

        blob = element_ret("tfoot", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


tfoot.r = tfoot
tfoot.c = tfoot
tfoot.d = tfoot



DELETED = ""


class th(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is th:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("th", children, **attrs))
        super(th, self).__init__()

    def __enter__(self):
        element_start("th", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("th", [])

    def __str__(self):

        blob = element_ret("th", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


th.r = th
th.c = th
th.d = th



DELETED = ""


class thead(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is thead:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("thead", children, **attrs))
        super(thead, self).__init__()

    def __enter__(self):
        element_start("thead", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("thead", [])

    def __str__(self):

        blob = element_ret("thead", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


thead.r = thead
thead.c = thead
thead.d = thead



DELETED = ""


class time(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is time:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("time", children, **attrs))
        super(time, self).__init__()

    def __enter__(self):
        element_start("time", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("time", [])

    def __str__(self):

        blob = element_ret("time", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


time.r = time
time.c = time
time.d = time



DELETED = ""


class title(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is title:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("title", children, **attrs))
        super(title, self).__init__()

    def __enter__(self):
        element_start("title", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("title", [])

    def __str__(self):

        blob = element_ret("title", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


title.r = title
title.c = title
title.d = title



DELETED = ""


class tr(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is tr:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("tr", children, **attrs))
        super(tr, self).__init__()

    def __enter__(self):
        element_start("tr", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("tr", [])

    def __str_(self):

        blob = element_ret("tr", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str_()


tr.r = tr
tr.c = tr
tr.d = tr



DELETED = ""


class tt(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is tt:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("tt", children, **attrs))
        super(tt, self).__init__()

    def __enter__(self):
        element_start("tt", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("tt", [])

    def __str__(self):

        blob = element_ret("tt", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


tt.r = tt
tt.c = tt
tt.d = tt



DELETED = ""


class u(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is u:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("u", children, **attrs))
        super(u, self).__init__()

    def __enter__(self):
        element_start("u", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("u", [])

    def __str__(self):

        blob = element_ret("u", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


u.r = u
u.c = u
u.d = u



DELETED = ""


class ul(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is ul:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("ul", children, **attrs))
        super(ul, self).__init__()

    def __enter__(self):
        element_start("ul", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("ul", [])

    def __str__(self):

        blob = element_ret("ul", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


ul.r = ul
ul.c = ul
ul.d = ul



DELETED = ""


class var(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is var:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("var", children, **attrs))
        super(var, self).__init__()

    def __enter__(self):
        element_start("var", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("var", [])

    def __str__(self):

        blob = element_ret("var", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


var.r = var
var.c = var
var.d = var



DELETED = ""


class video(ContextDecorator):
    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if type(child) is video:
                state.html[child.i] = DELETED

        state.html.append(lambda: element_ret("video", children, **attrs))
        super(video, self).__init__()

    def __enter__(self):
        element_start("video", self.children, **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end("video", [])

    def __str__(self):

        blob = element_ret("video", self.children, **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


video.r = video
video.c = video
video.d = video





def wbr(*children, **attrs):
    return element("wbr", children, void=True, **attrs)


def wbr_ret(*children, **attrs):
    return element_ret("wbr", children, void=True, **attrs)


wbr.r = wbr_ret

def img(*children, **attrs):
    return element("img", children, void=True, **attrs)


def img_ret(*children, **attrs):
    return element_ret("img", children, void=True, **attrs)


img.r = img_ret

def area(*children, **attrs):
    return element("area", children, void=True, **attrs)


def area_ret(*children, **attrs):
    return element_ret("area", children, void=True, **attrs)


area.r = area_ret

def hr(*children, **attrs):
    return element("hr", children, void=True, **attrs)


def hr_ret(*children, **attrs):
    return element_ret("hr", children, void=True, **attrs)


hr.r = hr_ret

def param(*children, **attrs):
    return element("param", children, void=True, **attrs)


def param_ret(*children, **attrs):
    return element_ret("param", children, void=True, **attrs)


param.r = param_ret

def keygen(*children, **attrs):
    return element("keygen", children, void=True, **attrs)


def keygen_ret(*children, **attrs):
    return element_ret("keygen", children, void=True, **attrs)


keygen.r = keygen_ret

def source(*children, **attrs):
    return element("source", children, void=True, **attrs)


def source_ret(*children, **attrs):
    return element_ret("source", children, void=True, **attrs)


source.r = source_ret

def base(*children, **attrs):
    return element("base", children, void=True, **attrs)


def base_ret(*children, **attrs):
    return element_ret("base", children, void=True, **attrs)


base.r = base_ret

def meta(*children, **attrs):
    return element("meta", children, void=True, **attrs)


def meta_ret(*children, **attrs):
    return element_ret("meta", children, void=True, **attrs)


meta.r = meta_ret

def br(*children, **attrs):
    return element("br", children, void=True, **attrs)


def br_ret(*children, **attrs):
    return element_ret("br", children, void=True, **attrs)


br.r = br_ret

def track(*children, **attrs):
    return element("track", children, void=True, **attrs)


def track_ret(*children, **attrs):
    return element_ret("track", children, void=True, **attrs)


track.r = track_ret

def menuitem(*children, **attrs):
    return element("menuitem", children, void=True, **attrs)


def menuitem_ret(*children, **attrs):
    return element_ret("menuitem", children, void=True, **attrs)


menuitem.r = menuitem_ret

def command(*children, **attrs):
    return element("command", children, void=True, **attrs)


def command_ret(*children, **attrs):
    return element_ret("command", children, void=True, **attrs)


command.r = command_ret

def embed(*children, **attrs):
    return element("embed", children, void=True, **attrs)


def embed_ret(*children, **attrs):
    return element_ret("embed", children, void=True, **attrs)


embed.r = embed_ret

def col(*children, **attrs):
    return element("col", children, void=True, **attrs)


def col_ret(*children, **attrs):
    return element_ret("col", children, void=True, **attrs)


col.r = col_ret

