from hypergen.imports import *

from django.urls.base import reverse
from django.templatetags.static import static
from django.http.response import HttpResponse

from website.templates2 import base_head, show_sources

def counter(request):
    return HttpResponse(hypergen(base_template, template, 0, settings={"liveview": True}))

def base_template(content_template, n):
    doctype()
    with html():
        with head():
            base_head()
        with body():
            with div(id_="content"):
                content_template(n)

            show_sources(__file__)

def template(n):
    p(a("Back to documentation", href=reverse("website:documentation")))

    h2("Hypergen core only counter")
    p("This is the same as the hellohypergen example, but we are not using the fancy stuff, ",
        "namely the @liveview and @action decorators and the autourls function.")

    with p():
        label("Current value: ")
        input_(type_="number", value=n)
        button("Increment", id_="increment", onclick=callback(reverse("hellocoreonly:increment"), n))

def increment(request):
    n, = loads(request.POST["hypergen_data"])["args"]

    commands = hypergen(template, n + 1, settings={"action": True, "target_id": "content", "returns": COMMANDS})
    return HttpResponse(dumps(commands), status=200, content_type='application/json')
