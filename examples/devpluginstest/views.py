d = dict
from hypergen.imports import *

from django.http.response import HttpResponse
from django.urls.base import reverse

def my_template(n):
    div("It works", n, sep=" ")

def v1(request):
    return HttpResponse(hypergen(my_template, 42))

def v2(request):
    return hypergen_to_response(my_template, 42)

def my_template2(n):
    doctype()
    with html():
        with head():
            title("Foo")
        with body():
            with div(id_="my-body-id"):
                my_content_template(n)

def my_content_template(n):
    div("It works", n, sep=" ")
    button("Click me!", onclick=callback(reverse("devpluginstest:c3"), 100), id_="b1")

def v3(request):
    return HttpResponse(hypergen(my_template2, 42, hypergen=d(plugins=[TemplatePlugin(), LiveviewPlugin()])))

def c3(request):
    data = hypergen(my_content_template, 666, hypergen=d(plugins=[TemplatePlugin(),
        CallbackPlugin()], full_return=True))
    commands = data["context"]["hypergen"]["commands"]
    commands.append(["hypergen.morph", "my-body-id", data["html"]])

    return HttpResponse(dumps(commands), status=200, content_type='application/json')
