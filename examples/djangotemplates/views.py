import operator
from django.http.response import HttpResponse

from django.shortcuts import render
from django.template.loader import render_to_string

from hypergen.imports import *
from hypergen.context import context as c
from hypergen.incubation import hypergenable

from hypergen.incubation import SessionVar
from website.templates2 import show_sources

d = dict
STACK = SessionVar("STACK", [])  # This variable lives in the session data.

@hypergenable
def djangotemplates(request):
    return render(request, "djangotemplates/base.html", d(stack=STACK.get(), sources=hypergen(show_sources,
        __file__)))

@hypergenable
def push(request):
    number, = loads(request.POST["hypergen_data"])["args"]
    if number is not None:
        assert type(number) is float
        STACK.append(number)
    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK.get())))
    return HttpResponse(dumps(c.hypergen.commands), status=200, content_type='application/json')

@hypergenable
def reset(request):
    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK.set([]))))
    return HttpResponse(dumps(c.hypergen.commands), status=200, content_type='application/json')

@hypergenable
def add(request, *args):
    return apply_operation(operator.add)

@hypergenable
def subtract(request, *args):
    return apply_operation(operator.sub)

@hypergenable
def multiply(request, *args):
    return apply_operation(operator.mul)

@hypergenable
def divide(request, *args):
    if len(STACK.get()) and STACK.get()[-1] == 0:
        return HttpResponse(dumps([["alert", "Can't divide by zero"]]), status=200, content_type='application/json')

    return apply_operation(operator.truediv)

def apply_operation(op):
    if len(STACK) < 2:
        return HttpResponse(dumps([["alert", "Stack has too few elements"]]), status=200,
            content_type='application/json')

    b, a = STACK.pop(), STACK.pop()
    STACK.append(op(a, b))

    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK.get())))
    return HttpResponse(dumps(c.hypergen.commands), status=200, content_type='application/json')
