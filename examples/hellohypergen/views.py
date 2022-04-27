from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED

from django.urls.base import reverse
from django.templatetags.static import static
from website.templates import base_head, show_sources

def template(n):
    with p():
        a("Back to examples", href=reverse("website:examples"))
    with p():
        label("Current value: ")
        input_(id_="n", type_="number", value=n)
        button("Increment", id_="increment", onclick=cb(increment, n))

@hypergen_view(url="^$", perm=NO_PERM_REQUIRED)
def counter(request):
    doctype()
    with html():
        with head():
            script(src=static("hypergen/hypergen.min.js"))
            base_head()
        with body(), div(id_="body"):
            template(1)
            show_sources(__file__)

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id="body")
def increment(request, n):
    template(n + 1)
