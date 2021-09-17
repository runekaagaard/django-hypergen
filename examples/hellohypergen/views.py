from contextlib import contextmanager

from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED

from django.templatetags.static import static

@hypergen_view(perm=NO_PERM_REQUIRED)
def counter(request):
    with base_template():
        template(1)

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id="body")
def increment(request, n):
    template(n + 1)

@contextmanager
def base_template():
    doctype()
    with html():
        with head():
            script(src=static("hypergen/hypergen.min.js"))
        with body(id_="body"):
            yield

def template(n):
    label("Current value: ")
    input_(id_="n", type_="number", value=n)
    button("Increment", id_="increment", onclick=cb(increment, n))
