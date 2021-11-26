
import bs4
import sys
import argparse
import pyperclip as pc
from bs4 import BeautifulSoup as bs, Tag, NavigableString
import keyword

GLOBALS = list(globals().keys())
BUILTINS = dir(__builtins__)

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file")
args = parser.parse_args()

def protect(x):
    if x in GLOBALS or x in BUILTINS or x in keyword.kwlist:
        return x + "_"
    else:
        return x

def tag_clone(self):
    copy = type(self)(None, self.builder, self.name, self.namespace, self.nsprefix)
    # work around bug where there is no builder set
    # https://bugs.launchpad.net/beautifulsoup/+bug/1307471
    copy.attrs = dict(self.attrs)
    for attr in ('can_be_empty_element', 'hidden'):
        setattr(copy, attr, getattr(self, attr))
    for child in self.contents:
        copy.append(child.clone())
    return copy

Tag.clone = tag_clone
NavigableString.clone = lambda self: type(self)(self)

def indent(txt, i):
    return "".join(["    " * i, txt])

def _attr_val(val):
    if type(val) is list:
        return (" ".join(val))
    return val

def _attrs(tag):
    def fmt_v(v):
        if type(v) in (list, tuple):
            return " ".join(v)
        else:
            return v

    omit = {"data-reactid", "aria-label"}
    omit_v = {"link": {"type": "text/css", "rel": "stylesheet"}, "script": {"type": "text/javascript"}}

    a = []
    for k, v in list(tag.attrs.items()):
        q = '"'
        v = fmt_v(v)
        if k in omit:
            continue
        x = omit_v.get(tag.name, None)
        if x:
            y = x.get(k, None)
            if y and y == v:
                continue
        if tag.name in ("link", "script", "meta"):
            if k in ("href", "src", "content"):
                if v.startswith("/static/"):
                    v = v.replace("/static/", "")
                    v = 'static("{}")'.format(v)
                    q = ""
        k = k.strip().replace("-", "_")
        k = protect(k)
        a.append('{}={}{}{}'.format(k, q, v, q))

    return ", ".join(a)

def _string(tag):
    for child in tag.children:
        if type(child) in (bs4.element.NavigableString, bs4.element.Script):
            return child.string

def _params(tag):
    def multiline(x):
        if "\n" in x:
            return '"""{}"""'.format(x)
        else:
            return '"{}"'.format(x)

    if _string(tag):
        txt = multiline(tag.string) if tag.string is not None else None
        if _attrs(tag):
            return ', '.join(x for x in [txt, _attrs(tag)] if x is not None)
        return txt
    return _attrs(tag)

def _c(tag, i):
    if not tag.name:
        return ""

    p = _params(tag)
    if p is None:
        p = ""

    return indent("with {}({}):\n".format(protect(tag.name), p), i)

def _(tag, i):
    if not tag.name:
        return ""

    return indent("{}({})\n".format(protect(tag.name), _params(tag)), i)

def hyperfy(html, i_start=1):
    soup = bs(html, 'html.parser')
    txt = "from django.templatetags.static import static\n\ndef my_hypergen_template():\n"
    for d in soup.descendants:
        e = d.clone()
        indent = len(list(d.parents)) - i_start + 1
        if type(e) == bs4.element.Tag:
            if len(list(e.children)) == 0 or (len(list(e.children)) == 1
                and type(next(e.children)) in [bs4.element.NavigableString, bs4.element.Script]):
                txt += _(d, indent)
            else:
                txt += _c(d, indent)
        else:
            pass
    return txt

if args.file:
    with open(args.file, "r") as file:
        sys.stdout.write(hyperfy(file))
else:
    txt = hyperfy(pc.paste())
    pc.copy(txt)
    sys.stdout.write(txt)
