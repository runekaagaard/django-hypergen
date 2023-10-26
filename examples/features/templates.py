from contextlib import contextmanager
import inspect

from hypergen.imports import *

from django.templatetags.static import static

from features.consts import *

def main():
    link(static("features.css"))

    h2("Features")
    with div(id="features"):
        feature(0)

def feature(n):
    from features import views
    with div(id="features-navigation", class_="grid2"):
        with div(class_="buttons"):
            a(i(class_="bi-arrow-left-circle"), href="#", class_="", id="features-prev",
                onclick=callback(views.feature, n - 1))
            a(i(class_="bi-arrow-right-circle"), href="#", class_="", id="features-next",
                onclick=callback(views.feature, n + 1))
        with div(class_="fr"):
            small(n + 1, "of", len(FEATURES), sep=" ")

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
    from hypergen.template import component

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
    from contextlib import contextmanager

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
                - modules
                - packages
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

                Write dynamic websites in pure python

                - No javascript code 
                - No serialization
                - No magic liveview strings
                - Use all the nice features of Django
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
    "Use WASD to navigate"
    @liveview(...)
    def snake(request):
        snake_url = ws_url("/ws/snake-consumer/")
        command("hypergen.websocket.open", snake_url)
        with div(id="snake-game"):
            templates.snake()

    class SnakeConsumer(HypergenWebsocketConsumer):
        ...

        def receive_callback(self, key):
            self.snake_game(key)

def f4():
    with div(class_="grid3"):
        cell_text("""
                Websockets
                =========

                Realtime two-way communication

                - Inbuilt opening/closing of websockets
                - Send client commands within consumers
            """)

        cell_code(fcode(f4_code), "views.py")

        with cell_full(), div(id="snake-game"):
            snake()

def snake_init(n):
    from features import views
    snake_url = ws_url("/ws/features/snake-consumer/")

    if n == 3:
        command("hypergen.websocket.open", snake_url)
        command("hypergen.intervalSet", [["hypergen.callback", snake_url, [None]]], 1000 / 10, "snake")
        command("hypergen.keypressToCallback", snake_url)
    else:
        command("hypergen.websocket.close", snake_url)
        command("hypergen.intervalClear", "snake")
        command("hypergen.keypressToCallbackRemove", snake_url)

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

# f5 - plugins

def f5_code():
    from hypergen.plugins import AlertifyPlugin

    @action(..., user_plugins=[AlertifyPlugin()])
    def my_action(request):
        messages.warning(request, "Uh-oh!")

def f5_template(text):
    from features import views
    input_(id="f5-i", type="button", value="Click me!", onclick=callback(views.alert))

def f5():
    with div(class_="grid3"):
        cell_code(fcode(f5_code), "views.py")

        cell_text("""
                Plugins
                =========

                Extend hypergens functionality with powerful plugins

                - Hypergen dogfoods plugins by writing liveview as a plugin
                - Plugins can have their open immutable state using context()
            """)

        with cell(""):
            with div(class_="running", id="f3"):
                f5_template("")

FEATURES = [f1, f2, f3, f4, f5]
