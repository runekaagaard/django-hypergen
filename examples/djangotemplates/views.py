# coding = utf-8
# pylint: disable=no-value-for-parameter
import operator

from django.shortcuts import render
from django.template.loader import render_to_string
from hypergen.core import hypergen_context_decorator, command, hypergen_response, context as c, loads

d = dict
# Only works in a one thread, one user context.
STACK = []

@hypergen_context_decorator
def djangotemplates(request):
    return render(request, "djangotemplates/base.html", d(stack=STACK))

@hypergen_context_decorator
def push(request):
    number, = loads(request.POST["hypergen_data"])["args"]
    if number is not None:
        assert type(number) is float
        STACK.append(number)
    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK)))
    return hypergen_response(c.hypergen.commands)

@hypergen_context_decorator
def reset(request):
    global STACK
    STACK = []

    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK)))
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
    if len(STACK) and STACK[-1] == 0:
        return hypergen_response([["alert", "Can't divide by zero"]])

    return apply_operation(operator.truediv)

def apply_operation(op):
    global STACK
    if len(STACK) < 2:
        return hypergen_response([["alert", "Stack has too few elements"]])

    b, a = STACK.pop(), STACK.pop()
    STACK.append(op(a, b))

    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK)))
    return hypergen_response(c.hypergen.commands)
