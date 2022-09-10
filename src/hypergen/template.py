d = dict
from hypergen.context import context as c, contextlist
from hypergen.hypergen import *
from hypergen.hypergen import make_string, t
from hypergen.plugins.appstate import AppstatePlugin

import time, logging
from collections import OrderedDict
from types import GeneratorType
from functools import wraps
from copy import deepcopy
from contextlib import ContextDecorator, contextmanager, ExitStack
from datetime import datetime

from pyrsistent import m
from django.http.response import HttpResponse

try:
    import docutils.core
    docutils_ok = True
except ImportError:
    docutils_ok = False

try:
    from yattag import indent as indent_
    yattag_ok = True
except ImportError:
    yattag_ok = False

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
    "tt", "u", "ul", "var", "video", "wbr", "component", "hypergen", "raw", "write", "rst", "hprint", "HTML", "FULL",
    "COMMANDS", "OMIT", "hypergen_to_response"]

### Constants ###

OMIT = "__OMIT__"

### Utility functions ###

def add_class(a, b):
    assert type(b) is str, "b must be string for now. PR?"
    if a in ("", OMIT, None):
        return b
    elif type(a) is str:
        return a.strip() + " " + b
    elif is_collection(a):
        if hasattr(a, "append"):
            a.append(b)
            return a
        elif hasattr(a, "add"):
            a.add(b)
            return a
        else:
            raise Exception("This class collection has neither an append() or add() method. Help!")
    else:
        raise Exception("I don't know how to add these variables together in the context of classes.")

### template itself is a plugin to hypergen ###

class TemplatePlugin:
    @contextmanager
    def context(self):
        with c(at="hypergen", into=contextlist("target_id"), ids=set()):
            yield

### Rendering ###

HTML = "HTML"
FULL = "FULL"
COMMANDS = "COMMANDS"
HYPERGEN_RETURNS = {HTML, FULL, COMMANDS}

def hypergen(template, *args, **kwargs):
    assert "request" in c, "The 'hypergen.context.context_middleware' Middleware must be installed!"
    settings = kwargs.pop("settings", {})

    plugins = settings.get("plugins", [TemplatePlugin()])
    if settings.get("liveview", False):
        from hypergen.liveview import LiveviewPlugin
        plugins.append(LiveviewPlugin())
    if settings.get("action", False):
        from hypergen.liveview import ActionPlugin
        plugins.append(
            ActionPlugin(
            target_id=settings.get("target_id", None),
            base_view=settings.get("base_view", None),
            prepend_commands=settings.get("prepend_commands", True),
            ))
    if settings.get("appstate", False):
        namespace = settings.get("namespace", None)
        assert namespace, "When appstate is set, namespace must be too."
        plugins.append(AppstatePlugin(namespace, settings["appstate"]))

    returns = settings.get("returns", HTML)
    assert returns in HYPERGEN_RETURNS, "The 'returns' hypergen setting must be one of {}".format(
        repr(HYPERGEN_RETURNS))
    indent = settings.get("indent", False)
    base_template = settings.get("base_template", None)

    plugins.extend(settings.get("user_plugins", []))
    with c(at="hypergen", plugins=plugins, base_template=base_template):
        with plugins_exit_stack("context"):
            plugins_method_call("template_before")
            template_result = (base_template()(template) if base_template else template)(*args, **kwargs)
            plugins_method_call("template_after", template_result=template_result)

            html = join_html(c.hypergen.into) if "into" in c.hypergen else ""
            html = plugins_pipeline("process_html", html)

            if indent:
                if not yattag_ok:
                    raise Exception("Do 'pip install yattag' to use the indent feature.")
                html = indent_(html, indentation='    ', newline='\n', indent_text=True)

            if returns == HTML:
                return html
            elif returns == COMMANDS:
                return c.hypergen.commands
            elif returns == FULL:
                return d(html=html, context=c.clone(), template_result=template_result)

def hypergen_to_response(func, *args, **kwargs):
    return HttpResponse(hypergen(func, *args, **kwargs))

### Helpers ###
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

def rst(restructured_text, report_level=docutils.utils.Reporter.SEVERE_LEVEL + 1 if docutils_ok else None):
    if not docutils_ok:
        raise Exception("Please 'pip install docutils' to use the rst() function.")
    raw(
        docutils.core.publish_parts(restructured_text, writer_name="html",
        settings_overrides={'_disable_config': True, 'report_level': report_level})["html_body"])

def hprint(*args, **kwargs):
    # TODO: Make custom support for:
    #           - Queryset
    #           - values and values_list
    #           - query (sql)
    #           - grouper
    from pprint import pformat
    d = dict

    @component
    def typeinfo(x):
        span(" (", x.__class__.__module__, ".", type(x).__name__, ")", style=d(color="darkgrey"))

    def fmt(x):
        pre(code(pformat(x, width=120)), style=d())

    with div(style=d(padding="8px", margin="4px 0 0 0", background="#ffc", color="black", font_family="sans-serif")):
        if len(args) == 1 and not kwargs:
            div(typeinfo(args[0]))
            fmt(args[0])
        else:
            for i, arg in enumerate(args, 1):
                div(b("arg", i, sep=" "), typeinfo(arg))
                fmt(arg)

        for k, v in kwargs.items():
            div(b(k), typeinfo(v))
            fmt(v)

### Base dom element ###
DELETED = ""

