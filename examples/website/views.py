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
from globalcontext.views import globalcontext
from gettingstarted.views import begin

def home(request):
    @base_template()
    def template():
        with div(class_="hero"):
            h2("Responsive Django, simpler", class_="center hero")
            p(i("Focus on just the functionality, while having 291% more fun!", sep=" "), class_="center")
        with div(class_="terminals", id_="starter"):
            div(
                a("new project", onmousedown=call_js("showTerminal", "starter", "startproject", "b2"), id_="b2",
                class_="selected"),
                a("new app", onmousedown=call_js("showTerminal", "starter", "startapp", "b1"), id_="b1"),
                sep=" ",
            )
            # Project template
            with div(id_="startproject", class_="inner"):
                pre(
                    code("""
python3 -m venv venv
source venv/bin/activate
pip install django django-hypergen
django-admin startproject \\
    --template=https://github.com/runekaagaard/django-hypergen-project-template/archive/master.zip \\
    myproject
cd myproject
python manage.py migrate
python manage.py runserver
""".strip()), class_="terminal nohighlight")
                p("Enjoy your new hypergen app at ", a("http://127.0.0.1:8000/", href="http://127.0.0.1:8000/"), " 🚀")

            # App template
            with div(id_="startapp", class_="inner", style={"display": "none"}):
                pre(
                    code("""
python manage.py startapp \\
    --template=https://github.com/runekaagaard/django-hypergen-app-template/archive/master.zip \\
    myapp
            """.strip()),
                    class_="terminal nohighlight",
                )
                with ol():
                    li("Add", code("'hypergen'"), "and", code("'myapp'"), "to", code("INSTALLED_APPS"), "in",
                        code("settings.py"), sep=" ")
                    li("Add", code("'hypergen.core.context_middleware'"), "to", code("MIDDLEWARE"), "in",
                        code("settings.py"), ", and", sep=" ")
                    li(
                        code(
                        "path('myapp/', include(myapp.urls, namespace='myapp')),", title="""
Don't forget these imports:

from django.urls import path, include
import myapp.urls
                    """.strip()), "to the ", code("urlpatterns"), "of your projects main",
                        code("urls.py"), "file, and enjoy your new hypergen app at",
                        code("http://127.0.0.1:8000/myapp/my_view/"), sep=" ")

        hr(style={"margin-top": "100px"})
        p(mark("2022-05-10: UNDER CONSTRUCTION"), "- we are releasing a version 1.0 very soon.",
            "Docs are being written and corners rounded :)", sep=" ")

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

        h2("Tutorials")
        ul(
            li(a("Getting Started", href=begin.reverse()),
            " - a walk-through from scratch that gets you up and running"))

        h2("Live documentation")
        p("Live documentation showing how Hypergen works.")
        with ul():
            li(a("Form inputs", href=inputs.reverse()))
            li(a("Client commands", href=commands.reverse()))
            li(a("Partial loading and history support", href=page1.reverse()))
            li(a("Hypergens global immutable context", href=globalcontext.reverse()))
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

        h2("Compatability")
        p("Hypergen is ", a("tested", href="https://github.com/runekaagaard/django-hypergen/actions"),
            " on the following combinations of Django and Python:", sep=" ")
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

        p("Both pytest integration and testcafe end-to-end tests are run over the entire matrix.")
        p("Hypergen supports all browser versions from IE10 and forward.")

        show_sources(__file__)

    return hypergen_to_response(template)
