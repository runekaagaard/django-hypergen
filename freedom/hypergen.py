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
from freedom.core import context as c

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


### Rendering ###
def hypergen_context(**kwargs):
    from freedom.core import namespace as ns
    return ns(
        into=[],
        liveview=True,
        id_counter=base65_counter(),
        id_prefix=(freedom.loads(c.request.body)["id_prefix"]
                   if c.request.is_ajax() else ""),
        event_handler_cache={},
        target_id=kwargs.pop("target_id", "__main__"),
        commands=[], )


def hypergen(func, *args, **kwargs):
    with c(hypergen=hypergen_context(**kwargs)):
        func(*args, **kwargs)
        html = join_html(c.hypergen.into)
        if c.hypergen.event_handler_cache:
            c.hypergen.commands.append([
                "./freedom", ["setEventHandlerCache"],
                [c.hypergen.target_id, c.hypergen.event_handler_cache]
            ])
        if not c.request.is_ajax():
            pos = html.find("</head")
            if pos != -1:
                s = '<script>window.applyCommands({})</script>'.format(
                    freedom.dumps(c.hypergen.commands))
                html = insert(html, s, pos)

            return HttpResponse(html)
        else:
            c.hypergen.commands.append(
                ["./freedom", ["morph"], [c.hypergen.target_id, html]])

            return c.hypergen.commands


### Helpers ###


def join(*values):
    return "".join(str(x) for x in values)


def join_html(html):
    def fmt(html):
        for item in html:
            if issubclass(type(item), base_element):
                yield str(item)
            elif callable(item):
                yield str(item())
            else:
                yield str(item)

    return "".join(fmt(html))


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


### Django ###


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

    return func


### Base dom element ###
class THIS(object):
    pass


NON_SCALARS = set((list, dict, tuple))
DELETED = ""


