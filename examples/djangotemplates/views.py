# coding = utf-8
# pylint: disable=no-value-for-parameter
d = dict

from django.shortcuts import render
from django.template.loader import render_to_string
from hypergen.core import hypergen_context_decorator, command, hypergen_response, context as c, loads

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
def plus(request, *args):
    global STACK
    STACK = [sum(STACK)]
    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK)))
    return hypergen_response(c.hypergen.commands)

@hypergen_context_decorator
def minus(request, *args):
    global STACK
    res = None
    for n in STACK:
        if res is None:
            res = n
            continue
        res -= n

    STACK = [res]
    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK)))
    return hypergen_response(c.hypergen.commands)

@hypergen_context_decorator
def multiply(request, *args):
    global STACK
    res = None
    for n in STACK:
        if res is None:
            res = n
            continue
        res *= n

    STACK = [res]
    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK)))
    return hypergen_response(c.hypergen.commands)

@hypergen_context_decorator
def divide(request, *args):
    global STACK
    res = None
    for n in STACK:
        if res is None:
            res = n
            continue
        elif n == 0:
            res = 0
            break

        res /= n

    STACK = [res]
    command("hypergen.morph", "content", render_to_string("djangotemplates/content.html", d(stack=STACK)))
    return hypergen_response(c.hypergen.commands)
