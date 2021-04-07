# coding = utf-8
# pylint: disable=no-value-for-parameter
from datetime import date, time, datetime

from freedom.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED
from freedom.hypergen import *
from freedom.hypergen import callback as cb
from freedom.core import context as c
import templates as shared_templates

HYPERGEN_SETTINGS = dict(perm=NO_PERM_REQUIRED, base_template=shared_templates.base_template, target_id="content",
    namespace="inputs", app_name="inputs")

@hypergen_view(url="$^", **HYPERGEN_SETTINGS)
def inputs(request):
    INPUT_TYPES = [
        ("button", d(value="clicked")),
        ("checkbox", d(checked=True)),
        ("color", d(value="#bb7777")),
        ("date", d(value=date(2021, 4, 16))),
        ("datetime-local", d(value=datetime.datetime(1941, 5, 5, 5, 23))),
        ("email", d(value="foo@example.com")),
        ("file", d()),
        ("hidden", d(value="hidden")),
        ("image", d(src="https://picsum.photos/80/40", value="clicked")),
        ("month", d(value=d(year=2099, month=9))),
        ("number", d(title="number (int)", value=99)),
        ("number", d(title="number (float)", value=12.12, js_coerce_func="hypergen.coerce.float")),
        ("password", d(value="1234")),
        ("radio", d(name="myradio", value=20, checked=True, js_coerce_func="hypergen.coerce.int")),
        ("radio", d(name="myradio", value=21, js_coerce_func="hypergen.coerce.int")),
        ("range", d()),
        ("reset", d(value="clicked")),
        ("search", d(value="Who is Rune Kaagaard?")),
        ("submit", d(value="clicked")),
        ("tel", d(value="12345678")),
        ("text", d(value="This is text!")),
        ("time", d(value=datetime.time(7, 42))),
        ("url", d(value="https://github.com/runekaagaard/django-freedom/")),
        ("week", d(value=d(year=1999, week=42))),]

    h1("Showing all input types.")
    with table():
        tr(th(x) for x in ["Input type", "Input attributes", "Element", "Server callback value"])

        for i, pair in enumerate(INPUT_TYPES):
            type_, attrs = pair
            title = attrs.pop("title", type_)
            id_ = "server-value-{}".format(i)

            with tr():
                td(title)
                td(code(attrs))
                submit_cb = cb(submit, THIS, id_)
                td(input_(id_=("element", i), class_="input", type_=type_, oninput=submit_cb, **attrs))
                td(id_=id_)

        with tr():
            i += 1
            id_ = "server-value-{}".format(i)
            attrs = d()
            td("textarea")
            td(code(attrs))
            submit_cb = cb(submit, THIS, id_)
            td(
                textarea("Who is Jeppe Tuxen?", id_=("element", i), class_="input", type_=type_, oninput=submit_cb,
                **attrs))
            td(id_=id_)

        with tr():
            i += 1
            id_ = "server-value-{}".format(i)
            attrs = d(js_coerce_func="hypergen.coerce.int")
            td("select")
            td(code(attrs))
            submit_cb = cb(submit, THIS, id_)
            td(
                select([option(x, value=x, selected=x == 3) for x in range(5)], id_=("element", i), class_="input",
                type_=type_, onclick=submit_cb, oninput=submit_cb, **attrs))
            td(id_=id_)

    script("""
        ready(function() {
            document.querySelectorAll(".input").forEach(el => (el.oninput(new Event("input"))));
        })
    """)

@hypergen_callback(perm=NO_PERM_REQUIRED, namespace="inputs")
def submit(request, value, target_id):
    c.hypergen = c.hypergen.set("target_id", target_id)
    with pre(style={"padding": 0}):
        raw(repr(value), " (", type(value).__name__, ")")
