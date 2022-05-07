from pprint import pformat

from hypergen.core import *
from hypergen.contrib import hypergen_view, NO_PERM_REQUIRED

from website.templates import base_example_template, show_func

@hypergen_view(perm=NO_PERM_REQUIRED)
def globalcontext(request):
    with base_example_template():
        h2("Global context")
        p("Django requires that the", code("hypergen.core.context_middleware"), "middleware is added to the",
            code("MIDDLEWARE"), "variable in settings.py:", sep=" ")
        pre(code("""
MIDDLEWARE = [
    ...
    'hypergen.core.context_middleware',
    ...
]
        """.strip()))

        p("It adds an immutable global ",
            a("data structure", href="https://pyrsistent.readthedocs.io/en/latest/api.html#pyrsistent.pmap"),
            " that is local to the request. ",
            "It's used throughout hypergen to collect html and several other features. Get at it like so:")
        pre(
            code("""
from hypergen.core import context
print(context.request) # The middleware adds the request.
        """.strip()))
        p("It's available to users too, although the names 'request', 'hypergen', 'users', 'appstate' ",
            "and 'base_template' are reserved for ",
            "internal use. Some of these will be removed in a future release.")
        p("Heres whats in", code("context.hypergen.into"), "right now for an example:", sep=" ")
        pre(code(pformat(context.hypergen.into), style={"max-height": "250px", "overflow-y": "scroll"}))

        h3("Using global context in your own apps")
        p("You can use your own global context like this example:")

        show_func(context_example)

        p("And it would yield the following html:")
        context_example()

def context_example():
    with context(at="my_appname", title="my original items", items=[1, 2, 3]):
        with dl():
            dt(context["my_appname"]["title"])
            dd(context["my_appname"]["items"], sep=", ")

            with context(at="my_appname", title="my nested items", items=[4, 5]):
                dt(context["my_appname"]["title"])
                dd(context["my_appname"]["items"], sep=", ")

            dt(context.my_appname["title"])
            dd(context.my_appname["items"], sep=", ")
