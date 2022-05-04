# coding=utf-8
import inspect, os, sys
from glob import glob

from django.urls.base import reverse

from hypergen.core import *
from hypergen.core import context as c

from django.templatetags.static import static

### Python 2+3 compatibility ###

def make_string(s):
    # TODO: WHY IS THERE AN IF STATEMENT HERE AT ALL?
    # We had a bug where 0 int did not get rendered. I suck.
    if s or type(s) in (int, float):
        return force_text(s)
    else:
        return ""

if sys.version_info.major > 2:
    from contextlib import contextmanager
else:
    from contextlib2 import contextmanager

def base_head():
    title("Django Hypergen")
    link("https://unpkg.com/simpledotcss/simple.min.css")
    link(href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/default.min.css")
    script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js")
    link(static("website/website.css"))
    script(src=static("website/website.js"))
    link(rel="apple-touch-icon", sizes="120x120", href=static("apple-touch-icon.png"))
    link(rel="icon", type_="image/png", sizes="32x32", href=static("favicon-32x32.png"))
    link(rel="icon", type_="image/png", sizes="16x16", href=static("websitefavicon-16x16.png"))
    link(rel="manifest", href=static("site.webmanifest"))
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
                h1(img(src=static("website/hypergen-logo.png"), class_="logo"), "ypergen - a Django liveview")

            with main():
                yield

            with footer():
                p("Built with Hypergen™ and ", span("❤", style={"color": "red"}))

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

        basedir = os.path.dirname(file_path)
        walked = list(os.walk(basedir))
        for folder, dirs, names in os.walk(basedir):
            for name in names:
                if any(x in name for x in omits):
                    continue

                fp = os.path.join(folder, name)
                title = fp.replace(os.path.dirname(file_path), "").lstrip("/")

                b(title)
                with open(fp) as f:
                    cls = "language-python" if title.endswith(".py") else OMIT
                    pre(code(f.read(), class_=cls))

def show_func(func):
    pre(code(inspect.getsource(func)))
