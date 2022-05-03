from collections import defaultdict
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from django.urls import reverse

from hypergen.core import *
from hypergen.core import hypergen_to_response
from notifications.views import notifications
from partialload.views import page1

from todomvc.views import todomvc, ALL
from inputs.views import inputs
from gameofcython.views import gameofcython
from djangotemplates.views import djangotemplates
from hellohypergen.views import counter
from t9n.views import page
from website.templates import base_template, show_sources
from commands.views import commands

def home(request):
    @base_template()
    def template():
        p(mark("UNDER CONSTRUCTION"), "- we are releasing a version 1.0 very soon.",
            "Docs are being written and corners rounded :)", sep=" ")
        with open("README.html") as f:
            raw(f.read())

        h2("Testing Matrix")
        p("Hypergen is tested on the following combinations of Django and Python.")
        with open("../.github/workflows/pytest.yml") as f:
            pytest = load(f.read(), Loader=Loader)
            adjm, xs, ys = defaultdict(list), set(), set()
            for combination in pytest["jobs"]["build"]["strategy"]["matrix"]["include"]:
                py, dj = combination["python-version"], combination["django-version"].replace("Django==", "")
                adjm[py].append(dj)
                xs.add(py)
                ys.add(dj)

            xs = sorted(xs, key=lambda x: int(str(x).split(".")[-1]))
            ys = sorted(ys)
            with table():
                tr(th(), [th("python ", x) for x in xs])
                for y in ys:
                    tr(th("django ", y), [
                        td("✔" if y in adjm[x] else "", style={"color": "green", "text-align": "center"})
                        for x in xs])

        show_sources(__file__)

    return hypergen_to_response(template)

def documentation(request):
    @base_template()
    def template():
        h2("App examples")
        p("These are examples of writing a django app with Django Hypergen. ", "Be sure to read the sources.")
        with ul():
            li(a("Hello hypergen", href=counter.reverse()))
            li(a("Hello core only hypergen", href=reverse("hellocoreonly:counter")),
                " - no magic from contrib.py used")
            li(a("TodoMVC", href=todomvc.reverse(ALL)))

        h2("Live documentation")
        p("Live documentation showing how Hypergen works.")
        with ul():
            li(a("Form inputs", href=inputs.reverse()))
            li(a("Client commands", href=commands.reverse()))
            li(a("Partial loading and history support", href=page1.reverse()))
            li(a("Notifications from Django messages", href=notifications.reverse()))
            li(strike(a("Not translation", href=page.reverse())))

        h2("Alternative template implementations")
        p("While the pure python template 'language' is the main template engine, we support two alternative ",
            " implementations.")
        with ul():
            li(
                a("Using liveview features from within Django Templates",
                href=reverse("djangotemplates:djangotemplates")),
                " - example of the mostly stable Django templates implementation. We could use some input on this, and are ready to polish it together with you."
            )
            li(a("Game of life in pure c++ with Cython", href=gameofcython.reverse()),
                " - example of the still unstable cython implemetation.")

        show_sources(__file__)

    return hypergen_to_response(template)
