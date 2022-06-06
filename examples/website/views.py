from hypergen.imports import *
from collections import defaultdict

from yaml import load

from djangolander.views import lander

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from django.urls import reverse

from notifications.views import notifications
from partialload.views import page1
from todomvc.views import todomvc, ALL
from inputs.views import inputs
from gameofcython.views import gameofcython
from djangotemplates.views import djangotemplates
from hellohypergen.views import counter
from t9n.views import page
from website.templates2 import base_template, show_sources
from commands.views import commands
from globalcontext.views import globalcontext
from gettingstarted.views import begin
from apptemplate.views import my_view
from coredocs.views import template, liveviews
from website.minidemoes.shoot_em_up import shoot_em_up

@liveview(re_path="^$", perm=NO_PERM_REQUIRED, base_template=base_template)
def home(request):
    with div(class_="hero"):
        h2("Build reactive web apps, without leaving Django", class_="center hero")
        p(i("Stay focused on the actual complexity of your app, while having 291% more fun!", sep=" "),
            class_="center")
        hr()

    h2("Why hypergen?")
    p("For a more technical explanation about the ", i("what"), " and the ", i("how"), ", check out our ",
        a("github page", href="https://github.com/runekaagaard/django-hypergen/"), " and read the ",
        a("documentation", href="/documentation/"), ".")
    p("We've been building Django apps for over 12 years, and have played around with different "
        "approaches. From nojs html pages, over jQuery enhanced apps to full blown server/client "
        "separation with React. We love composing html with jsx but felt a lot of our time was spent "
        "munging data between server and client, duplicating logic and keeping up with the extremely "
        "vast and ever-changing javascript ecosystem.")
    p("We felt there was a better way. For us.")
    p("We wanted something that feels like ", i("one single thing."), " Just like Django does. ",
        "We felt using html templates creates a second language and doesn't compose well. We also wanted ",
        "pain-free binding of DOM events to server functions as well as a simple way to instruct ",
        "the client to run javascript functions.")
    p("And Hypergen was born.")
    p("Thanks for reading this, drop by and ",
        a("say hi", href="https://github.com/runekaagaard/django-hypergen/discussions"), " :)")

    h2("Super duper quickstart")
    p("Read the ", a("Getting Started", href="/gettingstarted/begin/"), " tutorial for a more thorough experience. ",
        "For the most speedy start possible, run the following in your terminal.",
        ' Replace "myproject" and "myapp" with your own names.')
    with div(class_="terminals", id_="quickstart"):
        quickstart_template()

@action(perm=NO_PERM_REQUIRED, target_id="quickstart")
def quickstart(request, n, app_name):
    quickstart_template(n=n, app_name=app_name)

def quickstart_template(n=0, app_name="myapp"):
    div(
        a("new project", onmousedown=callback(quickstart, 0, app_name), id_="b2",
        class_="selected" if n == 0 else OMIT),
        a("new app", onmousedown=callback(quickstart, 1, app_name), id_="b1", class_="selected" if n == 1 else OMIT),
    )

    # Project template
    if n == 0:
        with div(id_="startproject", class_="inner"):
            pre(code(PROJECT), class_="terminal nohighlight")
            p("Enjoy your new hypergen app at ", a("http://127.0.0.1:8000/", href="http://127.0.0.1:8000/"), " 🚀")

    # App template
    if n == 1:
        with div(id_="startapp", class_="inner"):
            pre(
                code(APP),
                class_="terminal nohighlight",
            )
            with ol():
                li("Add", code("'hypergen'"), "and", code("'myapp'"), "to", code("INSTALLED_APPS"), "in",
                    code("settings.py"), sep=" ")
                li("Add", code("'hypergen.context.context_middleware'"), "to", code("MIDDLEWARE"), "in",
                    code("settings.py"), sep=" ")
                li("Add", code("path('myapp/', include(myapp.urls, namespace='myapp')),", title=IMPORTS), "to the ",
                    code("urlpatterns"), "variable of your projects main", code("urls.py"), "file", sep=" ")
            p("Enjoy your new hypergen app at", code("http://127.0.0.1:8000/myapp/my_view/"), "🤯", sep=" ")

IMPORTS = """
    Don't forget these imports:

    from django.urls import path, include
    import myapp.urls
                        """.strip()

PROJECT = """
python3 -m venv venv
source venv/bin/activate
pip install django django-hypergen
django-admin startproject \\
    --template=https://github.com/runekaagaard/django-hypergen-project-template/archive/master.zip \\
    myproject
cd myproject
python manage.py migrate
python manage.py runserver
""".strip()

APP = """
python manage.py startapp \\
    --template=https://github.com/runekaagaard/django-hypergen-app-template/archive/master.zip \\
    myapp
""".strip()

@liveview(perm=NO_PERM_REQUIRED, base_template=base_template)
def documentation(request):
    p(mark("2022-06-06: UNDER CONSTRUCTION"), "- we are releasing a version 1.0 very soon.",
        "Docs are being written and corners rounded :)", sep=" ")

    h2("App examples")
    p("These are examples of writing a Django app with Hypergen. ", "Be sure to read the sources.")
    with ul():
        li(a("Hello hypergen", href=counter.reverse()))
        li(a("Hello core only hypergen", href=reverse("hellocoreonly:counter")), " - no magic from liveview.py used")
        li(a("TodoMVC", href=todomvc.reverse(ALL)))
        li(a("Hypergen App template", href=my_view.reverse()))
        li(a("Shoot 'Em Duck", href=shoot_em_up.reverse()))

    h2("Tutorials")
    ul(li(a("Getting Started", href=begin.reverse()), " - a walk-through from scratch that gets you up and running"))

    h2("Documentation")
    p("Documentation explaining and showing how Hypergen works.")
    with ul():
        li(a("Templates", href=template.reverse()))
        li(a("Liveviews", href=liveviews.reverse()))
        li(a("Form inputs", href=inputs.reverse()))
        li(a("Client commands", href=commands.reverse()))
        li(a("Partial loading and history support", href=page1.reverse()))
        li(a("Hypergens global immutable context", href=globalcontext.reverse()))
        li(a("Notifications from Django messages", href=notifications.reverse()))

    h2("Alternative template implementations")
    p("While the pure python template 'language' is the main template engine, two alternative ",
        " implementations exists. These use an older version of Hypergen.")
    with ul():
        li(a("Django html Templates", href=reverse("djangotemplates:djangotemplates")),
            " - Django html templates instead of python templates. ",
            "We could use some input on this, and are ready to polish it together with you.")
        li(a("Game of life in pure c++ with Cython", href=gameofcython.reverse()),
            " - example of the alpha Cython implementation.")

    h2("Compatibility")
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
                tr(th("django ", y),
                    [td("✔" if y in adjm[x] else "", style={"color": "green", "text-align": "center"}) for x in xs])

    p("Both pytest integration and testcafe end-to-end tests are run over the entire matrix.")
    p("Hypergen supports all browser versions from IE10 and forward.")

    show_sources(__file__)
