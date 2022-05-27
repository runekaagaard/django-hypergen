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
            script(src=static("hypergen/hypergen.min.js"))
            base_head()
        with body():
            with div(id_="content"):
                content_template(n)

            show_sources(__file__)

def template(n):
    p(a("Back to documentation", href=reverse("website:documentation")))

    h2("Hypergen core only counter")
    p("This is the same as the hellohypergen example, but we are not using the fancy stuff from contrib.py, ",
        "namely the @hypergen_view and @hypergen_callback decorators and the hypergen_urls function.")
    p("There is an", a("even more low level example", href=reverse("hellocoreonly2:counter")), "available as well.",
        sep=" ")

    with p():
        label("Current value: ")
        input_(type_="number", value=n)
        button("Increment", id_="increment", onclick=callback(reverse("hellocoreonly:increment"), n))

def increment(request):
    n, = loads(request.POST["hypergen_data"])["args"]

    commands = hypergen(template, n + 1, settings={"action": True, "target_id": "content", "returns": COMMANDS})
    return HttpResponse(dumps(commands), status=200, content_type='application/json')
