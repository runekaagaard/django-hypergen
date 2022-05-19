from hypergen.imports import *
from hypergen import liveview
from hypergen import template

from django.http.response import HttpResponse
from django.urls.base import reverse

def my_template(n):
    div("It works", n, sep=" ")

def v1(request):
    return HttpResponse(hypergen(my_template, 42))

def v2(request):
    return hypergen_to_response(my_template, 42)

def my_template2(n):
    div("It works", n, sep=" ")
    button("Click me!", onclick=callback(reverse("devpluginstest:c3"), 100), id_="b1")

def v3(request):
    return HttpResponse(hypergen(my_template2, 42, hypergen_plugins=[template, liveview]))

def c3(request):
    return hypergen_to_response(my_template, 42)
