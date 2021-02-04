# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)

import string, sys
from collections import OrderedDict
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
        target_id=kwargs.get("target_id", "__main__"),
        commands=[], )


def hypergen(func, *args, **kwargs):
    kwargs = deepcopy(kwargs)
    target_id = kwargs.pop("target_id", "__main__")
    with c(hypergen=hypergen_context(target_id=target_id, **kwargs)):
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
        self.attrs["id_"] = LazyAttribute("id", self.attrs.get("id_", None))
        self.i = len(c.hypergen.into)
        self.sep = attrs.pop("sep", "")

        for child in children:
            if issubclass(type(child), base_element):
                child.delete()
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

    # def __str__(self):
    #     assert False, "DONT DO IT"
    #     into = self.start()
    #     into.extend(self.end())
    #     s = join_html(into)
    #     return s

    # def __unicode__(self):
    #     return self.__str__()

    def as_string(self):
        into = self.start()
        into.extend(self.end())
        s = join_html(into)
        return s

    def delete(self):
        for i in range(self.i, self.j):
            c.hypergen.into[i] = DELETED

    def format_children(self, children):
        into = []
        sep = t(self.sep)

        for x in children:
            if x in ("", None):
                continue
            elif issubclass(type(x), base_element):
                into.append(x)
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
        if self.attrs["id_"].v is None:
            self.attrs[
                "id_"].v = c.hypergen.id_prefix + next(c.hypergen.id_counter)
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
                if issubclass(type(arg), base_element):
                    if arg.attrs["id_"].v is None:
                        arg.attrs["id_"].v = c.hypergen.id_prefix + next(
                            c.hypergen.id_counter)
                args2.append(arg)

        return lambda: "H.cb({})".format(
            freedom.dumps(
                [func.hypergen_callback_url] + list(args2),
                unquote=True,
                escape=True,
                this=self))

    def attribute(self, k, v):
        k = t(k).rstrip("_").replace("_", "-")
        if c.hypergen.liveview is True and k.startswith("on") and type(v) in (
                list, tuple):
            return [" ", k, '="', self.liveview_attribute(v), '"']
        elif type(v) is LazyAttribute:
            return [v]
        elif type(v) is bool:
            if v is True:
                return [join((" ", k))]
        elif k == "style" and type(v) in (dict, OrderedDict):
            return [
                join((" ", k, '="', ";".join(
                    t(k1) + ":" + t(v1) for k1, v1 in items(v)), '"'))
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


### Some special dom elements ###

INPUT_CALLBACK_TYPES = dict(
    checkbox="H.cbs.c",
    month="H.cbs.i",
    number="H.cbs.i",
    range="H.cbs.f",
    week="H.cbs.i")


class input_(base_element_void):
    void = True

    def __init__(self, *children, **attrs):
        self.js_cb = INPUT_CALLBACK_TYPES.get(
            attrs.get("type_", "text"), "H.cbs.s")
        super(input_, self).__init__(*children, **attrs)

    void = True


input_.c = input_
input_.d = input_
input_.r = input_

### Special tags ###


def doctype(type_="html"):
    raw("<!DOCTYPE ", type_, ">")


### GENERATED BY build.py ###
# yapf: disable
class a(base_element): pass
a.c = a
a.d = a
a.r = a
class abbr(base_element): pass
abbr.c = abbr
abbr.d = abbr
abbr.r = abbr
class acronym(base_element): pass
acronym.c = acronym
acronym.d = acronym
acronym.r = acronym
class address(base_element): pass
address.c = address
address.d = address
address.r = address
class applet(base_element): pass
applet.c = applet
applet.d = applet
applet.r = applet
class area(base_element_void): pass
area.c = area
area.d = area
area.r = area
class article(base_element): pass
article.c = article
article.d = article
article.r = article
class aside(base_element): pass
aside.c = aside
aside.d = aside
aside.r = aside
class audio(base_element): pass
audio.c = audio
audio.d = audio
audio.r = audio
class b(base_element): pass
b.c = b
b.d = b
b.r = b
class base(base_element_void): pass
base.c = base
base.d = base
base.r = base
class basefont(base_element): pass
basefont.c = basefont
basefont.d = basefont
basefont.r = basefont
class bdi(base_element): pass
bdi.c = bdi
bdi.d = bdi
bdi.r = bdi
class bdo(base_element): pass
bdo.c = bdo
bdo.d = bdo
bdo.r = bdo
class big(base_element): pass
big.c = big
big.d = big
big.r = big
class blockquote(base_element): pass
blockquote.c = blockquote
blockquote.d = blockquote
blockquote.r = blockquote
class body(base_element): pass
body.c = body
body.d = body
body.r = body
class br(base_element_void): pass
br.c = br
br.d = br
br.r = br
class button(base_element): pass
button.c = button
button.d = button
button.r = button
class canvas(base_element): pass
canvas.c = canvas
canvas.d = canvas
canvas.r = canvas
class caption(base_element): pass
caption.c = caption
caption.d = caption
caption.r = caption
class center(base_element): pass
center.c = center
center.d = center
center.r = center
class cite(base_element): pass
cite.c = cite
cite.d = cite
cite.r = cite
class code(base_element): pass
code.c = code
code.d = code
code.r = code
class col(base_element_void): pass
col.c = col
col.d = col
col.r = col
class colgroup(base_element): pass
colgroup.c = colgroup
colgroup.d = colgroup
colgroup.r = colgroup
class data(base_element): pass
data.c = data
data.d = data
data.r = data
class datalist(base_element): pass
datalist.c = datalist
datalist.d = datalist
datalist.r = datalist
class dd(base_element): pass
dd.c = dd
dd.d = dd
dd.r = dd
class del_(base_element): pass
del_.c = del_
del_.d = del_
del_.r = del_
class details(base_element): pass
details.c = details
details.d = details
details.r = details
class dfn(base_element): pass
dfn.c = dfn
dfn.d = dfn
dfn.r = dfn
class dialog(base_element): pass
dialog.c = dialog
dialog.d = dialog
dialog.r = dialog
class dir_(base_element): pass
dir_.c = dir_
dir_.d = dir_
dir_.r = dir_
class div(base_element): pass
div.c = div
div.d = div
div.r = div
class dl(base_element): pass
dl.c = dl
dl.d = dl
dl.r = dl
class dt(base_element): pass
dt.c = dt
dt.d = dt
dt.r = dt
class em(base_element): pass
em.c = em
em.d = em
em.r = em
class embed(base_element_void): pass
embed.c = embed
embed.d = embed
embed.r = embed
class fieldset(base_element): pass
fieldset.c = fieldset
fieldset.d = fieldset
fieldset.r = fieldset
class figcaption(base_element): pass
figcaption.c = figcaption
figcaption.d = figcaption
figcaption.r = figcaption
class figure(base_element): pass
figure.c = figure
figure.d = figure
figure.r = figure
class font(base_element): pass
font.c = font
font.d = font
font.r = font
class footer(base_element): pass
footer.c = footer
footer.d = footer
footer.r = footer
class form(base_element): pass
form.c = form
form.d = form
form.r = form
class frame(base_element): pass
frame.c = frame
frame.d = frame
frame.r = frame
class frameset(base_element): pass
frameset.c = frameset
frameset.d = frameset
frameset.r = frameset
class h1(base_element): pass
h1.c = h1
h1.d = h1
h1.r = h1
class h2(base_element): pass
h2.c = h2
h2.d = h2
h2.r = h2
class h3(base_element): pass
h3.c = h3
h3.d = h3
h3.r = h3
class h4(base_element): pass
h4.c = h4
h4.d = h4
h4.r = h4
class h5(base_element): pass
h5.c = h5
h5.d = h5
h5.r = h5
class h6(base_element): pass
h6.c = h6
h6.d = h6
h6.r = h6
class head(base_element): pass
head.c = head
head.d = head
head.r = head
class header(base_element): pass
header.c = header
header.d = header
header.r = header
class hr(base_element_void): pass
hr.c = hr
hr.d = hr
hr.r = hr
class html(base_element): pass
html.c = html
html.d = html
html.r = html
class i(base_element): pass
i.c = i
i.d = i
i.r = i
class iframe(base_element): pass
iframe.c = iframe
iframe.d = iframe
iframe.r = iframe
class img(base_element_void): pass
img.c = img
img.d = img
img.r = img
class ins(base_element): pass
ins.c = ins
ins.d = ins
ins.r = ins
class kbd(base_element): pass
kbd.c = kbd
kbd.d = kbd
kbd.r = kbd
class label(base_element): pass
label.c = label
label.d = label
label.r = label
class legend(base_element): pass
legend.c = legend
legend.d = legend
legend.r = legend
class li(base_element): pass
li.c = li
li.d = li
li.r = li
class link(base_element): pass
link.c = link
link.d = link
link.r = link
class main(base_element): pass
main.c = main
main.d = main
main.r = main
class map_(base_element): pass
map_.c = map_
map_.d = map_
map_.r = map_
class mark(base_element): pass
mark.c = mark
mark.d = mark
mark.r = mark
class meta(base_element_void): pass
meta.c = meta
meta.d = meta
meta.r = meta
class meter(base_element): pass
meter.c = meter
meter.d = meter
meter.r = meter
class nav(base_element): pass
nav.c = nav
nav.d = nav
nav.r = nav
class noframes(base_element): pass
noframes.c = noframes
noframes.d = noframes
noframes.r = noframes
class noscript(base_element): pass
noscript.c = noscript
noscript.d = noscript
noscript.r = noscript
class object_(base_element): pass
object_.c = object_
object_.d = object_
object_.r = object_
class ol(base_element): pass
ol.c = ol
ol.d = ol
ol.r = ol
class optgroup(base_element): pass
optgroup.c = optgroup
optgroup.d = optgroup
optgroup.r = optgroup
class option(base_element): pass
option.c = option
option.d = option
option.r = option
class output(base_element): pass
output.c = output
output.d = output
output.r = output
class p(base_element): pass
p.c = p
p.d = p
p.r = p
class param(base_element_void): pass
param.c = param
param.d = param
param.r = param
class picture(base_element): pass
picture.c = picture
picture.d = picture
picture.r = picture
class pre(base_element): pass
pre.c = pre
pre.d = pre
pre.r = pre
class progress(base_element): pass
progress.c = progress
progress.d = progress
progress.r = progress
class q(base_element): pass
q.c = q
q.d = q
q.r = q
class rp(base_element): pass
rp.c = rp
rp.d = rp
rp.r = rp
class rt(base_element): pass
rt.c = rt
rt.d = rt
rt.r = rt
class ruby(base_element): pass
ruby.c = ruby
ruby.d = ruby
ruby.r = ruby
class s(base_element): pass
s.c = s
s.d = s
s.r = s
class samp(base_element): pass
samp.c = samp
samp.d = samp
samp.r = samp
class script(base_element): pass
script.c = script
script.d = script
script.r = script
class section(base_element): pass
section.c = section
section.d = section
section.r = section
class select(base_element): pass
select.c = select
select.d = select
select.r = select
class small(base_element): pass
small.c = small
small.d = small
small.r = small
class source(base_element_void): pass
source.c = source
source.d = source
source.r = source
class span(base_element): pass
span.c = span
span.d = span
span.r = span
class strike(base_element): pass
strike.c = strike
strike.d = strike
strike.r = strike
class strong(base_element): pass
strong.c = strong
strong.d = strong
strong.r = strong
class style(base_element): pass
style.c = style
style.d = style
style.r = style
class sub(base_element): pass
sub.c = sub
sub.d = sub
sub.r = sub
class summary(base_element): pass
summary.c = summary
summary.d = summary
summary.r = summary
class sup(base_element): pass
sup.c = sup
sup.d = sup
sup.r = sup
class svg(base_element): pass
svg.c = svg
svg.d = svg
svg.r = svg
class table(base_element): pass
table.c = table
table.d = table
table.r = table
class tbody(base_element): pass
tbody.c = tbody
tbody.d = tbody
tbody.r = tbody
class td(base_element): pass
td.c = td
td.d = td
td.r = td
class template(base_element): pass
template.c = template
template.d = template
template.r = template
class textarea(base_element): pass
textarea.c = textarea
textarea.d = textarea
textarea.r = textarea
class tfoot(base_element): pass
tfoot.c = tfoot
tfoot.d = tfoot
tfoot.r = tfoot
class th(base_element): pass
th.c = th
th.d = th
th.r = th
class thead(base_element): pass
thead.c = thead
thead.d = thead
thead.r = thead
class time(base_element): pass
time.c = time
time.d = time
time.r = time
class title(base_element): pass
title.c = title
title.d = title
title.r = title
class tr(base_element): pass
tr.c = tr
tr.d = tr
tr.r = tr
class track(base_element_void): pass
track.c = track
track.d = track
track.r = track
class tt(base_element): pass
tt.c = tt
tt.d = tt
tt.r = tt
class u(base_element): pass
u.c = u
u.d = u
u.r = u
class ul(base_element): pass
ul.c = ul
ul.d = ul
ul.r = ul
class var(base_element): pass
var.c = var
var.d = var
var.r = var
class video(base_element): pass
video.c = video
video.d = video
video.r = video
class wbr(base_element_void): pass
wbr.c = wbr
wbr.d = wbr
wbr.r = wbr
# yapf: enable
