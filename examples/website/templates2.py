# coding=utf-8
import inspect
import os
from glob import glob
from django.urls.base import reverse

from hypergen.imports import *
from hypergen.context import context as c

from django.templatetags.static import static
from contextlib import contextmanager

def base_head(monokai=False):
    meta(charset="utf-8")
    meta(http_equiv="X-UA-Compatible", content="IE=edge")
    meta(name="viewport", content="width=device-width, initial-scale=1.0")
    title("Django Hypergen")
    link("https://unpkg.com/simpledotcss@2.0.7/simple.min.css")
    script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.6.0/highlight.min.js")
    link("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css")
    link(static("website/website.css"))
    script(src=static("website/website.js"), defer=True)
    link(rel="apple-touch-icon", sizes="120x120", href=static("apple-touch-icon.png"))
    link(rel="icon", type_="image/png", sizes="32x32", href=static("favicon-32x32.png"))
    link(rel="icon", type_="image/png", sizes="16x16", href=static("favicon-16x16.png"))
    link(rel="mask-icon", href=static("safari-pinned-tab.svg"), color="#5bbad5")
    meta(name="msapplication-TileColor", content="#da532c")
    meta(name="theme-color", content="#ffffff")
    if monokai:
        link(href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/monokai-sublime.min.css")
    else:
        link(href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.6.0/styles/default.min.css")

@contextmanager
def base_template(monokai=False):
    doctype()
    with html():
        with head():
            base_head(monokai=monokai)

        with body():
            with header():
                with nav():
                    a("Home", href="/", class_="current" if c.request.path == "/" else OMIT)
                    a("Documentation", href="/documentation/",
                        class_="current" if c.request.path == "/documentation/" else OMIT)
                    a("News", href="/news/", class_="current" if c.request.path == "/news/" else OMIT)
                    with a(href="https://github.com/runekaagaard/django-hypergen/"):
                        img(src=static("website/github.png"), class_="icon")
                        raw("Github")
                with div(class_="title"):
                    h1(img(src=static("website/hypergen-logo.png"), class_="logo"), "ypergen")
                    span(" - take a break from javascript")

            with main(id_="main" if not monokai else "main-monokai"):
                yield

            with footer():
                p("Built with Hypergen, ", a("Simple.css", href="https://simplecss.org/", style={"color": "inherit"}),
                    " and ", span("❤", style={"color": "red"}))

base_template.target_id = "main"

@contextmanager
def base_template_monokai():
    with base_template(monokai=True):
        yield

base_template_monokai.target_id = "main-monokai"

@contextmanager
def base_example_template(file_=None):
    with base_template():
        with p():
            a("Back to documentation", href=reverse("website:documentation"))

        with div(id_="content"):
            yield

        if file_:
            show_sources(file_)

def doc_base_template(file_=None, target_id="content"):
    @contextmanager
    def _doc_base_template(file_=None):
        with base_template():
            with p():
                a("Back to documentation", href=reverse("website:documentation"))

            with div(id_=target_id):
                yield

            if file_:
                show_sources(file_)

    _doc_base_template.target_id = target_id

    return _doc_base_template

base_example_template.target_id = "content"

def show_sources(file_path):
    omits = ("__", "migrations", ".css", "management", ".so", "gameofcython.html", ".cpp", ".png", ".svg", ".ico",
        "webmanifest", "jpg", ".xml", ".svg", ".mp3")

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
