from copy import deepcopy
from django.http.response import HttpResponse
from hypergen.core import *
from hypergen.core import callback as cb

from django.urls.base import reverse
from django.templatetags.static import static
from hypergen.core import hypergen_to_response, loads, dumps
from website.templates import base_head, show_sources

def counter(request):
    html = hypergen(base_template, template, 0)  # hypergen returns html because it's not an ajax request.

    return HttpResponse(html)

def base_template(content_template, n):
    doctype()
    with html():
        with head():
            script(src=static("hypergen/hypergen.min.js"))
            base_head()
        with body():
            with div(id_="body"):
                content_template(n)

            show_sources(__file__)

def template(n):
    p(a("Back to documentation", href=reverse("website:documentation")))

    h2("Hypergen core only counter 2")
    p("This is using even less helper function than hello core only 1.")

    with p():
        label("Current value: ")
        input_(type_="number", value=n)
        button("Increment", id_="increment", onclick=cb(reverse("hellocoreonly2:increment"), n))

def increment(request):
    n, = loads(request.POST["hypergen_data"])["args"]

    # Because it's an ajax request hypergen returns a list of client commands.
    list_of_commands = hypergen(template, n + 1, target_id="body")
    # Lets console log the list of commands and alert the user.
    list_of_commands.append(["alert", "The list of commands received from the server can be seen in the js console."])
    list_of_commands.append(["console.log", "list of commands:", deepcopy(list_of_commands)])

    return HttpResponse(dumps(list_of_commands), status=200, content_type='application/json')
