# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)

from django.templatetags.static import static

d = dict

import string, sys, time, threading, datetime, json, logging, io
from collections import OrderedDict
from types import GeneratorType
from functools import wraps, update_wrapper
from copy import deepcopy

from contextlib import ContextDecorator, contextmanager, redirect_stderr
from pyrsistent import pmap, m

from django.http.response import HttpResponse, HttpResponseRedirect
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_str as force_text

try:
    import docutils.core
    docutils_ok = True
except ImportError:
    docutils_ok = False

from django.utils.safestring import mark_safe
from django.utils.dateparse import parse_date, parse_datetime, parse_time
from django.conf import settings
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object  # Backwards compatibility.

logger = logging.getLogger(__name__)

__all__ = [
    "a", "abbr", "acronym", "address", "applet", "area", "article", "aside", "audio", "b", "base", "basefont", "bdi",
    "bdo", "big", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code", "col",
    "colgroup", "data", "datalist", "dd", "del_", "details", "dfn", "dialog", "dir_", "div", "dl", "doctype", "dt",
    "em", "embed", "fieldset", "figcaption", "figure", "font", "footer", "form", "frame", "frameset", "h1", "h2",
    "h3", "h4", "h5", "h6", "head", "header", "hr", "html", "i", "iframe", "img", "input_", "ins", "kbd", "label",
    "legend", "li", "link", "main", "map_", "mark", "meta", "meter", "nav", "noframes", "noscript", "object_", "ol",
    "optgroup", "option", "output", "p", "param", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp",
    "script", "section", "select", "small", "source", "span", "strike", "strong", "style", "sub", "summary", "sup",
    "svg", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track",
    "tt", "u", "ul", "var", "video", "wbr", "component", "hypergen", "hypergen_to_response", "raw", "OMIT", "context",
    "write", "rst"]

### Python 2+3 compatibility ###

def make_string(s):
    # TODO: WHY IS THERE AN IF STATEMENT HERE AT ALL?
    # We had a bug where 0 int did not get rendered. I suck.
    if s or type(s) in (int, float):
        return force_text(s)
    else:
        return ""

if sys.version_info.major > 2:
    from html import escape

    def items(x):
        return list(x.items())
else:
    from cgi import escape

    def items(x):
        return iter(x.items())

### Constants ####

OMIT = "__OMIT__"

### Utilities ###

