from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED

from django.templatetags.static import static

@hypergen_view(url="^$", perm=NO_PERM_REQUIRED, translate=True)
def page(request):
    doctype()
    with html():
        with head():
            script(src=static("hypergen/hypergen.min.js"))
        with body(id_="body"):
            template(1)

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id="body")
def increment(request, n):
    template(n + 1)

def template(n):
    h1("Translation")
    p("Hypergen does not have a full translation framework (YET!). What it does have is editable strings.")
    h2("Try to edit these strings by clicking on them")
    small("Use Enter to save your changes and Escape to abort.")
    ul(li(x, id_=x) for x in ("edit this", "edit that", "edit me too"))
    div("But am I?????", div("I'm good"), div("Also mee"))
    input_(value="FOO")
