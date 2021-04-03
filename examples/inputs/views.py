# coding = utf-8
# pylint: disable=no-value-for-parameter
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
        "button", "checkbox", "color", "date", "datetime", "datetime-local", "email", "file", "hidden", "image",
        "month", "number", "password", "radio", "range", "reset", "search", "submit", "tel", "text", "time", "url",
        "week"]

    h1("Showing all input types.")
    with table():
        tr(th(x) for x in ["Input type", "Element", "Server value"])

        for type_ in INPUT_TYPES:
            src, value = "", ""
            if type_ == "image":
                src = "https://picsum.photos/80/40"
                value = "Clicked"
            elif type_ in ["button", "reset", "submit"]:
                value = "Clicked"
            with tr():
                td(type_)
                td(
                    input_(type_=type_, onclick=cb(submit, THIS, type_), oninput=cb(submit, THIS, type_), value=value,
                    src=src))
                td(id_=type_)

@hypergen_callback(**HYPERGEN_SETTINGS)
def submit(request, value, type_):
    def template():
        with pre(style={"padding": 0}):
            raw(repr(value), " (", type(value).__name__, ")")

    return hypergen(template, target_id=type_)
