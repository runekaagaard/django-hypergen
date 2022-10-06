import operator

from hypergen.imports import *
from hypergen.context import context as c
from hypergen.templatetags.hypergen import render_to_hypergen

from django.shortcuts import render

from hypergen.incubation import SessionVar
from website.templates2 import show_sources

STACK = SessionVar("STACK", [])  # This variable lives in the session data.

# djangotemplates is a vanilla Django view, with it's route defined in urls.py.
# It's decorated with @liveview to enable liveview capabilities.
@liveview(perm=NO_PERM_REQUIRED, autourl=False)
def djangotemplates(request):
    return render(request, "djangotemplates/content.html", context=dict(stack=STACK.get(),
        sources=hypergen(show_sources, __file__)))

def render_content():
    # render_to_hypergen() works exactly as Djangos render_to_string except for two things:
    #     1. It writes the HTML directly to the page.
    #     2. It supports a "block" keyword argument so that only the content of that block is rendered.
    render_to_hypergen("djangotemplates/content.html", context=dict(stack=STACK.get(),
        sources=hypergen(show_sources, __file__)), block="content")

###  ACTIONS ###
# @actions works exactly like vanilla hypergen actions, so the hypergen template language is enabled.
# Here we choose to use render_context to partially render a Django html template.

@action(perm=NO_PERM_REQUIRED, target_id="content")
def push(request, number):
    if number is not None:
        assert type(number) is float
        STACK.append(number)

    render_content()

@action(perm=NO_PERM_REQUIRED, target_id="content")
def reset(request):
    STACK.set([])
    render_content()

@action(perm=NO_PERM_REQUIRED, target_id="content")
def add(request, *args):
    apply_operation(operator.add)

@action(perm=NO_PERM_REQUIRED, target_id="content")
def subtract(request, *args):
    apply_operation(operator.sub)

@action(perm=NO_PERM_REQUIRED, target_id="content")
def multiply(request, *args):
    apply_operation(operator.mul)

@action(perm=NO_PERM_REQUIRED, target_id="content")
def divide(request, *args):
    if len(STACK.get()) and STACK.get()[-1] == 0:
        command("alert", "Can't divide by zero")
        return

    apply_operation(operator.truediv)

def apply_operation(op):
    if len(STACK) < 2:
        command("alert", "Stack has too few elements")
        return

    b, a = STACK.pop(), STACK.pop()
    STACK.append(op(a, b))

    render_content()