def wrap2(f):
    """
    A a decorator decorator, allowing the decorator to be used as:
        @decorator(with, arguments, and=kwargs)
    or
        @decorator

    It does not work for a wrapped function that takes a callback as the only input.

    It looks like this:

        @wrap2
        def mydecorator(func, *dargs, **dkwargs):
            @wraps(func)
            def _(*fargs, **fkwargs):
                return func(*fargs, **fkwargs)

            return _


        @mydecorator
        def myfunc(x, y=19):
            return x + y


        @mydecorator(42, foo=True)
        def myfunc2(x, y=19):
            return x + y
    """
    def _(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            f2 = f(args[0])
            update_wrapper(f2, args[0])
            return f2
        else:

            def f3(f4):
                f5 = f(f4, *args, **kwargs)
                update_wrapper(f5, f4)
                return f5

            return f3

    return _

### Rendering ###

def hypergen_context(data=None):
    if data is None:
        data = {}

    c_ = m(into=[], ids=set())

    return c_

@wrap2
def hypergen_context_decorator(func, *dargs, **dkwargs):
    @wraps(func)
    def _(*fargs, **fkwargs):
        with c(hypergen=hypergen_context()):
            return func(*fargs, **fkwargs)

    return _

def hypergen(func, *args, **kwargs):
    with c(hypergen=hypergen_context(kwargs)):
        func(*args, **kwargs)
        return join_html(c.hypergen.into)

def hypergen_to_response(func, *args, **kwargs):
    status = kwargs.pop("status", None)
    return HttpResponse(hypergen(func, *args, **kwargs), status)

### Helpers ###
class LazyAttribute(object):
    def __init__(self, k, v):
        self.k = k
        self.v = v

    def __str__(self):
        if not self.v:
            return ""
        else:
            return ' {}="{}"'.format(t(self.k), t(self.v))

    def __unicode__(self):
        return self.__str__()

def join_html(html):
    def fmt(html):
        for item in html:
            if issubclass(type(item), base_element):
                yield item.as_string()
            elif callable(item):
                yield item()
            elif type(item) is GeneratorType:
                with c(at="hypergen", into=[]):
                    yield join_html(item)
            else:
                yield item

    return "".join(make_string(x) for x in fmt(html))

def raw(*children):
    c.hypergen.into.extend(children)

def write(*children):
    c.hypergen.into.extend(t(x) for x in children)

def t(s, quote=True, translatable=False):
    return translate(escape(make_string(s), quote=quote), translatable=translatable)

def rst(restructured_text, report_level=docutils.utils.Reporter.SEVERE_LEVEL + 1):
    if not docutils_ok:
        raise Exception("Please 'pip install docutils' to use the rst() function.")
    raw(
        docutils.core.publish_parts(restructured_text, writer_name="html",
        settings_overrides={'_disable_config': True, 'report_level': report_level})["html_body"])

### Base dom element ###
class THIS(object):
    pass

NON_SCALARS = set((list, dict, tuple))
DELETED = ""

COERCE = {str: "hypergen.coerce.str", int: "hypergen.coerce.int", float: "hypergen.coerce.float"}

class base_element(ContextDecorator):
    void = False
    auto_id = False
    config_attrs = {"t", "sep", "coerce_to", "js_coerce_func", "js_value_func"}
    translatable = True
    translatable_attributes = ["placeholder", "title"]

    def __new__(cls, *args, **kwargs):
        instance = ContextDecorator.__new__(cls)
        setattr(instance, "tag", cls.__name__.rstrip("_"))
        return instance

    def __init__(self, *children, **attrs):
        def init(self, *children, **attrs):
            self.t = attrs.get("t", t)
            self.children = children
            self.attrs = attrs

            id_ = self.attrs.get("id_", None)
            if type(id_) in (tuple, list):
                id_ = "-".join(str(x) for x in id_)
            self.attrs["id_"] = LazyAttribute("id", id_)

            self.i = len(c.hypergen.into)
            self.sep = attrs.get("sep", "")
            self.end_char = attrs.pop("end", None)
            self.js_value_func = attrs.get("js_value_func", "hypergen.read.value")

            coerce_to = attrs.get("coerce_to", None)
            if coerce_to is not None:
                try:
                    self.js_coerce_func = COERCE[coerce_to]
                except KeyError:
                    raise Exception("coerce must be one of: {}".format(list(COERCE.keys())))
            else:
                self.js_coerce_func = attrs.get("js_coerce_func", None)

            c.hypergen.into.extend(self.start())
            c.hypergen.into.extend(self.end())
            self.j = len(c.hypergen.into)
            super(base_element, self).__init__()

        assert "hypergen" in c, "Element called outside hypergen context."
        c.hypergen.wrap_elements(init, self, *children, **attrs)

        if self.attrs["id_"].v is not None:
            id_ = self.attrs["id_"].v
            assert id_ not in c.hypergen["ids"], "Duplicate id: {}".format(id_)
            c.hypergen["ids"].add(id_)

    def __enter__(self):
        c.hypergen.into.extend(self.start())
        self.delete()
        return self

    def __exit__(self, *exc):
        if not self.void:
            c.hypergen.into.extend(self.end())

    def __repr__(self):
        def value(v):
            if isinstance(v, LazyAttribute):
                return '"{}"'.format(v.v)
            elif v is THIS:
                return "THIS"
            elif callable(v) and hasattr(v, "hypergen_callback_signature"):
                name, a, kw = v.hypergen_callback_signature
                return "{}({})".format(name, signature(a, kw))
            elif callable(v):
                if hasattr(v, "__name__"):
                    return ".".join((v.__module__, v.__name__)).replace("builtins.", "")
                else:
                    return repr(v)
            elif type(v) is str:
                return '"{}"'.format(v)
            else:
                return repr(v)

        def args(x):
            return value(x)

        def kwargs(k, v):
            return k, value(v)

        def signature(a, kw):
            a, kw = deepcopy(a), deepcopy(kw)
            return ", ".join([args(x) for x in a] + [
                "{}={}".format(*kwargs(k, v))
                for k, v in list(kw.items()) if not (isinstance(v, LazyAttribute) and v.v is None)])

        return "{}({})".format(self.__class__.__name__, signature(self.children, self.attrs))

    def as_string(self):
        into = self.start()
        into.extend(self.end())
        s = join_html(into)
        return s

    def delete(self):
        for i in range(self.i, self.j):
            c.hypergen.into[i] = DELETED

    def format_children(self, children, nested=False):
        into = []
        sep = self.t(self.sep)

        for x in children:
            if x in ("", None):
                continue
            elif issubclass(type(x), base_element):
                x.delete()
                into.append(x)
            elif type(x) is Component:
                x.delete()
                into.extend(x.into)
            elif type(x) in (list, tuple, GeneratorType):
                into.extend(self.format_children(list(x), nested=True))
            elif callable(x):
                into.append(x)
            else:
                into.append(self.t(x, translatable=self.translatable))
            if sep:
                into.append(sep)
        if sep and children:
            into.pop()

        if self.end_char and not nested:
            into.append(self.t(self.end_char))

        return into

    def ensure_id(self):
        assert self.attrs["id_"].v is not None, "You need to set an ID for {}".format(repr(self))

    def attribute(self, k, v):
        k = t(k).rstrip("_").replace("_", "-")
        if v == OMIT or v is None:
            return []
        elif callable(v):
            return v(self, k, v)
        elif type(v) is LazyAttribute:
            return [v]
        elif type(v) is bool:
            if v is True:
                return [" ", k]
            else:
                return []
        elif k == "style" and type(v) in (dict, OrderedDict):
            return [" ", k, '="', ";".join(t(k1.replace("_", "-")) + ":" + t(v1) for k1, v1 in items(v)), '"']
        elif k == "class" and type(v) in (list, tuple, set):
            return [" ", k, '="', t(" ".join(v)), '"']
        else:
            if v is None:
                v = ""
            else:
                v = t(v, translatable=(k in self.translatable_attributes and type(v) is str))
            assert '"' not in v, "How dare you put a \" in my attributes! :)"
            return [" ", k, '="', v, '"']

    def start(self):
        into = ["<", self.tag]
        for k, v in items(self.attrs):
            if k in self.config_attrs:
                continue
            into.extend(self.attribute(k, v))

        if self.void:
            into.append(join(("/")))
        into.append(join('>',))
        into.extend(self.format_children(self.children))
        return into

    def end(self):
        if not self.void:
            return ["</{}>".format(self.tag)]
        else:
            return [""]

class base_element_void(base_element):
    void = True
    translatable = False

class Component(object):
    def __init__(self, into, i, j):
        self.into = into
        self.i = i
        self.j = j

    def delete(self):
        for i in range(self.i, self.j):
            c.hypergen.into[i] = DELETED

def component(f):
    @wraps(f)
    def _(*args, **kwargs):
        with c(into=[], at="hypergen"):
            f(*args, **kwargs)
            into = c.hypergen.into
        i = len(c.hypergen.into)
        c.hypergen.into.extend(into)
        j = len(c.hypergen.into)
        return Component(into, i, j)

    return _

### Some special dom elements ###

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

# TODO: Move stuff to liveview.
class input_(base_element_void):
    void = True

    def __init__(self, *children, **attrs):
        if attrs.get("type_", None) == "radio":
            assert attrs.get("name"), "Name must be set for radio buttons."
        super(input_, self).__init__(*children, **attrs)
        self.js_value_func = attrs.pop("js_value_func",
            JS_VALUE_FUNCS.get(attrs.get("type_", "text"), "hypergen.read.value"))
        if self.js_coerce_func is None:
            self.js_coerce_func = attrs.pop("js_coerce_func", JS_COERCE_FUNCS.get(attrs.get("type_", "text"), None))

    def attribute(self, k, v):
        if k != "value":
            return super().attribute(k, v)

        type_ = self.attrs.get("type_", None)
        if type_ == "datetime-local":
            return [" ", k, '="', v.strftime("%Y-%m-%dT%H:%M:%S"), '"']
        elif type_ == "month" and type(v) is dict:
            return [" ", k, '="', "{:04}-{:02}".format(v["year"], v["month"]), '"']
        elif type_ == "week" and type(v) is dict:
            return [" ", k, '="', "{:04}-W{:02}".format(v["year"], v["week"]), '"']
        else:
            return super().attribute(k, v)

### Special tags ###

def doctype(type_="html"):
    raw("<!DOCTYPE ", type_, ">")

### All the tags ###
# yapf: disable
class a(base_element):
    def __init__(self, *children, **attrs):
        # TODO: Move to liveview.
        href = attrs.get("href")
        if type(href) is StringWithMeta:
            base_template1 = href.meta.get("base_template", None)
            if base_template1 is not None:
                base_template2 = getattr(c, "base_template", None)
                if base_template1 == base_template2:
                    # Partial loading is possible.
                    attrs["onclick"] = "hypergen.callback('{}', [], {{'event': event}})".format(href)

        super(a, self).__init__(*children, **attrs)

class abbr(base_element): pass
class acronym(base_element): pass
class address(base_element): pass
class applet(base_element): pass
class area(base_element_void): pass
class article(base_element): pass
class aside(base_element): pass
class audio(base_element): pass
class b(base_element): pass
class base(base_element_void): pass
class basefont(base_element): pass
class bdi(base_element): pass
class bdo(base_element): pass
class big(base_element): pass
class blockquote(base_element): pass
class body(base_element): pass
class br(base_element_void): pass
class button(base_element): pass
class canvas(base_element): pass
class caption(base_element): pass
class center(base_element): pass
class cite(base_element): pass
class code(base_element): pass
class col(base_element_void): pass
class colgroup(base_element): pass
class data(base_element): pass
class datalist(base_element): pass
class dd(base_element): pass
class del_(base_element): pass
class details(base_element): pass
class dfn(base_element): pass
class dialog(base_element): pass
class dir_(base_element): pass
class div(base_element): pass
class dl(base_element): pass
class dt(base_element): pass
class em(base_element): pass
class embed(base_element_void): pass
class fieldset(base_element): pass
class figcaption(base_element): pass
class figure(base_element): pass
class font(base_element): pass
class footer(base_element): pass
class form(base_element): pass
class frame(base_element): pass
class frameset(base_element): pass
class h1(base_element): pass
class h2(base_element): pass
class h3(base_element): pass
class h4(base_element): pass
class h5(base_element): pass
class h6(base_element): pass
class head(base_element): pass
class header(base_element): pass
class hr(base_element_void): pass
class html(base_element): pass
class i(base_element): pass
class iframe(base_element): pass
class img(base_element_void): pass
class ins(base_element): pass
class kbd(base_element): pass
class label(base_element): pass
class legend(base_element): pass
class li(base_element): pass

class link(base_element):
    def __init__(self, href, rel="stylesheet", type_="text/css", **attrs):
        attrs["href"] = href
        super(link, self).__init__(rel=rel, type_=type_, **attrs)

class main(base_element): pass
class map_(base_element): pass
class mark(base_element): pass
class meta(base_element_void): pass
class meter(base_element): pass
class nav(base_element): pass
class noframes(base_element): pass
class noscript(base_element): pass
class object_(base_element): pass
class ol(base_element): pass
class optgroup(base_element): pass
class option(base_element): pass
class output(base_element): pass
class p(base_element): pass
class param(base_element_void): pass
class picture(base_element): pass
class pre(base_element): pass
class progress(base_element): pass
class q(base_element): pass
class rp(base_element): pass
class rt(base_element): pass
class ruby(base_element): pass
class s(base_element): pass
class samp(base_element): pass

class script(base_element):
    def __init__(self, *children, **attrs):
        attrs["t"] = lambda x, **kwargs: x
        super(script, self).__init__(*children, **attrs)

class section(base_element): pass
class select(base_element): pass
class small(base_element): pass
class source(base_element_void): pass
class span(base_element): pass
class strike(base_element): pass
class strong(base_element): pass

class style(base_element):
    def __init__(self, *children, **attrs):
        attrs["t"] = lambda x, **kwargs: x
        super(style, self).__init__(*children, **attrs)

class sub(base_element): pass
class summary(base_element): pass
class sup(base_element): pass
class svg(base_element): pass
class table(base_element): pass
class tbody(base_element): pass
class td(base_element): pass
class template(base_element): pass
class textarea(base_element): pass
class tfoot(base_element): pass
class th(base_element): pass
class thead(base_element): pass
class time_(base_element): pass
class title(base_element): pass
class tr(base_element): pass
class track(base_element_void): pass
class tt(base_element): pass
class u(base_element): pass
class ul(base_element): pass
class var(base_element): pass
class video(base_element): pass
class wbr(base_element_void): pass
# yapf: enable

### Context ###

class Context(threading.local):
    def __init__(self):
        self.ctx = pmap()
        super(Context, self).__init__()

    def replace(self, **items):
        self.ctx = m(**items)

    def __getattr__(self, k):
        try:
            return self.__dict__['ctx'][k]
        except KeyError:
            raise AttributeError("No such attribute: " + k)

    def __setattr__(self, k, v):
        if k == "ctx":
            return super(Context, self).__setattr__(k, v)
        else:
            self.ctx = self.ctx.set(k, v)

    def __getitem__(self, k):
        return self.__dict__['ctx'][k]

    def __setitem__(self, k, v):
        raise Exception("TODO")

    def __contains__(self, k):
        return k in self.ctx

    @contextmanager
    def __call__(self, transformer=None, at=None, **items):
        try:
            # Store previous value.
            ctx = self.ctx
            if at is None:
                if transformer is not None:
                    self.ctx = transformer(self.ctx)
                self.ctx = self.ctx.update(m(**items))
            else:
                if at not in self.ctx:
                    self.ctx = self.ctx.set(at, pmap(items))
                else:
                    new_value_at = self.ctx[at].update(pmap(items))
                    if not new_value_at:
                        raise Exception("Not immutable context variable attempted updated. If you want to nest "
                            "with context() statements you must use a pmap() or another immutable hashmap type.")

                    self.ctx = self.ctx.set(at, new_value_at)

                if transformer is not None:
                    self.ctx = self.ctx.set(at, transformer(self.ctx[at]))

            yield
        finally:
            # Reset to previous value.
            self.ctx = ctx

context = Context()
c = context

def _init_context(request):
    return dict(user=request.user, request=request)

def context_middleware(get_response):
    def _(request):
        with context(**_init_context(request)):
            return get_response(request)

    return _

class ContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        context.replace(**_init_context(request))
