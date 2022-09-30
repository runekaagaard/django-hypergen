# coding = utf-8
# pylint: disable=no-value-for-parameter
import operator

from django.shortcuts import render
from django.template.loader import render_to_string

from hypergen.imports import *
from hypergen.context import context as c

def hypergen_context_decorator(f):
    return f

from hypergen.incubation import SessionVar
from website.templates2 import show_sources

d = dict
STACK = SessionVar("STACK", [])  # This variable lives in the session data.

@liveview(perm=NO_PERM_REQUIRED, autourl=False)
def djangotemplates(request):
    return render(request, "djangotemplates/base.html", d(stack=STACK.get(), sources=hypergen(show_sources,
        __file__)))

@hypergen_context_decorator
def push(request):
    number, = loads(request.POST["hypergen_data"])["args"]
    if number is not None:
        assert type(number) is float
        STACK.append(number)
    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK.get())))
    return hypergen_response(c.hypergen.commands)

@hypergen_context_decorator
def reset(request):
    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK.set([]))))
    return hypergen_response(c.hypergen.commands)

@hypergen_context_decorator
def add(request, *args):
    return apply_operation(operator.add)

@hypergen_context_decorator
def subtract(request, *args):
    return apply_operation(operator.sub)

@hypergen_context_decorator
def multiply(request, *args):
    return apply_operation(operator.mul)

@hypergen_context_decorator
def divide(request, *args):
    if len(STACK.get()) and STACK.get()[-1] == 0:
        return hypergen_response([["alert", "Can't divide by zero"]])

    return apply_operation(operator.truediv)

def apply_operation(op):
    if len(STACK) < 2:
        return hypergen_response([["alert", "Stack has too few elements"]])

    b, a = STACK.pop(), STACK.pop()
    STACK.append(op(a, b))

    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK.get())))
    return hypergen_response(c.hypergen.commands)
