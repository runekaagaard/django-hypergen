# coding = utf-8
# pylint: disable=no-value-for-parameter
d = dict
import datetime

from yapf.yapflib.yapf_api import FormatCode

from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED
from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.core import context as c
import templates as shared_templates

@hypergen_view(url="", perm=NO_PERM_REQUIRED, base_template=shared_templates.base_template, target_id="content")
def inputs(request):
    style("pre { background-color: gainsboro; padding: 4px;}")
    INPUT_TYPES = [
        ("checkbox", d(checked=True)),
        ("color", d(value="#bb7777")),
        ("date", d(value=datetime.date(2021, 4, 16))),
        ("datetime-local", d(value=datetime.datetime(1941, 5, 5, 5, 23))),
        ("email", d(value="foo@example.com")),
        ("file", d()),
        ("hidden", d(value="hidden")),
        ("month", d(value=d(year=2099, month=9))),
        ("number", d(title="number (int)", value=99)),
        ("number", d(title="number (float)", value=12.12, coerce_to=float)),
        ("password", d(value="1234")),
        ("radio", d(name="myradio", value=20, checked=True, coerce_to=int)),
        ("radio", d(name="myradio", value=21, coerce_to=int)),
        ("range", d()),
        ("search", d(value="Who is Rune Kaagaard?")),
        ("tel", d(value="12345678")),
        ("text", d(value="This is text!")),
        ("time", d(value=datetime.time(7, 42))),
        ("url", d(value="https://github.com/runekaagaard/django-hypergen/")),
        ("week", d(value=d(year=1999, week=42))),]

    CLICK_TYPES = [
        ("button", d(value="clicked")),
        ("image", d(src="https://picsum.photos/80/40", value="clicked")),
        ("reset", d(value="clicked")),
        ("submit", d(value="clicked")),]

    h1("Showing all input types.")
    with table():
        tr(th(x) for x in ["Input type", "Code", "Rendered", "Server callback value"])

        for i, pair in enumerate(INPUT_TYPES):
            type_, attrs = pair
            title = attrs.pop("title", type_)
            id_ = "server-value-{}".format(i)

            with tr():
                submit_cb = cb(submit, THIS, id_)
                el = input_(id_=("element", i), type_=type_, oninput=submit_cb, **attrs)
                th(title)
                td(pre(code(FormatCode(repr(el))[0])))
                td(el)
                td(id_=id_)

        for i, pair in enumerate(CLICK_TYPES):
            i += len(INPUT_TYPES)
            type_, attrs = pair
            title = attrs.pop("title", type_)
            id_ = "server-value-{}".format(i)

            with tr():
                submit_cb = cb(submit, THIS, id_)
                el = input_(id_=("element", i), type_=type_, onclick=submit_cb, **attrs)
                th(title)
                td(pre(code(FormatCode(repr(el))[0])))
                td(el)
                td(id_=id_)

        with tr():
            i += 1
            id_ = "server-value-{}".format(i)
            attrs = d()
            submit_cb = cb(submit, THIS, id_)
            el = textarea("Who is Jeppe Tuxen?", id_=("element", i), oninput=submit_cb, **attrs)
            th("textarea")
            td(pre(code(FormatCode(repr(el))[0])))
            td(el)
            td(id_=id_)

        with tr():
            i += 1
            id_ = "server-value-{}".format(i)
            attrs = d(coerce_to=int)
            submit_cb = cb(submit, THIS, id_)
            el = select([option(x, value=x, selected=x == 3) for x in range(5)], id_=("element", i),
                onclick=submit_cb, oninput=submit_cb, **attrs)
            th("select")
            td(pre(code(FormatCode(repr(el))[0])))
            td(el)
            td(id_=id_)

    # script("""
    #     ready(function() {
    #          document.querySelectorAll(".input").forEach(el => (el.oninput(new Event("input"))));
    #     })
    # """)

@hypergen_callback(perm=NO_PERM_REQUIRED)
def submit(request, value, target_id):
    c.hypergen = c.hypergen.set("target_id", target_id)
    with pre(style={"padding": 0}):
        raw(repr(value), " (", type(value).__name__, ")")
