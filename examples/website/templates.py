# coding=utf-8
import os
from glob import glob
from django.urls.base import reverse

from hypergen.core import *
from hypergen.core import context as c

from django.templatetags.static import static
from contextlib import contextmanager

def base_head():
    title("Django Hypergen")
    link("https://unpkg.com/simpledotcss/simple.min.css")
    link(href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/default.min.css")
    script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js")
    link(static("website/website.css"))
    script(src=static("website/website.js"))

@contextmanager
def base_template():
    doctype()
    with html():
        with head():
            script(src=static("hypergen/hypergen.min.js"))
            base_head()

        with body():
            with header():
                with nav():
                    a("Home", href="/", class_="current" if c.request.path == "/" else OMIT)
                    a("Examples", href="/examples/", class_="current" if c.request.path == "/examples/" else OMIT)
                    a("Documentation", onclick='alert("To be done")')
                    a("Support", href="https://github.com/runekaagaard/django-hypergen/issues")
                    with a(href="https://github.com/runekaagaard/django-hypergen/"):
                        img(src=static("website/github.png"), class_="icon")
                        raw("Github")
                h1("Hypergen - a Django liveview")

            with main():
                yield

@contextmanager
def base_example_template():
    with base_template():
        with p():
            a("Back to examples", href=reverse("website:examples"))

        yield

def show_sources(file_path):
    omits = ("__", "migrations", ".css", "commands", ".so", "gameofcython.html", ".cpp", ".png")

    hr()
    with details():
        summary("Show sources")

        for fp in reversed(glob(os.path.dirname(file_path) + "/**/*.*", recursive=True)):
            if any(x in fp for x in omits):
                continue
            title = fp.replace(os.path.dirname(file_path), "").lstrip("/")

            b(title)
            with open(fp) as f:
                cls = "language-python" if title.endswith(".py") else OMIT
                pre(code(f.read(), class_=cls))
