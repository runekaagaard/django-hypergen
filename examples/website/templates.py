# coding=utf-8
d = dict

from django.templatetags.static import static

from contextlib import contextmanager
from hypergen.core import *
from hypergen.core import context as c

@contextmanager
def base_template():
    doctype()
    with html():
        with head():
            title("Django Hypergen")
            script(src=static("hypergen/hypergen.min.js"))
            link("https://unpkg.com/simpledotcss/simple.min.css")
            link(href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/default.min.css")
            script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js")
            link(static("website/website.css"))
            script(src=static("website/website.js"))

        with body():
            with header():
                with nav():
                    a("Home", href="/", class_="current" if c.request.path == "/" else OMIT)
                    a("Examples", href="/examples/", class_="current" if c.request.path == "/examples/" else OMIT)
                    a("Documentation", href="https://readthedocs.com/TODOTODOTODO")
                    a("Support", href="https://github.com/runekaagaard/django-hypergen/issues")
                    with a(href="https://github.com/runekaagaard/django-hypergen/"):
                        img(src=static("website/github.png"), class_="icon")
                        raw("Github")
                h1("Hypergen - a Django liveview")

            with main():
                yield
