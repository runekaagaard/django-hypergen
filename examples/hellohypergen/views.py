# Import all html tag functions, etc.
from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED

from django.urls.base import reverse
from django.templatetags.static import static
from website.templates import base_head, show_sources

# So this a hypergen view. If no "url" parameter is given one will be automatically assigned. "perm" is required.
# A LOT of stuff happens under the hood and the decorator can be configured in many ways. Just go with it for now.
@hypergen_view(perm=NO_PERM_REQUIRED)
def counter(request):
    # hypergen_view collects html and returns it as a Django response.
    doctype()  # standard html5 doctype.
    with html():  # tags can be nested
        with head():
            script(src=static("hypergen/hypergen.min.js"))  # html attributes are keyword arguments.
            base_head()
        with body():
            # This id matches the "target_id" argument to the "increment" callback.
            with div(id_="body"):
                # Render the dynamic content of the page. This happens in it's own function so that functionality
                # can be shared between the view and the callback.
                template(1)

            show_sources(__file__)

# Hypergen html is very easy to compose, just use functions.
def template(n):
    # Tags can take other tags as arguments.
    p(a("Back to examples", href=reverse("website:examples")))

    h2("Hypergen counter")
    p('When you click "increment" the server tells the client to update the content on the page using morphdom.',
        "Event binding, ajax calls, routing, (de)serialization, page updating, back button support, "
        "etc. we get for free from hypergen.", sep=" ")  # joins by " ".

    with p():
        label("Current value: ")
        # Names that clashes with python inbuilts are postfixed with a "_".
        input_(type_="number", value=n)
        # When this button is clicked it will call the "increment" function on the server with "n" as it's first
        # argument after the request. All normal python types, dicts, lists, dates, etc. will be automatically
        # serialized and deserialized between server and client.
        #
        # Elements with callbacks _must_ have an id.
        button("Increment", id_="increment", onclick=cb(increment, n))

# And this is a hypergen callback. It's the ajax brother to the hypergen_view. "perm" and "target_id" are required.
# "target_id" is where the output of "template(n+1)" will be written to on the client.
@hypergen_callback(perm=NO_PERM_REQUIRED, target_id="body")
def increment(request, n):
    # Increment "n" and render again.
    template(n + 1)
