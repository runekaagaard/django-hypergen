from hypergen.core import *
from hypergen.core import callback as cb

from django.urls.base import reverse
from django.templatetags.static import static
from hypergen.core import hypergen_to_response, loads
from website.templates import base_head, show_sources

def counter(request):
    return hypergen_to_response(base_template, template, 0)

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

    h2("Hypergen core only counter")
    p("This is the same as the hellohypergen example, but we are not using the fancy stuff from contrib.py, ",
        "namely the @hypergen_view and @hypergen_callback decorators.")

    with p():
        label("Current value: ")
        input_(type_="number", value=n)
        button("Increment", id_="increment", onclick=cb(reverse("hellocoreonly2:increment"), n))

def increment(request):
    n, = loads(request.POST["hypergen_data"])["args"]

    return hypergen_to_response(template, n + 1, target_id="body")
