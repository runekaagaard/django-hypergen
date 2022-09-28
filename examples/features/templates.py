from contextlib import contextmanager
import inspect

from hypergen.imports import *

from django.templatetags.static import static

from features.consts import *

def main():
    link("https://highlightjs.org/static/demo/styles/base16/monokai.css")
    link(static("features.css"))

    h2("Features")
    with div(id="features"):
        feature(0)

def feature(n):
    from features import views
    FEATURES[n]()

    with div():
        a("🢨", href="1", class_="selected nul", id="features-prev", onclick=callback(views.feature, n - 1))
        a("🢩", href="2", class_="selected nul", id="features-next", onclick=callback(views.feature, n + 1))
        small(n + 1, "of", len(FEATURES), sep=" ", class_="fr")

def fcode(func):
    s = inspect.getsource(func)
    s = s.replace("\n    ", "\n")
    s = "\n".join(s.splitlines()[1:])

    return s

# pre(code(hypergen(func, settings=dict(indent=True))))

@contextmanager
def cell(title):
    with div(class_="cell"):
        div(h4(title), class_="header")
        with div(class_="inner"):
            yield

def cell_text(s):
    with div(class_="cell tc"), div(class_="inner-full"), div():
        rst(ri(s))

@component
def cell_code(s, title=None):
    with cell(title):
        inner_code(s)

@component
def inner_code(s):
    with pre():
        code(s)

def ri(s):
    l1 = s.splitlines()[1]
    s2 = " " * (len(l1) - len(l1.lstrip(" ")))

    return s.replace("\n" + s2, "\n")

# feature1

def f1_code():
    with table(class_="striped"):
        tr(th("n"), th("squared"))
        for n in range(1, 4):
            with tr():
                td(n)
                td(n * n)

def f1():
    with div(class_="grid3"):
        cell_code(fcode(f1_code), "Hypergen")

        cell_text("""
                Write HTML in pure python
                =========================

                Build templates in a turing complete language

                - conditionals
                - loops
                - with statements
                - djangos ORM
            """)

        cell_code(F1, "HTML")

# features

def f2_code():
    @component
    def form_field(field):
        with div(class_="form-group"):
            label(field.label)
            input_(
                type=field.type,
                value=field.value(),
            )

    def my_template(form):
        for fields in form:
            form_field(form_field)

def f2_code2():
    @contextmanager
    def card(title):
        with div(class_="card"):
            h4(title)
            with div(class_="footer"):
                yield

    def my_template(person):
        with card(person.name):
            button("Show details")

def f2():
    with div(class_="grid3"):
        cell_code(fcode(f2_code), "Component")

        cell_text("""
                Composable
                ==========

                Compose your templates with ... tadaaaah ... python

                - functions
                - modules & packages
                - @component
                - @contextmanager
            """)

        cell_code(fcode(f2_code2), "Context manager")

FEATURES = [f1, f2]
