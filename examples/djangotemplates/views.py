import operator
from django.http.response import HttpResponse

from django.shortcuts import render

from hypergen.imports import *
from hypergen.context import context as c
from hypergen.templatetags.hypergen import render_to_hypergen

from hypergen.incubation import SessionVar
from website.templates2 import show_sources

d = dict
STACK = SessionVar("STACK", [])  # This variable lives in the session data.

@liveview(perm=NO_PERM_REQUIRED, autourl=False)
def djangotemplates(request):
    return render(request, "djangotemplates/content.html", context=d(stack=STACK.get(),
        sources=hypergen(show_sources, __file__)))

def render_content():
    render_to_hypergen("djangotemplates/content.html", context=d(stack=STACK.get(),
        sources=hypergen(show_sources, __file__)), block="content")

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
