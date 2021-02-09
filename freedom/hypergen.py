# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)
d = dict

import string, sys, time
from collections import OrderedDict
from functools import partial
from copy import deepcopy
from types import GeneratorType
from functools import wraps
from collections import namedtuple

from contextlib2 import ContextDecorator
from pyrsistent import m

from django.urls.base import reverse_lazy
from django.http.response import HttpResponse
from django.utils.encoding import force_text

import freedom
from freedom.utils import insert
from freedom.core import context as c

### Python 2+3 compatibility ###


def make_string(x):
    if x is not None:
        return force_text(x)
    else:
        return ""


if sys.version_info.major > 2:
    from html import escape
    letters = string.ascii_letters

    def items(x):
        return x.items()
else:
    from cgi import escape
    letters = string.letters
    str = make_string

    def items(x):
        return x.iteritems()


### Rendering ###
def hypergen_context(**kwargs):
    return m(
        into=[],
        liveview=True,
        id_counter=base65_counter(),
        id_prefix=(freedom.loads(c.request.body)["id_prefix"]
                   if c.request.is_ajax() else ""),
        event_handler_cache={},
        target_id=kwargs.get("target_id", "__main__"),
        commands=[],
        collection={}, )


def hypergen(func, *args, **kwargs):
    a = time.time()
    kwargs = deepcopy(kwargs)
    target_id = kwargs.pop("target_id", "__main__")
    with c(hypergen=hypergen_context(target_id=target_id, **kwargs)):
        func(*args, **kwargs)
        html = join_html(c.hypergen.into)
        if c.hypergen.event_handler_cache:
            command("freedom.setEventHandlerCache", c.hypergen.target_id,
                    c.hypergen.event_handler_cache)
        if not c.request.is_ajax():
            pos = html.find("</head")
            if pos != -1:
                s = '<script>$(() => window.applyCommands({}))</script>'.format(
                    freedom.dumps(c.hypergen.commands))
                html = insert(html, s, pos)
            print "Execution time:", time.time() - a
            return HttpResponse(html)
        else:
            command("freedom.morph", c.hypergen.target_id, html)
            print "Execution time:", time.time() - a
            return c.hypergen.commands


def command(javascript_func_path, *args, **kwargs):
    prepend = kwargs.pop("prepend", False)
    return_ = kwargs.pop("return_", False)
    item = [javascript_func_path] + list(args) + [kwargs]
    if return_:
        return item
    elif prepend:
        c.hypergen.commands.insert(0, item)
    else:
        c.hypergen.commands.append(item)


### Helpers ###


class LazyAttribute(object):
    def __init__(self, k, v):
        self.k = k
        self.v = v

    def __str__(self):
        if not self.v:
            return ""
        else:
            return ' {}="{}"'.format(self.k, t(self.v))

    def __unicode__(self):
        return self.__str__()


def join(*values):
    return "".join(str(x) for x in values)


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

    return "".join(str(x) for x in fmt(html))


def raw(*children):
    c.hypergen.into.extend(children)


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


### Callbacks ###
def callback_attribute(k, data_id):
    return join(" ", k, '="', "e('{}',{})".format(c.hypergen.target_id,
                                                  data_id), '"')


def add_callback(cb_func, element, cb_args, cb_kwargs, event_handler_config):
    def fix_this(x):
        return element if x is THIS else x

    element.ensure_id()
    cmd = command(
        "freedom.callback",
        cb_func.hypergen_callback_url, [fix_this(x) for x in cb_args],
        cb_kwargs,
        event_handler_config,
        return_=True)
    cmd_id = id(cmd)
    c.hypergen.event_handler_cache[cmd_id] = cmd
    return cmd_id


def defer_callback(cb_func):
    assert hasattr(cb_func, "hypergen_callback_url"), "Not a callback func"

    @wraps(cb_func)
    def f1(*cb_args, **cb_kwargs):
        # TODO: Add default todos per attribute_keys.
        event_handler_config = d(debounce=cb_kwargs.pop("debounce", 0))

        def f2(element, attribute_key):
            return add_callback(cb_func, element, cb_args, cb_kwargs,
                                event_handler_config)

        return f2

    return f1


def callback(func):
    """
    Makes a function a callback for django.
    """
    if "is_test" in c:
        func.hypergen_callback_url = "/path/to/{}/".format(func.__name__)
    else:
        func.hypergen_callback_url = reverse_lazy(
            "freedom:callback",
            args=[".".join((func.__module__, func.__name__))])

    func.hypergen_is_callback = True
    func.actual_func = func

    return defer_callback(func)


### Base dom element ###
class THIS(object):
    pass


NON_SCALARS = set((list, dict, tuple))
DELETED = ""


