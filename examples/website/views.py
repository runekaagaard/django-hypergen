from hypergen.imports import *
from hypergen.plugins.alertify import AlertifyPlugin

from collections import defaultdict

from yaml import load

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
from website.templates2 import base_template, show_sources, base_template_monokai
from commands.views import commands
from globalcontext.views import globalcontext
from gettingstarted.views import begin
from apptemplate.views import my_view
from coredocs.views import template, liveviews
from website.minidemoes.shoot_em_up import shoot_em_up
from websockets.views import chat

from features import templates as features_templates

@liveview(re_path="^$", perm=NO_PERM_REQUIRED, base_template=base_template_monokai, user_plugins=[AlertifyPlugin()])
def home(request):
    if hasattr(request, 'session') and not request.session.session_key:
        request.session.save()
        request.session.modified = True

    with div(class_="hero"):
        h2("Build reactive web apps, without leaving Django", class_="center hero")
        p(i("Stay focused on the actual complexity of your app, while having 291% more fun!", sep=" "),
            class_="center")
        hr()

    features_templates.main()

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
            p("Enjoy your new hypergen project at ", a("http://127.0.0.1:8000/", href="http://127.0.0.1:8000/"), " 🚀")

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
    h2("News")
    ul(
        li(
        b("2023-11-28"),
        "A lot of recent releases only made master and not pypi but today we are proud to",
        "announce that we are releasing the first stable release of Hypergen. We've been using it in production",
        "for several years, built big systems with it and it's rock-solid enough to warrant the version number ",
        i("1.5.2."),
        "About this release: ",
        ul(
        li(
        "Stable means ",
        a("stable!", href="https://www.youtube.com/watch?v=oyLBGkS5ICk"),
        " Barring security issues, we will not break your code. Everything that can be found in ",
        "the docs will not change in a way that breaks existing userland code.",
        ),
        li(a("Websockets", href="/coredocs/websockets/"),
        "are stable and in a very usable state. We've started using them in production and are currently",
        "pondering several quality-of-life improvements to them.", sep=" "),
        li("Extend support so we now support from python 3.6 / django 1.11.29 up to python 3.12 / django 4.2.6."),
        li("Lots of cleanups and refactorings."),
        ),
        sep=" ",
        ),
        li(b("2022-10-06"), "Another hotly requested feature has hit main.",
        "Existing Django templates can now be extended with liveview capabilities!", "Check out the",
        a("demo", href="/djangotemplates/"), "with sources and the",
        a("documentation.", href="/coredocs/django_templates/"), sep=" "),
        li(b("2022-10-01"), "One of the most requested features at Djangocon was websockets.",
        "I'm happy to announce that websockets are now in main, and a release will happen soon.",
        "You can see it in action as the snake game under", a("Features", href="/"), "and as the obligatory",
        a("chat application.", href=chat.reverse()), sep=" "),
        li(b("2022-09-27:"), "Thank you to the Djangocon organisers and all the wonderful",
        "Django developers we met and listened too!",
        "Hope to see you all in Edinburgh, next year <3.", "We have made available our",
        a("slides", href="https://runekaagaard.github.io/hypergen-djangocon-2022/"), "and the",
        a("example code.", href="https://github.com/runekaagaard/hypergen-djangocon-2022"), sep=" "),
        li(b("2022-09-14:"), "Good news everybody! Hypergen been accepted as a",
        a("workshop", href="https://pretalx.evolutio.pt/djangocon-europe-2022/talk/CFCFFF/"),
        "at djangocon in Porto 2022-09-22. Hope to talk to you there!", sep=" "),
        li(
        b("2022-06-08:"),
        "Pushed version 0.9.9 to pypi. Everything is looking good after a major refactoring. The next version will",
        "be a release candidate for 1.0.0 which will be the first officially stable version of Hypergen.", sep=" "),
        li(b("2022-06-07:"), "The first version of the documentation is complete.", sep=" "))

    h2("App examples")
    p("These are examples of writing a Django app with Hypergen. ", "Be sure to read the sources.")
    with ul():
        li(a("Hello hypergen", href=counter.reverse()))
        li(a("Hello core only hypergen", href=reverse("hellocoreonly:counter")), " - no magic from liveview.py used")
        li(a("TodoMVC", href=todomvc.reverse(ALL)))
        li(a("Hypergen App template", href=my_view.reverse()))
        li(a("Shoot 'Em Duck", href=shoot_em_up.reverse()))
        li(a("Chat app using websockets", href=chat.reverse()), sep=" ")

    h2("Tutorials")
    ul(li(a("Getting Started", href=begin.reverse()), " - a walk-through from scratch that gets you up and running"))

    h2("Documentation")
    p("Documentation explaining and showing how Hypergen works.")
    with ul():
        li(a("Python Templates", href=template.reverse()))
        li(a("Liveviews", href=liveviews.reverse()))
        li(a("Websockets", href="/coredocs/websockets/"))
        li(a("Django HTML Templates", href="/coredocs/django_templates/"))
        li(a("Form inputs", href=inputs.reverse()))
        li(a("Client commands", href=commands.reverse()))
        li(a("Partial loading and history support", href=page1.reverse()))
        li(a("Hypergens global immutable context", href=globalcontext.reverse()))
        li(a("Notifications from Django messages", href=notifications.reverse()))

    h2("Other template implementations")
    with ul():
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
