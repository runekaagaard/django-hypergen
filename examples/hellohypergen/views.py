# Import all html tag functions, etc.
from hypergen.imports import *

from django.urls.base import reverse
from website.templates2 import base_head, show_sources

# So this a hypergen liveview. If no "path" parameter is given one will be automatically assigned. "perm" is required.
# A LOT of stuff happens under the hood and the decorator can be configured in many ways. Just go with it for now.
@liveview(perm=NO_PERM_REQUIRED)
def counter(request):
    # @liveview collects html and returns it as a Django response.
    doctype()  # standard html5 doctype.
    with html():  # tags can be nested
        with head():
            base_head()  # makes the site look good. Not important.
        with body():
            # This id matches the "target_id" argument to the "increment" callback.
            with div(id_="content"):
                # Render the dynamic content of the page. This happens in it's own function so that functionality
                # can be shared between the view and the callback.
                template(1)

            show_sources(__file__)
            # hypergen automatically injects it's needed javascript just before the </body> tag.

# Hypergen html is very easy to compose, just use functions.
def template(n):
    # Tags can take other tags as arguments.
    p(a("Back to documentation", href=reverse("website:documentation")))

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
        button("Increment", id_="increment", onmousedown=callback(increment, n))

# And this is an hypergen action. It's the ajax brother to the @liveview. "perm" is required.
# "target_id" is the DOM element id where "template(n+1)" will be written to on the client.
@action(perm=NO_PERM_REQUIRED, target_id="content")
def increment(request, n):
    # Increment "n" and render again.
    template(n + 1)
