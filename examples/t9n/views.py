from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED

from django.urls.base import reverse

from website.templates import base_template

@hypergen_view(url="^$", perm=NO_PERM_REQUIRED, translate=True)
def page(request):
    with base_template():
        template()

@hypergen_callback(perm=NO_PERM_REQUIRED, translate=True, target_id="body")
def reload(request):
    template()

def template():
    p(a("Back to examples", href=reverse("website:examples")))

    h2("Translation")
    p("Hypergen does not have a full translation framework (YET!). What it does have is editable strings.")
    p(
        "Use ctrl+shift+1 or command+shift+1 to toggle translation mode and then try to edit these strings"
        " by clicking on them. Enter the text 'RESET' to reset to the original value. ",
        "Use enter to commit and escape to cancel.")
    p("Use Enter to save your changes and Escape to abort. "
        "But you will have to be ", a("logged in", href="/admin/"),
        " and have the permission hypergen.kv_hypergen_translations.", id_="foo")
    ul(li(x, id_=x) for x in ("edit this", "edit that", "edit me too"))
    h2("How does it work?")
    p("Hypergen persists the translation strings in the ", a("Key/Value model", href="/admin/hypergen/kv/"),
        " and keeps the strings cached in memory for a very fast performance.")

    button("Reload", id_="reload", onclick=cb(reload))