class base_element(ContextDecorator):
    void = False
    auto_id = False

    def __new__(cls, *args, **kwargs):
        instance = ContextDecorator.__new__(cls)
        setattr(instance, "tag", cls.__name__.rstrip("_"))
        return instance

    def __init__(self, *children, **attrs):
        with ExitStack() as stack:
            [
                stack.enter_context(plugin.wrap_element_init(self, children, attrs)) for plugin in c.hypergen.plugins
                if hasattr(plugin, "wrap_element_init")]

            assert "hypergen" in c, "Element called outside hypergen context."

            self.t = attrs.pop("t", t)
            self.children = children
            self.attrs = attrs
            self.sep = attrs.pop("sep", "")
            self.end_char = attrs.pop("end", None)

            # Id
            id_ = self.attrs.get("id_", self.attrs.pop("id", None))
            if type(id_) in (tuple, list):
                id_ = "-".join(str(x) for x in id_)
            self.attrs["id_"] = id_

            # Make sure ids are unique
            if id_ is not None:
                assert id_ not in c.hypergen["ids"], "Duplicate id: {}".format(id_)
                c.hypergen["ids"].add(id_)

            # Render and save position in into.
            self.i = len(c.hypergen.into)
            c.hypergen.into.extend(self.start())
            c.hypergen.into.extend(self.end())
            self.j = len(c.hypergen.into)

            super(base_element, self).__init__()

    def __enter__(self):
        c.hypergen.into.extend(self.start())
        self.delete()
        return self

    def __exit__(self, *exc):
        if not self.void:
            c.hypergen.into.extend(self.end())

    def __repr__(self):
        from hypergen.liveview import THIS

        def value(v):
            if v is THIS:
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
            return ", ".join([args(x)
                for x in a] + ["{}={}".format(*kwargs(k, v)) for k, v in list(kw.items()) if v is not None])

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
                into.append(self.t(x))
            if sep:
                into.append(sep)
        if sep and children:
            into.pop()

        if self.end_char and not nested:
            into.append(self.t(self.end_char))

        return into

    def ensure_id(self):
        assert self.attrs["id_"] is not None, "This element needs an id_='myid' attribute: {}".format(repr(self))

    def attribute(self, k, v):
        k = t(k).rstrip("_").replace("_", "-")
        if v == OMIT or v is None:
            return []
        elif callable(v):
            return v(self, k, v)
        elif type(v) is bool:
            if v is True:
                return [" ", k]
            else:
                return []
        elif k == "style" and type(v) in (dict, OrderedDict):
            return [" ", k, '="', ";".join(t(k1.replace("_", "-")) + ":" + t(v1) for k1, v1 in v.items()), '"']
        elif k == "class" and type(v) in (list, tuple, set):
            return [" ", k, '="', t(" ".join(v)), '"']
        else:
            if v is None:
                v = ""
            else:
                v = t(v)
            assert '"' not in v, "How dare you put a \" in my attributes! :)"
            return [" ", k, '="', v, '"']

    def start(self):
        cache = getattr(self, "_start_cache", None)
        if cache:
            return cache

        into = ["<", self.tag]
        for k, v in self.attrs.items():
            into.extend(self.attribute(k, v))

        if self.void:
            into.append("/")
        into.append('>')
        into.extend(self.format_children(self.children))

        self._start_cache = into

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
    @wraps(f)
    def _(*args, **kwargs):
        with c(into=contextlist("target_id"), at="hypergen"):
            f(*args, **kwargs)
            into = c.hypergen.into
        i = len(c.hypergen.into)
        c.hypergen.into.extend(into)
        j = len(c.hypergen.into)
        return Component(into, i, j)

    return _

### Some special dom elements ###

class input_(base_element_void):
    void = True

    def __init__(self, *children, **attrs):
        type_ = attrs.get("type_", attrs.pop("type", None))
        if type_:
            attrs["type_"] = type_
        if type_ == "radio":
            assert attrs.get("name"), "Name must be set for radio buttons."
        super(input_, self).__init__(*children, **attrs)

    def attribute(self, k, v):
        if k != "value":
            return super().attribute(k, v)

        type_ = self.attrs.get("type_", None)
        if type_ == "datetime-local" and type(v) is datetime:
            return [" ", k, '="', v.strftime("%Y-%m-%dT%H:%M:%S"), '"']
        elif type_ == "month" and type(v) is dict:
            return [" ", k, '="', "{:04}-{:02}".format(v["year"], v["month"]), '"']
        elif type_ == "week" and type(v) is dict:
            return [" ", k, '="', "{:04}-W{:02}".format(v["year"], v["week"]), '"']
        else:
            return super().attribute(k, v)

class a(base_element):
    def __init__(self, *children, **attrs):
        class_active, href = attrs.pop("class_active", None), attrs.get("href", None)
        if class_active and href:
            from hypergen.liveview import url_is_active
            if url_is_active(href):
                attrs["class"] = add_class(attrs.get("class"), class_active)

        super(a, self).__init__(*children, **attrs)

def doctype(type_="html"):
    raw("<!DOCTYPE ", type_, ">")

### All the tags ###
# yapf: disable
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
    def __init__(self, href=OMIT, rel="stylesheet", **attrs):
        type_ = attrs.get("type_", attrs.pop("type", "text/css"))
        attrs["type_"] = type_
        attrs["href"] = href
        super(link, self).__init__(rel=rel, **attrs)

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
class wbr(base_element_void):
    pass
# yapf: enable
