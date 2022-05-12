# coding = utf-8
# pylint: disable=no-value-for-parameter
d = dict
import datetime
from collections import namedtuple
from django.urls.base import reverse
from hypergen.core import COERCE, JS_COERCE_FUNCS, JS_VALUE_FUNCS

from yapf.yapflib.yapf_api import FormatCode

from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED
from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.core import context as c

from website.templates import base_template, show_sources

E = namedtuple("E", 'type,attrs,doc')
E.__new__.__defaults__ = (None,) * 3  # default keyword not in py3.6

@hypergen_view(url="^$", perm=NO_PERM_REQUIRED, base_template=base_template)
def inputs(request):
    INPUT_TYPES = [
        E("checkbox", d(checked=True)),
        E("color", d(value="#bb7777")),
        E(
        "date", d(value=datetime.date(2021, 4, 16)),
        "Takes a datetime. Date, datetime-local, month, time and week fields also accepts the string representation as input value. They will return the python object on the server though."
        ),
        E("datetime-local", d(value=datetime.datetime(1941, 5, 5, 5, 23)), "Takes a datetime."),
        E("email", d(value="foo@example.com")),
        E("file", d()),
        E("hidden", d(value="hidden")),
        E("month", d(value=d(year=2099, month=9)), "Takes a dict with year and month."),
        E("number", d(title="number (int)", value=99)),
        E("number", d(title="number (float)", value=12.12, coerce_to=float), "Coercing to float here."),
        E("password", d(value="1234")),
        E("radio", d(name="myradio", value=20, checked=True, coerce_to=int),
        "Set the same name for radio groups. Notice the coercion to int."),
        E("radio", d(name="myradio", value=21, coerce_to=int)),
        E("range", d()),
        E("search", d(value="Who is Rune Kaagaard?")),
        E("tel", d(value="12345678")),
        E("text", d(value="This is text!")),
        E("time", d(value=datetime.time(7, 42)), "Takes a datetime.time value."),
        E("url", d(value="https://github.com/runekaagaard/django-hypergen/")),
        E("week", d(value=d(year=1999, week=42)), "Takes a dict with year and week."),]

    CLICK_TYPES = [
        ("button", d(value="clicked")),
        ("image", d(src="https://picsum.photos/80/40", value="clicked")),
        ("reset", d(value="clicked")),
        ("submit", d(value="clicked")),]

    with p():
        a("Back to documentation", href=reverse("website:documentation"))

    h2("Form Input elements")
    p(
        "Hypergen has special support for input, select and textarea elements. They can be used as arguments to ",
        "callback functions. When the event the callback is attached to happens, the frontend will read their values and send them as arguments to the callback functions."
    )
    p("As an example try to experiment with what this code would send to the server:")
    pre(
        code("""
inputs = [
    input_(id_="i1", value=1, type_="number"),
    input_(id_="i2", value=2, type_="number", coerce_to=float),
    input_(id_="i3", value=None, type_="number", coerce_to=str),]
i4 = input_(id_="i4", value=4)
button("send to server", onclick=cb(mycallback, inputs, {"myi4": i4}), id_="mycallback-send")
    """.strip()))
    with p():
        inputs = [
            input_(id_="i1", value=1, type_="number"),
            input_(id_="i2", value=2, type_="number", coerce_to=float),
            input_(id_="i3", value=None, type_="number", coerce_to=str),]
        i4 = input_(id_="i4", value=4)
        button("send to server", onclick=cb(mycallback, inputs, {"myi4": i4}), id_="mycallback-send")
        span(id_="mycallback-receive")

    p("The fact that multiple inputs can be nested into your datastructure of choice and sent to the server ",
        "allows for very flexible workflows.")

    dl(
        em("class input_(coerce_to=None, js_value_func=None, js_coerce_func=None)"),
        p("Renders an html5 <input /> tag. select() and textarea() works the same."),
        dt("coerce_to"),
        dd('Takes the following builtin types: ', span([x.__name__ for x in list(COERCE.keys())], sep=", "), "."),
        dt("js_value_func"),
        dd("Se below"),
        dt("js_coerce_func"),
        dd("Se below"),
    )

    with details():
        summary("Low level value reading and value coercion")
        p("Input elements has useful defaults for reading the value",
            "of the different input types and to which datatype to coerce the read value.",
            "Value reading and value coercion can be overridden by the js_value_func and js_coerce_func kwargs.",
            "Their values should exist as a dotted path on the frontend.", sep=" ")
        p("These are the default values for js_value_func by element type: ")
        with dl():
            for k, v in list(JS_VALUE_FUNCS.items()):
                dt(k)
                dd(v)
            dt("everything else")
            dd("hypergen.read.value")

        p("And similarly for js_coerce_func:")
        with dl():
            for k, v in list(JS_COERCE_FUNCS.items()):
                dt(k)
                dd(v)
        p("Check hypergen.js to see their definitions. Should you wish to implement a custom html tag you would ",
            "probably change these. Otherwise the default settings should be sufficient.")

    h2("Examples for all HTML5 input types.")
    p("Interact with the form elements below to see which data is send to the server.")

    with table():
        tr(th(x) for x in ["Input type", "Code", "Rendered", "Server callback value"])
        tr(
            td(x) for x in [
            "", "This is the __repr__ representations of the hypergen input elements, which coincidentally"
            " looks a lot like python code :)", "",
            "The data received on the server when the relevant onXXX events are triggered."])

        for i, pair in enumerate(INPUT_TYPES):
            type_, attrs, doc = pair
            title = attrs.pop("title", type_)
            id_ = "server-value-{}".format(i)

            with tr():
                submit_cb = cb(submit, THIS, id_)
                el = input_(id_=("element", i), type_=type_, oninput=submit_cb, **attrs)
                th(title)
                td(pre(code(FormatCode(repr(el))[0])), p(doc) if doc else "")
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

    show_sources(__file__)

@hypergen_callback(perm=NO_PERM_REQUIRED)
def submit(request, value, target_id):
    c.hypergen = c.hypergen.set("target_id", target_id)
    with pre(style={"padding": 0}):
        raw(repr(value), " (", type(value).__name__, ")")

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id="mycallback-receive")
def mycallback(request, a1, a2):
    span(" Executed on server: ")
    with code():
        raw("mycallback(request, {}, {})".format(repr(a1), repr(a2)))
