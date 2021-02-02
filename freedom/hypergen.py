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


def element_start(tag,
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


def element(tag,
            children,
            lazy=False,
            into=None,
            void=False,
            sep="",
            add_to=None,
            **attrs):
    blob = element_start(
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


def element_ret(tag,
                children,
                lazy=False,
                into=None,
                void=False,
                sep="",
                add_to=None,
                **attrs):
    into = Blob()
    element(
        tag,
        children,
        lazy=lazy,
        into=into,
        void=void,
        sep="",
        add_to=add_to,
        **attrs)

    return into


def element_end(tag, children, into=None, sep="", void=False):
    if void is False:
        write(*children, into=into, sep=sep)
        raw(("</", t(tag), ">"), into=into)


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
DELETED = ""


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
            print "AAAA", repr(arg)
        else:
            print "BBB", repr(arg)
            args2.append(arg)

    return "H.cb({})".format(
        freedom.dumps(
            [func.hypergen_callback_url] + list(args2),
            unquote=True,
            escape=True,
            this=this))


class base_element(ContextDecorator):
    js_cb = "H.cbs.s"
    void = False

    def __init__(self, *children, **attrs):
        self.children = children
        self.attrs = attrs
        self.i = len(state.html)
        for child in children:
            if issubclass(type(child), base_element):
                state.html[child.i] = DELETED

        state.html.append(
            lambda: element_ret(self.tag, children, js_cb=self.js_cb, void=self.void, **attrs))
        super(base_element, self).__init__()

    def __enter__(self):
        element_start(
            self.tag,
            self.children,
            js_cb=self.js_cb,
            void=self.void,
            **self.attrs)
        state.html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        return element_end(self.tag, [])

    def __str__(self):

        blob = element_ret(
            self.tag,
            self.children,
            js_cb=self.js_cb,
            void=self.void,
            **self.attrs)
        return "".join(blob.html)

    def __unicode__(self):
        return self.__str__()


### Input ###

INPUT_TYPES = dict(
    checkbox="H.cbs.c",
    month="H.cbs.i",
    number="H.cbs.i",
    range="H.cbs.f",
    week="H.cbs.i")


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




class a(base_element):
    tag = "a"


a.r = a
a.c = a
a.d = a





class abbr(base_element):
    tag = "abbr"


abbr.r = abbr
abbr.c = abbr
abbr.d = abbr





class acronym(base_element):
    tag = "acronym"


acronym.r = acronym
acronym.c = acronym
acronym.d = acronym





class address(base_element):
    tag = "address"


address.r = address
address.c = address
address.d = address





class applet(base_element):
    tag = "applet"


applet.r = applet
applet.c = applet
applet.d = applet





class article(base_element):
    tag = "article"


article.r = article
article.c = article
article.d = article





class aside(base_element):
    tag = "aside"


aside.r = aside
aside.c = aside
aside.d = aside





class audio(base_element):
    tag = "audio"


audio.r = audio
audio.c = audio
audio.d = audio





class b(base_element):
    tag = "b"


b.r = b
b.c = b
b.d = b





class basefont(base_element):
    tag = "basefont"


basefont.r = basefont
basefont.c = basefont
basefont.d = basefont





class bdi(base_element):
    tag = "bdi"


bdi.r = bdi
bdi.c = bdi
bdi.d = bdi





class bdo(base_element):
    tag = "bdo"


bdo.r = bdo
bdo.c = bdo
bdo.d = bdo





class big(base_element):
    tag = "big"


big.r = big
big.c = big
big.d = big





class blockquote(base_element):
    tag = "blockquote"


blockquote.r = blockquote
blockquote.c = blockquote
blockquote.d = blockquote





class body(base_element):
    tag = "body"


body.r = body
body.c = body
body.d = body





class button(base_element):
    tag = "button"


button.r = button
button.c = button
button.d = button





class canvas(base_element):
    tag = "canvas"


canvas.r = canvas
canvas.c = canvas
canvas.d = canvas





class caption(base_element):
    tag = "caption"


caption.r = caption
caption.c = caption
caption.d = caption





class center(base_element):
    tag = "center"


center.r = center
center.c = center
center.d = center





class cite(base_element):
    tag = "cite"


cite.r = cite
cite.c = cite
cite.d = cite





class code(base_element):
    tag = "code"


code.r = code
code.c = code
code.d = code





class colgroup(base_element):
    tag = "colgroup"


colgroup.r = colgroup
colgroup.c = colgroup
colgroup.d = colgroup





class data(base_element):
    tag = "data"


data.r = data
data.c = data
data.d = data





class datalist(base_element):
    tag = "datalist"


datalist.r = datalist
datalist.c = datalist
datalist.d = datalist





class dd(base_element):
    tag = "dd"


dd.r = dd
dd.c = dd
dd.d = dd





class del_(base_element):
    tag = "del"


del_.r = del_
del_.c = del_
del_.d = del_





class details(base_element):
    tag = "details"


details.r = details
details.c = details
details.d = details





class dfn(base_element):
    tag = "dfn"


dfn.r = dfn
dfn.c = dfn
dfn.d = dfn





class dialog(base_element):
    tag = "dialog"


dialog.r = dialog
dialog.c = dialog
dialog.d = dialog





class dir_(base_element):
    tag = "dir"


dir_.r = dir_
dir_.c = dir_
dir_.d = dir_





class dl(base_element):
    tag = "dl"


dl.r = dl
dl.c = dl
dl.d = dl





class dt(base_element):
    tag = "dt"


dt.r = dt
dt.c = dt
dt.d = dt





class em(base_element):
    tag = "em"


em.r = em
em.c = em
em.d = em





class fieldset(base_element):
    tag = "fieldset"


fieldset.r = fieldset
fieldset.c = fieldset
fieldset.d = fieldset





class figcaption(base_element):
    tag = "figcaption"


figcaption.r = figcaption
figcaption.c = figcaption
figcaption.d = figcaption





class figure(base_element):
    tag = "figure"


figure.r = figure
figure.c = figure
figure.d = figure





class font(base_element):
    tag = "font"


font.r = font
font.c = font
font.d = font





class footer(base_element):
    tag = "footer"


footer.r = footer
footer.c = footer
footer.d = footer





class form(base_element):
    tag = "form"


form.r = form
form.c = form
form.d = form





class frame(base_element):
    tag = "frame"


frame.r = frame
frame.c = frame
frame.d = frame





class frameset(base_element):
    tag = "frameset"


frameset.r = frameset
frameset.c = frameset
frameset.d = frameset





class h1(base_element):
    tag = "h1"


h1.r = h1
h1.c = h1
h1.d = h1





class h2(base_element):
    tag = "h2"


h2.r = h2
h2.c = h2
h2.d = h2





class h3(base_element):
    tag = "h3"


h3.r = h3
h3.c = h3
h3.d = h3





class h4(base_element):
    tag = "h4"


h4.r = h4
h4.c = h4
h4.d = h4





class h5(base_element):
    tag = "h5"


h5.r = h5
h5.c = h5
h5.d = h5





class h6(base_element):
    tag = "h6"


h6.r = h6
h6.c = h6
h6.d = h6





class head(base_element):
    tag = "head"


head.r = head
head.c = head
head.d = head





class header(base_element):
    tag = "header"


header.r = header
header.c = header
header.d = header





class html(base_element):
    tag = "html"


html.r = html
html.c = html
html.d = html





class i(base_element):
    tag = "i"


i.r = i
i.c = i
i.d = i





class iframe(base_element):
    tag = "iframe"


iframe.r = iframe
iframe.c = iframe
iframe.d = iframe





class ins(base_element):
    tag = "ins"


ins.r = ins
ins.c = ins
ins.d = ins





class kbd(base_element):
    tag = "kbd"


kbd.r = kbd
kbd.c = kbd
kbd.d = kbd





class label(base_element):
    tag = "label"


label.r = label
label.c = label
label.d = label





class legend(base_element):
    tag = "legend"


legend.r = legend
legend.c = legend
legend.d = legend





class li(base_element):
    tag = "li"


li.r = li
li.c = li
li.d = li





class main(base_element):
    tag = "main"


main.r = main
main.c = main
main.d = main





class map_(base_element):
    tag = "map"


map_.r = map_
map_.c = map_
map_.d = map_





class mark(base_element):
    tag = "mark"


mark.r = mark
mark.c = mark
mark.d = mark





class meter(base_element):
    tag = "meter"


meter.r = meter
meter.c = meter
meter.d = meter





class nav(base_element):
    tag = "nav"


nav.r = nav
nav.c = nav
nav.d = nav





class noframes(base_element):
    tag = "noframes"


noframes.r = noframes
noframes.c = noframes
noframes.d = noframes





class noscript(base_element):
    tag = "noscript"


noscript.r = noscript
noscript.c = noscript
noscript.d = noscript





class object_(base_element):
    tag = "object"


object_.r = object_
object_.c = object_
object_.d = object_





class ol(base_element):
    tag = "ol"


ol.r = ol
ol.c = ol
ol.d = ol





class optgroup(base_element):
    tag = "optgroup"


optgroup.r = optgroup
optgroup.c = optgroup
optgroup.d = optgroup





class option(base_element):
    tag = "option"


option.r = option
option.c = option
option.d = option





class output(base_element):
    tag = "output"


output.r = output
output.c = output
output.d = output





class p(base_element):
    tag = "p"


p.r = p
p.c = p
p.d = p





class picture(base_element):
    tag = "picture"


picture.r = picture
picture.c = picture
picture.d = picture





class pre(base_element):
    tag = "pre"


pre.r = pre
pre.c = pre
pre.d = pre





class progress(base_element):
    tag = "progress"


progress.r = progress
progress.c = progress
progress.d = progress





class q(base_element):
    tag = "q"


q.r = q
q.c = q
q.d = q





class rp(base_element):
    tag = "rp"


rp.r = rp
rp.c = rp
rp.d = rp





class rt(base_element):
    tag = "rt"


rt.r = rt
rt.c = rt
rt.d = rt





class ruby(base_element):
    tag = "ruby"


ruby.r = ruby
ruby.c = ruby
ruby.d = ruby





class s(base_element):
    tag = "s"


s.r = s
s.c = s
s.d = s





class samp(base_element):
    tag = "samp"


samp.r = samp
samp.c = samp
samp.d = samp





class script(base_element):
    tag = "script"


script.r = script
script.c = script
script.d = script





class section(base_element):
    tag = "section"


section.r = section
section.c = section
section.d = section





class small(base_element):
    tag = "small"


small.r = small
small.c = small
small.d = small





class span(base_element):
    tag = "span"


span.r = span
span.c = span
span.d = span





class strike(base_element):
    tag = "strike"


strike.r = strike
strike.c = strike
strike.d = strike





class strong(base_element):
    tag = "strong"


strong.r = strong
strong.c = strong
strong.d = strong





class style(base_element):
    tag = "style"


style.r = style
style.c = style
style.d = style





class sub(base_element):
    tag = "sub"


sub.r = sub
sub.c = sub
sub.d = sub





class summary(base_element):
    tag = "summary"


summary.r = summary
summary.c = summary
summary.d = summary





class sup(base_element):
    tag = "sup"


sup.r = sup
sup.c = sup
sup.d = sup





class svg(base_element):
    tag = "svg"


svg.r = svg
svg.c = svg
svg.d = svg





class table(base_element):
    tag = "table"


table.r = table
table.c = table
table.d = table





class tbody(base_element):
    tag = "tbody"


tbody.r = tbody
tbody.c = tbody
tbody.d = tbody





class td(base_element):
    tag = "td"


td.r = td
td.c = td
td.d = td





class template(base_element):
    tag = "template"


template.r = template
template.c = template
template.d = template





class tfoot(base_element):
    tag = "tfoot"


tfoot.r = tfoot
tfoot.c = tfoot
tfoot.d = tfoot





class th(base_element):
    tag = "th"


th.r = th
th.c = th
th.d = th





class thead(base_element):
    tag = "thead"


thead.r = thead
thead.c = thead
thead.d = thead





class time(base_element):
    tag = "time"


time.r = time
time.c = time
time.d = time





class title(base_element):
    tag = "title"


title.r = title
title.c = title
title.d = title





class tr(base_element):
    tag = "tr"


tr.r = tr
tr.c = tr
tr.d = tr





class tt(base_element):
    tag = "tt"


tt.r = tt
tt.c = tt
tt.d = tt





class u(base_element):
    tag = "u"


u.r = u
u.c = u
u.d = u





class ul(base_element):
    tag = "ul"


ul.r = ul
ul.c = ul
ul.d = ul





class var(base_element):
    tag = "var"


var.r = var
var.c = var
var.d = var





class video(base_element):
    tag = "video"


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

