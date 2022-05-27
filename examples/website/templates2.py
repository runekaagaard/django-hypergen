# coding=utf-8
import inspect
import os
from glob import glob
from django.urls.base import reverse

from hypergen.imports import *

from django.templatetags.static import static
from contextlib import contextmanager

def base_head():
    meta(charset="utf-8")
    meta(http_equiv="X-UA-Compatible", content="IE=edge")
    meta(name="viewport", content="width=device-width, initial-scale=1.0")
    title("Django Hypergen")
    link("https://unpkg.com/simpledotcss@2.0.7/simple.min.css")
    link(href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/default.min.css")
    script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js")
    link(static("website/website.css"))
    script(src=static("website/website.js"), defer=True)
    link(rel="apple-touch-icon", sizes="120x120", href=static("apple-touch-icon.png"))
    link(rel="icon", type_="image/png", sizes="32x32", href=static("favicon-32x32.png"))
    link(rel="icon", type_="image/png", sizes="16x16", href=static("favicon-16x16.png"))
    link(rel="mask-icon", href=static("safari-pinned-tab.svg"), color="#5bbad5")
    meta(name="msapplication-TileColor", content="#da532c")
    meta(name="theme-color", content="#ffffff")

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
                    a("Documentation", href="/documentation/",
                        class_="current" if c.request.path == "/documentation/" else OMIT)
                    a("Support", href="https://github.com/runekaagaard/django-hypergen/issues")
                    with a(href="https://github.com/runekaagaard/django-hypergen/"):
                        img(src=static("website/github.png"), class_="icon")
                        raw("Github")
                with div(class_="title"):
                    h1(img(src=static("website/hypergen-logo.png"), class_="logo"), "ypergen")
                    span(" - take a break from javascript")

            with main(id_="main"):
                yield

            with footer():
                p("Built with Hypergen, ", a("Simple.css", href="https://simplecss.org/", style={"color": "inherit"}),
                    " and ", span("❤", style={"color": "red"}))

base_template.target_id = "main"

@contextmanager
def base_example_template():
    with base_template():
        with p():
            a("Back to documentation", href=reverse("website:documentation"))

        with div(id_="content"):
            yield

def show_sources(file_path):
    omits = ("__", "migrations", ".css", "management", ".so", "gameofcython.html", ".cpp", ".png", ".svg", ".ico",
        "webmanifest", "jpg", ".xml")

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

def show_func(func):
    pre(code(inspect.getsource(func)))
