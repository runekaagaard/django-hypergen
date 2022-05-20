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
    button("And me!", onclick=callback(reverse("devpluginstest:c4"), 100), id_="b2")
    button("Alerts!", onclick=call_js("alert", 1234), id_="b3")
    button("Me too!", onclick=callback(reverse("devpluginstest:c5"), 100), id_="b4")

def v3(request):
    return HttpResponse(hypergen(my_template2, 42, hypergen=d(plugins=[TemplatePlugin(), LiveviewPlugin()])))

def c3(request):
    data = hypergen(my_content_template, 666, hypergen=d(plugins=[TemplatePlugin(), CallbackPlugin()], returns=FULL))
    commands = data["context"]["hypergen"]["commands"]
    commands.append(["hypergen.morph", "my-body-id", data["html"]])

    return HttpResponse(dumps(commands), status=200, content_type='application/json')

def c4(request):
    commands = hypergen(
        my_content_template, 666, hypergen=d(plugins=[TemplatePlugin(),
        CallbackPlugin(target_id="my-body-id")], returns=COMMANDS))

    return HttpResponse(dumps(commands), status=200, content_type='application/json')

def c5(request):
    def only_commands():
        command("console.log", "So lets go!")

    commands = hypergen(only_commands, hypergen=d(plugins=[CallbackPlugin()], returns=COMMANDS))

    return HttpResponse(dumps(commands), status=200, content_type='application/json')

### v4

def my_page():
    with html(), body(), div(id_="body"):
        my_form(0)

def my_form(n):
    h2("WOW!")
    el = input_(type_="number", id_="i1", value=n)
    button("MORE!", id_="i2", onclick=callback(reverse("devpluginstest:c6"), el))

def v4(request):
    return HttpResponse(hypergen(my_page, hypergen=d(plugins=[TemplatePlugin(), LiveviewPlugin()])))

def c6(request):
    n, = loads(request.POST["hypergen_data"])["args"]
    commands = hypergen(my_form, n + 1, hypergen=d(plugins=[TemplatePlugin(),
        CallbackPlugin(target_id="body")], returns=COMMANDS))

    return HttpResponse(dumps(commands), status=200, content_type='application/json')
