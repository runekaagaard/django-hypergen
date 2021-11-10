from django.urls import reverse

from hypergen.core import *
from hypergen.core import hypergen_to_response

from todomvc.views import todomvc, ALL
from inputs.views import inputs
from gameofcython.views import gameofcython
from djangotemplates.views import djangotemplates
from hellohypergen.views import counter

def home(request):
    def template():
        h1("Welcome to hypergen examples")
        with ul():
            li(a("Hello hypergen", href=counter.reverse()))
            li(a("TodoMVC", href=todomvc.reverse(ALL)))
            li(a("Inputs", href=inputs.reverse()))
            li(a("Game of life in pure c++ with Cython", href=gameofcython.reverse()))
            li(
                a("Using liveview features from within Django Templates",
                href=reverse("djangotemplates:djangotemplates")))

    return hypergen_to_response(template)
