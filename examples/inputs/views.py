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
        "month", "number (int)", "number (float)", "password", "radio", "range", "reset", "search", "submit", "tel",
        "text", "time", "url", "week"]

    h1("Showing all input types.")
    with table():
        tr(th(x) for x in ["Input type", "Element", "Server value"])

        for i, type_ in enumerate(INPUT_TYPES):
            src, value, step = OMIT, OMIT, OMIT
            id_ = "server-value-{}".format(i)
            if "number" in type_:
                if type_ == "number-float":
                    step = "any"
                type_ = "number"

            elif type_ == "image":
                src = "https://picsum.photos/80/40"
                value = "Clicked"
            elif type_ in ["button", "reset", "submit"]:
                value = "Clicked"
            with tr():
                td(type_)
                submit_cb = cb(submit, THIS, id_)
                td(
                    input_(id_=("element", i), class_="input", type_=type_, onclick=submit_cb, oninput=submit_cb,
                    value=value, src=src, step=step))
                td(id_=id_)

    script("""

    """)

@hypergen_callback(view=inputs, **HYPERGEN_SETTINGS)
def submit(request, value, target_id):
    return
    c.hypergen = c.hypergen.set("target_id", target_id)
    with pre(style={"padding": 0}):
        raw(repr(value), " (", type(value).__name__, ")")
