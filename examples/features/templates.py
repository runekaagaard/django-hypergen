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
        feature(len(FEATURES) - 1)

def feature(n):
    from features import views
    with div():
        a("🢨", href="1", class_="selected nul", id="features-prev", onclick=callback(views.feature, n - 1))
        a("🢩", href="2", class_="selected nul", id="features-next", onclick=callback(views.feature, n + 1))
        small(n + 1, "of", len(FEATURES), sep=" ", class_="fr")

    snake_init(n)

    FEATURES[n]()

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

@contextmanager
def cell_full():
    with div(class_="cell-full"), div(class_=""), div():
        yield

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

    def template(form):
        for fields in form:
            form_field(form_field)

def f2_code2():
    @contextmanager
    def card(title):
        with div(class_="card"):
            h4(title)
            with div(class_="footer"):
                yield

    def template(person):
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

# feature3

# yapf: disable
def f3_code():
    def template(text):
        input(id="text",
              oninput=callback(
                reverser,
                THIS)
        )

        p(text)

    @liveview(...)
    def reverse_text(request):
        template("")

    @action(...)
    def reverser(request, text):
        template(text[::-1])

# yapf: enable

def f3_code2():
    "Cool"

def f3():
    with div(class_="grid3"):
        cell_code(fcode(f3_code), "views.py")

        cell_text("""
                Liveviews
                =========

                Write dynamic websites effortlessly

                - Everything lives on the backend
                - No frontend
                - Single source of truth
            """)

        with cell(""):
            with div(class_="running", id="f3"):
                f3_template("")

def f3_template(text):
    from features import views
    input_(id="f3-i", placeholder="Write here...", oninput=callback(views.reverser, THIS))

    with p():
        if text:
            write(text[::-1])
        else:
            raw("&nbsp;")

# f4 - snake
def f4_code():
    "WASD to navigate"

def f4():
    with div(class_="grid3"):
        cell_text("""
                Websockets
                =========

                Need faster two way communication?

                - @consumer
                - Same features as @action
                - Fun
            """)

        cell_code(fcode(f4_code), "")

        with cell_full(), div(id="snake-game"):
            snake()

def snake_init(n):
    from features import views
    if n == 3:
        command("hypergen_websockets.open", views.snake.reverse())
        command("hypergen.intervalSet", [["hypergen.callback", views.snake.reverse(), [None]]], 1000 / 10, "snake")
        command("hypergen.keypressToCallback", views.snake.reverse())
    else:
        command("hypergen_websockets.close", views.snake.reverse())
        command("hypergen.intervalClear", "snake")
        command("hypergen.keypressToCallbackRemove", views.snake.reverse())

def snake(consumer=None):
    with table():
        for y in range(0, 20):
            with tr():
                for x in range(0, 20):
                    if not consumer:
                        td(class_="b")
                    else:
                        if (x, y) in consumer.fruit:
                            cls = "r"
                        else:
                            cls = "g" if (x, y) in consumer.state else "b"
                        td(class_=cls)

FEATURES = [f1, f2, f3, f4]
