d = dict
from hypergen.context import context as c
from hypergen.utils import *
from hypergen.hypergen import *
from hypergen.hypergen import make_string, t

import time, logging
from collections import OrderedDict
from types import GeneratorType
from functools import wraps
from copy import deepcopy
from contextlib import ContextDecorator, contextmanager, ExitStack

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
    "tt", "u", "ul", "var", "video", "wbr", "component", "hypergen", "hypergen_to_response", "raw", "write", "rst",
    "TemplatePlugin", "HTML", "FULL", "COMMANDS", "base_element"]

### template itself is a plugin to hypergen ###
class TemplatePlugin:
    @contextmanager
    def context(self):
        with c(at="hypergen", into=[], ids=set()):
            yield

### Rendering ###

HTML = "HTML"
FULL = "FULL"
COMMANDS = "COMMANDS"
HYPERGEN_RETURNS = {HTML, FULL, COMMANDS}

def hypergen(func, *args, **kwargs):
    assert "request" in c, "The 'hypergen.context.context_middleware' Middleware must be installed!"
    settings = kwargs.pop("hypergen", {})

    plugins = settings.get("plugins", [TemplatePlugin()])
    if settings.get("liveview", False):
        from hypergen.liveview import LiveviewPlugin
        plugins.append(LiveviewPlugin())
    if settings.get("callback", False):
        from hypergen.liveview import CallbackPlugin
        plugins.append(CallbackPlugin(target_id=settings.get("target_id", None)))

    returns = settings.get("returns", HTML)
    assert returns in HYPERGEN_RETURNS, "The 'returns' hypergen setting must be one of {}".format(
        repr(HYPERGEN_RETURNS))
    indent = settings.get("indent", False)
    base_template = settings.get("base_template", None)

    with c(at="hypergen", plugins=plugins, base_template=base_template):
        with ExitStack() as stack:
            [stack.enter_context(plugin.context()) for plugin in c.hypergen.plugins if hasattr(plugin, "context")]
            func_result = (base_template()(func) if base_template else func)(*args, **kwargs)

            html = join_html(c.hypergen.into) if "into" in c.hypergen else ""

            for plugin in c.hypergen.plugins:
                if not hasattr(plugin, "process_html"):
                    continue
                html = plugin.process_html(html)

            if indent:
                if not yattag_ok:
                    raise Exception("Do 'pip install yattag' to use the indent feature.")
                html = indent_(html, indentation='    ', newline='\n', indent_text=True)

            if returns == HTML:
                return html
            elif returns == COMMANDS:
                return c.hypergen.commands
            elif returns == FULL:
                return d(html=html, context=c.clone(), func_result=func_result)

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

def rst(restructured_text, report_level=docutils.utils.Reporter.SEVERE_LEVEL + 1):
    if not docutils_ok:
        raise Exception("Please 'pip install docutils' to use the rst() function.")
    raw(
        docutils.core.publish_parts(restructured_text, writer_name="html",
        settings_overrides={'_disable_config': True, 'report_level': report_level})["html_body"])

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

            id_ = self.attrs.get("id_", None)
            if type(id_) in (tuple, list):
                id_ = "-".join(str(x) for x in id_)
            self.attrs["id_"] = LazyAttribute("id", id_)

            self.i = len(c.hypergen.into)
            self.sep = attrs.pop("sep", "")
            self.end_char = attrs.pop("end", None)

            c.hypergen.into.extend(self.start())
            c.hypergen.into.extend(self.end())
            self.j = len(c.hypergen.into)

            super(base_element, self).__init__()

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
            # TODO: plugin
            # elif v is THIS:
            #     return "THIS"
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
                into.append(self.t(x))
            if sep:
                into.append(sep)
        if sep and children:
            into.pop()

        if self.end_char and not nested:
            into.append(self.t(self.end_char))

        return into

    def ensure_id(self):
        assert self.attrs["id_"].v is not None, "This element needs an id_='myid' attribute: {}".format(repr(self))

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
        into = ["<", self.tag]
        for k, v in self.attrs.items():
            into.extend(self.attribute(k, v))

        if self.void:
            into.append("/")
        into.append('>')
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

class input_(base_element_void):
    void = True

    def __init__(self, *children, **attrs):
        if attrs.get("type_", None) == "radio":
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

### Special tags ###
def doctype(type_="html"):
    raw("<!DOCTYPE ", type_, ">")

### All the tags ###
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
    def __init__(self, href=OMIT, rel="stylesheet", type_="text/css", **attrs):
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
class wbr(base_element_void):
    pass
# yapf: enable