class base_element(ContextDecorator):
    js_cb = "H.cbs.s"
    void = False
    auto_id = False

    def __new__(cls, *args, **kwargs):
        instance = ContextDecorator.__new__(cls)
        setattr(instance, "tag", cls.__name__.rstrip("_"))
        return instance

    def __init__(self, *children, **attrs):
        assert "hypergen" in c, "Missing global context: hypergen"
        self.children = children
        self.attrs = attrs
        self.i = len(c.hypergen.into)
        self.sep = attrs.pop("sep", "")
        self.auto_id = self.has_any_liveview_attribute()

        for child in children:
            if issubclass(type(child), base_element):
                c.hypergen.into[child.i] = DELETED
        c.hypergen.into.append(lambda: join_html((self.start(), self.end())))
        super(base_element, self).__init__()

    def __enter__(self):
        c.hypergen.into.append(lambda: self.start())
        c.hypergen.into[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        if not self.void:
            c.hypergen.into.append(lambda: self.end())

    def __str__(self):
        return join_html((self.start(), self.end()))

    def __unicode__(self):
        return self.__str__()

    def format_children(self, children):
        into = []
        sep = t(self.sep)

        for x in children:
            if x in ("", None):
                continue
            elif issubclass(type(x), base_element):
                into.append(str(x))
            elif type(x) in (list, tuple, GeneratorType):
                into.extend(self.format_children(list(x)))
            elif callable(x):
                into.append(x)
            else:
                into.append(t(x))
            if sep:
                into.append(sep)
        if sep and children:
            into.pop()

        return into

    def liveview_attribute(self, args):
        func = args[0]
        assert callable(func), (
            "First callback argument must be a callable, got "
            "{}.".format(repr(func)))
        args = args[1:]

        args2 = []
        for arg in args:
            if type(arg) in NON_SCALARS:
                c.hypergen.event_handler_cache[id(arg)] = arg
                args2.append(
                    freedom.quote("H.e['{}'][{}]".format(
                        c.hypergen.target_id, id(arg))))
            else:
                args2.append(arg)

        print "AAAAAAAAAAAAAAAAAAA", args2
        return "H.cb({})".format(
            freedom.dumps(
                [func.hypergen_callback_url] + list(args2),
                unquote=True,
                escape=True,
                this=self))

    def has_any_liveview_attribute(self):
        return any(self.is_liveview_attribute(*x) for x in items(self.attrs))

    def is_liveview_attribute(self, k, v):
        return c.hypergen.liveview is True and k.startswith("on") and type(
            v) in (list, tuple)

    def attribute(self, k, v):
        k = t(k).rstrip("_").replace("_", "-")
        if self.is_liveview_attribute(k, v):
            return join(" ", k, '="', self.liveview_attribute(v), '"')
        elif type(v) is bool:
            if v is True:
                return join((" ", k))
        elif k == "style" and type(v) in (dict, OrderedDict):
            return join((" ", k, '="', ";".join(
                t(k1) + ":" + t(v1) for k1, v1 in items(v)), '"'))
        else:
            return join(" ", k, '="', t(v), '"')

    def start(self):
        if self.auto_id and "id_" not in self.attrs:
            self.attrs[
                "id_"] = c.hypergen.id_prefix + next(c.hypergen.id_counter)

        into = ["<", self.tag]
        for k, v in items(self.attrs):
            into.append(self.attribute(k, v))

        if self.void:
            into.append(join(("/")))
        into.append(join('>', ))
        into.extend(self.format_children(self.children))

        return join_html(into)

    def end(self):
        if not self.void:
            return "</{}>".format(self.tag)
        else:
            return ""


### Some special dom elements ###

INPUT_CALLBACK_TYPES = dict(
    checkbox="H.cbs.c",
    month="H.cbs.i",
    number="H.cbs.i",
    range="H.cbs.f",
    week="H.cbs.i")


class input_(base_element):
    void = True

    def __init__(self, *children, **attrs):
        self.js_cb = INPUT_CALLBACK_TYPES.get(
            attrs.get("type_", "text"), "H.cbs.s")
        super(input_, self).__init__(*children, **attrs)

    void = True


### Special tags ###


def doctype(type_="html"):
    raw("<!DOCTYPE ", type_, ">")


### TEMPLATE-ELEMENT ###


class div(base_element):
    pass


div.r = div
div.c = div
div.d = div


### TEMPLATE-ELEMENT ###
### TEMPLATE-VOID-ELEMENT ###
class link(base_element):
    void = True


link.r = link
### TEMPLATE-VOID-ELEMENT ###




class a(base_element):
    pass


a.r = a
a.c = a
a.d = a





class abbr(base_element):
    pass


abbr.r = abbr
abbr.c = abbr
abbr.d = abbr





class acronym(base_element):
    pass


acronym.r = acronym
acronym.c = acronym
acronym.d = acronym





class address(base_element):
    pass


address.r = address
address.c = address
address.d = address





class applet(base_element):
    pass


applet.r = applet
applet.c = applet
applet.d = applet





class article(base_element):
    pass


article.r = article
article.c = article
article.d = article





class aside(base_element):
    pass


aside.r = aside
aside.c = aside
aside.d = aside





class audio(base_element):
    pass


audio.r = audio
audio.c = audio
audio.d = audio





class b(base_element):
    pass


b.r = b
b.c = b
b.d = b





class basefont(base_element):
    pass


basefont.r = basefont
basefont.c = basefont
basefont.d = basefont





class bdi(base_element):
    pass


bdi.r = bdi
bdi.c = bdi
bdi.d = bdi





class bdo(base_element):
    pass


bdo.r = bdo
bdo.c = bdo
bdo.d = bdo





class big(base_element):
    pass


big.r = big
big.c = big
big.d = big





class blockquote(base_element):
    pass


blockquote.r = blockquote
blockquote.c = blockquote
blockquote.d = blockquote





class body(base_element):
    pass


body.r = body
body.c = body
body.d = body





class button(base_element):
    pass


button.r = button
button.c = button
button.d = button





class canvas(base_element):
    pass


canvas.r = canvas
canvas.c = canvas
canvas.d = canvas





class caption(base_element):
    pass


caption.r = caption
caption.c = caption
caption.d = caption





class center(base_element):
    pass


center.r = center
center.c = center
center.d = center





class cite(base_element):
    pass


cite.r = cite
cite.c = cite
cite.d = cite





class code(base_element):
    pass


code.r = code
code.c = code
code.d = code





class colgroup(base_element):
    pass


colgroup.r = colgroup
colgroup.c = colgroup
colgroup.d = colgroup





class data(base_element):
    pass


data.r = data
data.c = data
data.d = data





class datalist(base_element):
    pass


datalist.r = datalist
datalist.c = datalist
datalist.d = datalist





class dd(base_element):
    pass


dd.r = dd
dd.c = dd
dd.d = dd





class del_(base_element):
    pass


del_.r = del_
del_.c = del_
del_.d = del_





class details(base_element):
    pass


details.r = details
details.c = details
details.d = details





class dfn(base_element):
    pass


dfn.r = dfn
dfn.c = dfn
dfn.d = dfn





class dialog(base_element):
    pass


dialog.r = dialog
dialog.c = dialog
dialog.d = dialog





class dir_(base_element):
    pass


dir_.r = dir_
dir_.c = dir_
dir_.d = dir_





class dl(base_element):
    pass


dl.r = dl
dl.c = dl
dl.d = dl





class dt(base_element):
    pass


dt.r = dt
dt.c = dt
dt.d = dt





class em(base_element):
    pass


em.r = em
em.c = em
em.d = em





class fieldset(base_element):
    pass


fieldset.r = fieldset
fieldset.c = fieldset
fieldset.d = fieldset





class figcaption(base_element):
    pass


figcaption.r = figcaption
figcaption.c = figcaption
figcaption.d = figcaption





class figure(base_element):
    pass


figure.r = figure
figure.c = figure
figure.d = figure





class font(base_element):
    pass


font.r = font
font.c = font
font.d = font





class footer(base_element):
    pass


footer.r = footer
footer.c = footer
footer.d = footer





class form(base_element):
    pass


form.r = form
form.c = form
form.d = form





class frame(base_element):
    pass


frame.r = frame
frame.c = frame
frame.d = frame





class frameset(base_element):
    pass


frameset.r = frameset
frameset.c = frameset
frameset.d = frameset





class h1(base_element):
    pass


h1.r = h1
h1.c = h1
h1.d = h1





class h2(base_element):
    pass


h2.r = h2
h2.c = h2
h2.d = h2





class h3(base_element):
    pass


h3.r = h3
h3.c = h3
h3.d = h3





class h4(base_element):
    pass


h4.r = h4
h4.c = h4
h4.d = h4





class h5(base_element):
    pass


h5.r = h5
h5.c = h5
h5.d = h5





class h6(base_element):
    pass


h6.r = h6
h6.c = h6
h6.d = h6





class head(base_element):
    pass


head.r = head
head.c = head
head.d = head





class header(base_element):
    pass


header.r = header
header.c = header
header.d = header





class html(base_element):
    pass


html.r = html
html.c = html
html.d = html





class i(base_element):
    pass


i.r = i
i.c = i
i.d = i





class iframe(base_element):
    pass


iframe.r = iframe
iframe.c = iframe
iframe.d = iframe





class ins(base_element):
    pass


ins.r = ins
ins.c = ins
ins.d = ins





class kbd(base_element):
    pass


kbd.r = kbd
kbd.c = kbd
kbd.d = kbd





class label(base_element):
    pass


label.r = label
label.c = label
label.d = label





class legend(base_element):
    pass


legend.r = legend
legend.c = legend
legend.d = legend





class li(base_element):
    pass


li.r = li
li.c = li
li.d = li





class main(base_element):
    pass


main.r = main
main.c = main
main.d = main





class map_(base_element):
    pass


map_.r = map_
map_.c = map_
map_.d = map_





class mark(base_element):
    pass


mark.r = mark
mark.c = mark
mark.d = mark





class meter(base_element):
    pass


meter.r = meter
meter.c = meter
meter.d = meter





class nav(base_element):
    pass


nav.r = nav
nav.c = nav
nav.d = nav





class noframes(base_element):
    pass


noframes.r = noframes
noframes.c = noframes
noframes.d = noframes





class noscript(base_element):
    pass


noscript.r = noscript
noscript.c = noscript
noscript.d = noscript





class object_(base_element):
    pass


object_.r = object_
object_.c = object_
object_.d = object_





class ol(base_element):
    pass


ol.r = ol
ol.c = ol
ol.d = ol





class optgroup(base_element):
    pass


optgroup.r = optgroup
optgroup.c = optgroup
optgroup.d = optgroup





class option(base_element):
    pass


option.r = option
option.c = option
option.d = option





class output(base_element):
    pass


output.r = output
output.c = output
output.d = output





class p(base_element):
    pass


p.r = p
p.c = p
p.d = p





class picture(base_element):
    pass


picture.r = picture
picture.c = picture
picture.d = picture





class pre(base_element):
    pass


pre.r = pre
pre.c = pre
pre.d = pre





class progress(base_element):
    pass


progress.r = progress
progress.c = progress
progress.d = progress





class q(base_element):
    pass


q.r = q
q.c = q
q.d = q





class rp(base_element):
    pass


rp.r = rp
rp.c = rp
rp.d = rp





class rt(base_element):
    pass


rt.r = rt
rt.c = rt
rt.d = rt





class ruby(base_element):
    pass


ruby.r = ruby
ruby.c = ruby
ruby.d = ruby





class s(base_element):
    pass


s.r = s
s.c = s
s.d = s





class samp(base_element):
    pass


samp.r = samp
samp.c = samp
samp.d = samp





class script(base_element):
    pass


script.r = script
script.c = script
script.d = script





class section(base_element):
    pass


section.r = section
section.c = section
section.d = section





class small(base_element):
    pass


small.r = small
small.c = small
small.d = small





class span(base_element):
    pass


span.r = span
span.c = span
span.d = span





class strike(base_element):
    pass


strike.r = strike
strike.c = strike
strike.d = strike





class strong(base_element):
    pass


strong.r = strong
strong.c = strong
strong.d = strong





class style(base_element):
    pass


style.r = style
style.c = style
style.d = style





class sub(base_element):
    pass


sub.r = sub
sub.c = sub
sub.d = sub





class summary(base_element):
    pass


summary.r = summary
summary.c = summary
summary.d = summary





class sup(base_element):
    pass


sup.r = sup
sup.c = sup
sup.d = sup





class svg(base_element):
    pass


svg.r = svg
svg.c = svg
svg.d = svg





class table(base_element):
    pass


table.r = table
table.c = table
table.d = table





class tbody(base_element):
    pass


tbody.r = tbody
tbody.c = tbody
tbody.d = tbody





class td(base_element):
    pass


td.r = td
td.c = td
td.d = td





class template(base_element):
    pass


template.r = template
template.c = template
template.d = template





class tfoot(base_element):
    pass


tfoot.r = tfoot
tfoot.c = tfoot
tfoot.d = tfoot





class th(base_element):
    pass


th.r = th
th.c = th
th.d = th





class thead(base_element):
    pass


thead.r = thead
thead.c = thead
thead.d = thead





class time(base_element):
    pass


time.r = time
time.c = time
time.d = time





class title(base_element):
    pass


title.r = title
title.c = title
title.d = title





class tr(base_element):
    pass


tr.r = tr
tr.c = tr
tr.d = tr





class tt(base_element):
    pass


tt.r = tt
tt.c = tt
tt.d = tt





class u(base_element):
    pass


u.r = u
u.c = u
u.d = u





class ul(base_element):
    pass


ul.r = ul
ul.c = ul
ul.d = ul





class var(base_element):
    pass


var.r = var
var.c = var
var.d = var





class video(base_element):
    pass


video.r = video
video.c = video
video.d = video





class wbr(base_element):
    void = True


wbr.r = wbr

class img(base_element):
    void = True


img.r = img

class area(base_element):
    void = True


area.r = area

class hr(base_element):
    void = True


hr.r = hr

class param(base_element):
    void = True


param.r = param

class keygen(base_element):
    void = True


keygen.r = keygen

class source(base_element):
    void = True


source.r = source

class base(base_element):
    void = True


base.r = base

class meta(base_element):
    void = True


meta.r = meta

class br(base_element):
    void = True


br.r = br

class track(base_element):
    void = True


track.r = track

class menuitem(base_element):
    void = True


menuitem.r = menuitem

class command(base_element):
    void = True


command.r = command

class embed(base_element):
    void = True


embed.r = embed

class col(base_element):
    void = True


col.r = col

