from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED

from django.templatetags.static import static

@hypergen_view(perm=NO_PERM_REQUIRED)
def counter(request):
    doctype()
    with html():
        with head():
            script(src=static("hypergen/hypergen.min.js"))
        with body():
            with div(id_="body"):
                template(1)

def template(n):
    with p():
        label("Current value: ")
        input_(type_="number", value=n)
        button("Increment", id_="increment", onclick=cb(increment, n))

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id="body")
def increment(request, n):
    template(n + 1)
