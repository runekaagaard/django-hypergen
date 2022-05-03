# Import all html tag functions, etc.
from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED

from django.urls.base import reverse
from django.templatetags.static import static
from website.templates import base_head, show_sources


# So this a hypergen view. If no "url" parameter is given one will be automatically assigned. "perm" is required.
# A LOT of stuff happens under the hood and the decorator can be configured in many ways. Just go with it for now.
@hypergen_view(perm=NO_PERM_REQUIRED)
def begin(request):
    # hypergen_view collects html and returns it as a Django response.
    doctype()  # standard html5 doctype.
    with html():  # tags can be nested
        with head():
            script(src=static("hypergen/hypergen.min.js"))  # html attributes are keyword arguments.
            base_head()
        with body():
            # This id matches the "target_id" argument to the "increment" callback.
            with div(id_="body"):
                # Render the dynamic content of the page. This happens in it's own function so that functionality
                # can be shared between the view and the callback.
                template(1)

            show_sources(__file__)


# Hypergen html is very easy to compose, just use functions.
def template(n):
    # Tags can take other tags as arguments.
    p(a("Back to documentation", href=reverse("website:documentation")))

    h1("Getting Started")
    p("The purpose of this short tutorial is getting you up and running with hypergen, let you code you first liveview, and give you an idea of how Django Hypergen can contribute to your workflow")
    h3("Django - the framework for champions - getting ready for hypergen")
    p("Lets install Django")
    p("If you already have a Django project you can use as a testbed for hypergen, feel free to skip this section. "
      "But if you are new to Django or want to have a clean installation for messing around with hypergen, read on.")

    pre(
        code("""# Create project dir and go
mkdir my-hypergen-app && cd my-hypergen-app
# Create virtual environment
python3 -m venv venv
# Activate virtual environment
source venv/bin/activate
# Install the latest Django
pip install django
# Start project and go 
django-admin startproject myproject && cd myproject
# Run migrations
python manage.py migrate
# Run the dev-server
python manage.py runserver"""
        )
    )

    p("If you go to ", a("localhost:8000", href="localhost:8000"),
      " you should see a space rocket! Congrats you're now ready to dive in to the world of hypergen")
    h3("Install hypergen")
    p("Before we can actually work with hypergen we need to install it, ctrl-c to exit the runserver and execute the following:")
    pre(
        code("""pip install django-hypergen""")
    )

    p("Further more we need to add the middleware class that keeps track of the hypergen context, add hypergen.core.ContextMiddleware to MIDDLEWARE in settings.py, so it looks like this:")
    pre(
        code("""....
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hypergen.core.ContextMiddleware'
]
.....""")
    )

    h3("Make the app")
    p("Lets start a new app, so we can give hypergen a testrun")
    pre(
        code("""python manage.py startapp myapp""")
    )
    p("This will create a new folder called myapp")
    p("Add the app to INSTALLED_APPS in myproject/settings.py")
    pre(
        code("""....
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp'
]
.....""")
    )

    p("In the myapp/views.py file we will create our first hypergen view")
    p("Delete everything in this file and make it look like this:")
    pre(
        code("""from hypergen.core import *
from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED

@hypergen_view(perm=NO_PERM_REQUIRED)
def step1(request):
    doctype()
    html(
        head(),
        body(
            h1("This is rendered with hypergen"),
            strong("An awesome HTML rendering engine, where you define templates using python only")
        )
    )
""".strip())
    )
    p("In order to view this in a browser we can add the view to myapp/urls.py and include the namespaced app in myproject/urls.py like this")
    p("In the myapp folder create a file named urls.py, and add this content")
    pre(
        code("""from hypergen.contrib import hypergen_urls
from myapp import views

app_name = 'myapp'

# Automatically creates urlpatterns for all functions in views.py decorated with @hypergen_view or @hypergen_callback.
urlpatterns = hypergen_urls(views, namespace="myapp")
""")
    )
    p("Finally we can include this new myapp/urls.py in our main urls.py inside the myproject folder like so:")
    pre(
        code("""from django.contrib import admin
from django.urls import path, include
import myapp.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include(myapp.urls, namespace="myapp")),
]
""")
    )
    p("Startup the dev server (python manage.py runserver) and go to localhost:8000/myapp/step1")
    p("If all went well you should see a beautifully rendered HTML page, like in the good old days, no css, no JS just plain HTML")
    p("How is this exciting you might ask... And really its not.. at least not yet. So far we what we have could be acquired just as easy using normal Django template without hypergen")
    h3("Composablity")
    p("Lets take all this hypergen template rendering out of the view and make it into its own function. Add this new view to myapp/views.py")
    pre(
        code("""
        
......        
@hypergen_view(perm=NO_PERM_REQUIRED)
def step2(request):
    template2()

def template2():
    doctype()
    html(
        head(
            link(href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css")
        ),
        body(
            h1("This is rendered with hypergen "),
            strong("An awesome HTML rendering engine, where you define templates using python only"),
            h2("And because hypergen defines html templates in pure python functions these can be refactored into separate functions")
        )
    )
""".strip())
    )
    p("No need to edit urls.py. Your new view is instantly available and located at localhost:8000/myapp/step2")
    p("Whats happening?")
    p("It looks a lot different now. "
      "That's because we took the liberty of adding the water.css stylesheet to this page, using the link() function."
      "In general: All html tags (<html><div><span><audio> you name it). has an equivalent hypergen function (which is imported from hypergen.core in the begining of views.py)")
    pre(code(
        "from hypergen.core import *"
    ))