class base_element(ContextDecorator):
    js_cb = "freedom.v.s"
    void = False
    auto_id = False
    auto_collect = False

    def __new__(cls, *args, **kwargs):
        instance = ContextDecorator.__new__(cls)
        setattr(instance, "tag", cls.__name__.rstrip("_"))
        return instance

    def __init__(self, *children, **attrs):
        assert "hypergen" in c, "Missing global context: hypergen"
        self.children = children
        self.attrs = attrs
        self.attrs["id_"] = LazyAttribute("id", self.attrs.get("id_", None))
        self.i = len(c.hypergen.into)
        self.sep = attrs.pop("sep", "")
        collect_name = attrs.pop("collect_name", attrs.get("id_", None))

        self.delete_children(self.children)
        c.hypergen.into.extend(self.start())
        c.hypergen.into.extend(self.end())
        self.j = len(c.hypergen.into)
        if self.auto_collect:
            if type(c.hypergen.collection) is dict:
                if collect_name is not None:
                    c.hypergen.collection[collect_name] = self
            elif type(c.hypergen.collection) is list:
                c.hypergen.collection.append(self)

        super(base_element, self).__init__()

    def __enter__(self):
        c.hypergen.into.extend(self.start())
        self.delete()
        return self

    def __exit__(self, *exc):
        if not self.void:
            c.hypergen.into.extend(self.end())

    def as_string(self):
        into = self.start()
        into.extend(self.end())
        s = join_html(into)
        return s

    def delete(self):
        for i in range(self.i, self.j):
            c.hypergen.into[i] = DELETED

    def delete_children(self, children):
        children = list(children)
        for i in range(0, len(children)):
            child = children[i]
            if issubclass(type(child), base_element):
                child.delete()
            elif type(child) in (list, tuple):
                self.delete_children(child)

    def format_children(self, children, _t=t):
        into = []
        sep = t(self.sep)

        for x in children:
            if x in ("", None):
                continue
            elif issubclass(type(x), base_element):
                into.append(x)
            elif type(x) in (list, tuple):
                into.extend(self.format_children(list(x), _t=_t))
            elif type(x) in (GeneratorType, ):
                into.append(x)
            elif callable(x):
                into.append(x)
            elif type(x) is Component:
                x.delete()
                into.extend(x.into)
            else:
                into.append(_t(x))
            if sep:
                into.append(sep)
        if sep and children:
            into.pop()

        return into

    def ensure_id(self):
        if self.attrs["id_"].v is None:
            self.attrs[
                "id_"].v = c.hypergen.id_prefix + next(c.hypergen.id_counter)

    def attribute(self, k, v):
        k = t(k).rstrip("_").replace("_", "-")
        if c.hypergen.liveview is True and callable(v):
            data_id = v(self, k)
            return [callback_attribute(k, data_id)]
        elif c.hypergen.liveview is True and k.startswith("on") and type(
                v) in (list, tuple):
            data_id = add_callback(v[0], self, v[1:], {}, {})
            return [callback_attribute(k, data_id)]
        elif type(v) is LazyAttribute:
            return [v]
        elif type(v) is bool:
            if v is True:
                return [join(" ", k)]
            else:
                return []
        elif k == "style" and type(v) in (dict, OrderedDict):
            return [
                join(" ", k, '="', ";".join(
                    t(k1.replace("_", "-")) + ":" + t(v1)
                    for k1, v1 in items(v)), '"')
            ]
        else:
            return [join(" ", k, '="', t(v), '"')]

    def start(self):
        into = ["<", self.tag]
        for k, v in items(self.attrs):
            into.extend(self.attribute(k, v))

        if self.void:
            into.append(join(("/")))
        into.append(join('>', ))
        into.extend(self.format_children(self.children))
        return into

    def end(self):
        if not self.void:
            return ["</{}>".format(self.tag)]
        else:
            return [""]


class base_element_void(base_element):
    void = True


class Component(object):
    def __init__(self, into, i, j):
        self.into = into
        self.i = i
        self.j = j

    def delete(self):
        for i in range(self.i, self.j):
            c.hypergen.into[i] = DELETED


def component(f):
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

INPUT_CALLBACK_TYPES = dict(
    checkbox="freedom.v.c",
    month="freedom.v.i",
    number="freedom.v.i",
    range="freedom.v.f",
    week="freedom.v.i")


class input_(base_element_void):
    void = True
    auto_collect = True

    def __init__(self, *children, **attrs):
        self.js_cb = INPUT_CALLBACK_TYPES.get(
            attrs.get("type_", "text"), "freedom.v.s")
        super(input_, self).__init__(*children, **attrs)


### Special tags ###


def doctype(type_="html"):
    raw("<!DOCTYPE ", type_, ">")


### GENERATED BY build.py ###
# yapf: disable
class a(base_element): pass
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
class script(base_element): pass
class section(base_element): pass
class select(base_element): pass
class small(base_element): pass
class source(base_element_void): pass
class span(base_element): pass
class strike(base_element): pass
class strong(base_element): pass
class style(base_element): pass
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
