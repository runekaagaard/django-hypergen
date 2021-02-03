# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)

import string, sys
from threading import local
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
def hypergen_context(**kwargs):
    from freedom.core import namespace as ns
    return ns(
        into=[],
        liveview=True,
        id_counter=base65_counter(),
        id_prefix=(freedom.loads(context.request.body)["id_prefix"]
                   if context.request.is_ajax() else ""),
        event_handler_cache={},
        target_id=kwargs.pop("target_id", "__main__"),
        commands=[], )


### Control ###
def hypergen(func, *args, **kwargs):
    with context(hypergen=hypergen_context(**kwargs)):
        func(*args, **kwargs)
        # TODO, use join_html
        html = "".join(
            str(x()) if callable(x) else str(x) for x in context.hypergen.into)
        if context.hypergen.event_handler_cache:
            context.hypergen.commands.append([
                "./freedom", ["setEventHandlerCache"], [
                    context.hypergen.target_id,
                    context.hypergen.event_handler_cache
                ]
            ])
        if not context.request.is_ajax():
            s = '<script>window.applyCommands({})</script>'.format(
                freedom.dumps(context.hypergen.commands))
            pos = html.find("</head")
            if pos != -1:
                html = insert(html, s, pos)
            return HttpResponse(html)
        else:
            context.hypergen.commands.append(
                ["./freedom", ["morph"], [context.hypergen.target_id, html]])
            return context.hypergen.commands


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
    if "is_test" in context:
        func.hypergen_callback_url = "/path/to/{}/".format(func.__name__)
    else:
        func.hypergen_callback_url = reverse_lazy(
            "freedom:callback",
            args=[".".join((func.__module__, func.__name__))])

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
DELETED = ""

### Input ###

INPUT_TYPES = dict(
    checkbox="H.cbs.c",
    month="H.cbs.i",
    number="H.cbs.i",
    range="H.cbs.f",
    week="H.cbs.i")


class base_element(object):  # TODO: Delete
    pass


class input_(base_element):
    tag = "input"
    void = True

    def __init__(self, *children, **attrs):
        self.js_cb = INPUT_TYPES.get(attrs.get("type_", "text"), "H.cbs.s")
        super(input_, self).__init__(*children, **attrs)

    void = True


input_.r = input_

### Select ###


class select(base_element):
    tag = "select"


select.r = select
select.c = select
select.d = select

### Textarea ###


class textarea(base_element):
    tag = "textarea"


textarea.r = textarea
textarea.c = textarea
textarea.d = textarea

### Special tags ###


def doctype(type_="html"):
    raw("<!DOCTYPE ", type_, ">")


### TEMPLATE-ELEMENT ###


class div(base_element):
    tag = "div"


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

### RENDERED-ELEMENTS ###

### RENDERED-VOID-ELEMENTS ###
