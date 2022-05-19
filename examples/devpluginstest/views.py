from hypergen.template import *

from django.http.response import HttpResponse

def v1(request):
    return HttpResponse(hypergen(my_template, 42))

def v2(request):
    return hypergen_to_response(my_template, 42)

def my_template(n):
    div("It works", n, sep=" ")
