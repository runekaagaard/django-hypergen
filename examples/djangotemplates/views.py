import operator

from hypergen.imports import *
from hypergen.context import context as c
from hypergen.templatetags.hypergen import render_to_hypergen

from django.shortcuts import render

from website.templates2 import show_sources

# appstate lives in Django's session and are automatically saved at the end of each request.
def init_appstate():
    return []

init_appstate.namespace = "djangotemplates"

# djangotemplates is a vanilla Django view, with it's route defined in urls.py and not by autourls.
# It's decorated with @liveview to enable liveview capabilities.
@liveview(perm=NO_PERM_REQUIRED, autourl=False, appstate=init_appstate)
def djangotemplates(request):
    return render(request, "djangotemplates/content.html", context=dict(stack=context.hypergen.appstate,
        sources=hypergen(show_sources, __file__)))

def render_content():
    # render_to_hypergen() works exactly as Djangos render_to_string except for two things:
    #     1. It writes the HTML directly to the page.
    #     2. It supports a "block" keyword argument so that only the content of that block is rendered.
    render_to_hypergen("djangotemplates/content.html", context=dict(stack=context.hypergen.appstate,
        sources=hypergen(show_sources, __file__)), block="content")

###  ACTIONS ###
# @actions works exactly like vanilla hypergen actions, so the hypergen template language is enabled.
# Here we choose to use render_context to partially render a Django html template.

@action(perm=NO_PERM_REQUIRED, target_id="content", appstate=init_appstate)
def push(request, number):
    if number is not None:
        assert type(number) is float
        context.hypergen.appstate.append(number)

    render_content()

@action(perm=NO_PERM_REQUIRED, target_id="content", appstate=init_appstate)
def reset(request):
    context.hypergen.appstate = []
    render_content()

@action(perm=NO_PERM_REQUIRED, target_id="content", appstate=init_appstate)
def add(request, *args):
    apply_operation(operator.add)

@action(perm=NO_PERM_REQUIRED, target_id="content", appstate=init_appstate)
def subtract(request, *args):
    apply_operation(operator.sub)

@action(perm=NO_PERM_REQUIRED, target_id="content", appstate=init_appstate)
def multiply(request, *args):
    apply_operation(operator.mul)

@action(perm=NO_PERM_REQUIRED, target_id="content", appstate=init_appstate)
def divide(request, *args):
    if len(context.hypergen.appstate) and context.hypergen.appstate[-1] == 0:
        command("alert", "Can't divide by zero")
        return

    apply_operation(operator.truediv)

def apply_operation(op):
    if len(context.hypergen.appstate) < 2:
        command("alert", "Stack has too few elements")
        return

    b, a = context.hypergen.appstate.pop(), context.hypergen.appstate.pop()
    context.hypergen.appstate.append(op(a, b))

    render_content()
