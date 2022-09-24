# pylint: disable=no-value-for-parameter
from hypergen.imports import *
from hypergen.incubation import SessionVar
import operator

from django.shortcuts import render
from django.template.loader import render_to_string

from website.templates2 import show_sources

d = dict
STACK = SessionVar("STACK", [])  # This variable lives in the session data.

def djangotemplates(request):
    return render(
        request,
        "djangotemplates/base.html",
        d(stack=STACK.get(),
        #sources=hypergen_to_string(show_sources, __file__)
         ))

def push(request):
    number, = loads(request.POST["hypergen_data"])["args"]
    if number is not None:
        assert type(number) is float
        STACK.append(number)
    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK.get())))
    return hypergen_response(context.hypergen.commands)

def reset(request):
    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK.set([]))))
    return hypergen_response(context.hypergen.commands)

def add(request, *args):
    return apply_operation(operator.add)

def subtract(request, *args):
    return apply_operation(operator.sub)

def multiply(request, *args):
    return apply_operation(operator.mul)

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
    return hypergen_response(context.hypergen.commands)
