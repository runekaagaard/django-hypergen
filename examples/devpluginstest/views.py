d = dict
from hypergen.contrib import base_template
from hypergen.imports import *

from contextlib import contextmanager

from django.http.response import HttpResponse, HttpResponseRedirect
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
        my_content_template, 222, hypergen=d(plugins=[TemplatePlugin(),
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
    return HttpResponse(hypergen(my_page, hypergen=d(plugins=[TemplatePlugin(), LiveviewPlugin()], indent=True)))

def c6(request):
    n, = loads(request.POST["hypergen_data"])["args"]
    commands = hypergen(my_form, n + 1, hypergen=d(plugins=[TemplatePlugin(),
        CallbackPlugin(target_id="body")], returns=COMMANDS))

    return HttpResponse(dumps(commands), status=200, content_type='application/json')

### v5

def my_page2():
    with html(), body(), div(id_="body"):
        my_form2(0)

def my_form2(n):
    h2("WOW!")
    el = input_(type_="number", id_="i1", value=n)
    button("MORE!", id_="i2", onclick=callback(reverse("devpluginstest:c7"), el))

def v5(request):
    return HttpResponse(hypergen(my_page2, hypergen=d(liveview=True)))

def c7(request):
    n, = loads(request.POST["hypergen_data"])["args"]
    commands = hypergen(my_form2, n + 1, hypergen=d(callback=True, returns=COMMANDS, target_id="body"))

    return HttpResponse(dumps(commands), status=200, content_type='application/json')

# v6
@contextmanager
def v6_base_template():
    doctype()
    with html():
        with head():
            title("I am title")
        with body():
            h1("I am base!")
            with div(id_="content"):
                yield

v6_base_template.target_id = "content"

@liveview(perm=NO_PERM_REQUIRED, base_template=v6_base_template, autourl=False, partial=False)
def v6(request):
    p("I am view!")

def c8(request):
    n, = loads(request.POST["hypergen_data"])["args"]
    commands = hypergen(my_form2, n + 1, hypergen=d(callback=True, returns=COMMANDS, target_id="body"))

    return HttpResponse(dumps(commands), status=200, content_type='application/json')

@liveview(perm=NO_PERM_REQUIRED, autourl=False)
def v7(request):
    body(p("I am view!", reverse("devpluginstest:v7"), sep=" "))

@liveview(perm=NO_PERM_REQUIRED, base_template=v6_base_template, partial=False)
def v8(request):
    p("I am view!", v8.reverse(), sep=" ")

@liveview(perm=NO_PERM_REQUIRED, base_template=v6_base_template, path="thisv9/")
def v9(request):
    p("I am view!", v9.reverse(), sep=" ")

@liveview(perm=NO_PERM_REQUIRED, base_template=v6_base_template, path="this10/<int:num>/<slug:title>/")
def v10(request, num, title):
    p("I am view!", num, title, v10.reverse(num=num, title=title), sep=" - ")

@liveview(perm=NO_PERM_REQUIRED, base_template=v6_base_template,
    re_path=r"^v11ok/(?P<year>[0-9]{4})/(?P<username>\w+)/$")
def v11(request, year, username):
    p("I am view!", title, username, v11.reverse(year=year, username=username), sep=" - ")

@liveview(perm=NO_PERM_REQUIRED, base_template=v6_base_template, re_path=r"^v12what/([0-9]{4})/(\w+)/$")
def v12(request, year, username):
    p("I am view!", title, username, v12.reverse(year, username), sep=" - ")

@liveview(perm="no-idont-have-it", base_template=v6_base_template)
def v13(request):
    p("I am view!")

@liveview(perm="no-idont-have-it", base_template=v6_base_template, raise_exception=True)
def v14(request):
    body(p("I am view!"))

@liveview(perm="no-idont-have-it", base_template=v6_base_template, login_url="/mitobito", redirect_field_name="nooog")
def v15(request, year, username):
    p("I am view!")

# partial
@liveview(perm=NO_PERM_REQUIRED, base_template=v6_base_template)
def v16(request):
    div(a("v16", href=v16.reverse()))
    div(a("v17", href=v17.reverse()))
    a("v17", href=v17.reverse())
    with div():
        a("v17", href=v17.reverse())

@liveview(perm=NO_PERM_REQUIRED, base_template=v6_base_template)
def v17(request):
    div(a("v16", href=v16.reverse()))
    div(a("v18", href=v18.reverse()))

@liveview(perm=NO_PERM_REQUIRED, base_template=v6_base_template)
def v18(request):
    div("End of line")

# actions
@liveview(perm=NO_PERM_REQUIRED, base_template=v6_base_template)
def v19(request):
    button("Do it", onclick=callback(c20, 10, 20), id_="b1")
    button("Do it2", onclick=callback(c21, 10, 20), id_="b2")
    button("Forbidden", onclick=callback(c23, "new"), id_="b3")
    button("Replace", onclick=callback(c22, "new content"), id_="b4")
    button("Redirect", onclick=callback(c24), id_="b5")
    button("Redirect2", onclick=callback(c25), id_="b6")
    div("replace into here", id_="replaceinto")

@action(perm=NO_PERM_REQUIRED, target_id="content")
def c20(request, x, y):
    div("I am new div!", x, y)

@action(perm=NO_PERM_REQUIRED, base_template=v6_base_template)
def c21(request, x, y):
    div("I am new div!", x, y)

@action(perm=NO_PERM_REQUIRED, target_id="replaceinto")
def c22(request, content):
    div(content)

@action(perm="forbidden", target_id="replaceinto", re_path=r"^sosupergreat/$")
def c23(request, content):
    div(content)

@action(perm=NO_PERM_REQUIRED, path="thepathc24/")
def c24(request):
    command("hypergen.redirect", v18.reverse())

@action(perm=NO_PERM_REQUIRED)
def c25(request):
    return HttpResponseRedirect(v17.reverse())
