from contextlib import contextmanager
import codecs
from django.http.response import HttpResponse

from hypergen.core import *
from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED

from django.templatetags.static import static

@hypergen_view(perm=NO_PERM_REQUIRED)
def sink(request):
    section(
        [1, 2, 3],
        (x for x in [4, 5, 6]),
        7,
        lambda: 8,
        b(9),
        sep=" ",
        end=".",
    )
    hr()

    div(a=OMIT, b=True, c=False, d=None, style={"background_color": "green"}, class_=["p1", "p2", "p3"],
        id_=("mymodel", "42"))
    hr()

    ul(li(x) for x in range(1, 4))
    hr()

    p("I am good.", "So am I.", "But what", code("about this"), sep=" ", end=".")

def my_view(request):
    return hypergen_to_response(my_template, "hypergen")
    return HttpResponse(hypergen(my_template, "hypergen"))

def my_template(name):
    doctype()
    with html():
        with body():
            p("Hello ", name)
