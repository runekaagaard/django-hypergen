# Import all html tag functions, etc.
from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED

from django.urls.base import reverse
from django.templatetags.static import static
from website.templates import base_head, show_sources


def pretty_indent(txt):
    """counts num of whitespaces in firstline, and removes from rest"""
    lines = txt.split("\n")
    count = 0
    lines = [line for line in lines if len(line.split()) > 0]
    for c in lines[0]:
        if c.isspace():
            count = count + 1
        else:
            break
    return "\n".join(x[count:] for x in lines).strip()


_code = code


def code(txt):
    return _code(pretty_indent(txt))


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
        code("""
        # Create project dir and go
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
        python manage.py runserver
        """
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
        code("""
        ....
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
        code("""
        ....
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'myapp'
        ]
        .....
        """
             )
    )

    p("In the myapp/views.py file we will create our first hypergen view")
    p("Delete everything in this file and make it look like this:")
    pre(
        code("""
        from hypergen.core import *
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
        """)
    )
    p("In order to view this in a browser we can add the view to myapp/urls.py and include the namespaced app in myproject/urls.py like this")
    p("In the myapp folder create a file named urls.py, and add this content")
    pre(
        code("""
        from hypergen.contrib import hypergen_urls
        from myapp import views

        app_name = 'myapp'

        # Automatically creates urlpatterns for all functions in views.py decorated with @hypergen_view or @hypergen_callback.
        urlpatterns = hypergen_urls(views, namespace="myapp")
        """)
    )
    p("Finally we can include this new myapp/urls.py in our main urls.py inside the myproject folder like so:")
    pre(
        code("""
        from django.contrib import admin
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
        """)
    )
    p("No need to edit urls.py. Your new view is instantly available and located at localhost:8000/myapp/step2")
    p("How come It looks a lot different now, you might ask"
      "That's because we took the liberty of adding the water.css stylesheet to this page, using the link() function."
      "In general: All html tags (<html><div><span><audio> etc.) has an equivalent hypergen function, which was imported from hypergen.core in the begining of views.py in "
      "this line")
    pre(code(
        "from hypergen.core import *"
    ))
    p("Lets call these tag rendering python functions for base components. A base component does take both args and kwargs. Args beeing either text or other components,"
      " which will effectively be nested inside the corresponding element when rendered. Kwargs will become the named attributes of the element")
    p("Here's is an example:")
    pre(code("""
        section(
            "This is a section, with an ", a("link", id="im-one-of-a-kind", class_="clickable", href="#"), " inside", br(),
            "The link has the id ", i("im-one-of-a-kind")
        )
        """

             )
        )
    p("which when rendered as html looks like this:")
    pre(code("""
        <section>
             This is a section, with an <a id="im-one-of-a-kind" class="clickable" href="#">link</a> inside <br/>
             The link has the id <i>im-one-of-a-kind</i> and a class attribute named <i>clickable</i>
        </section>
        """)
        )
    p("As you can see we can define html elements with python functions; their children with other python functions as arguments; and their attributes with kwargs")
    p('You might have noticed that the class attribute of the a tag, is defined as class_="clickable" instead of just class. ')
    p("This is because class is a reserved keyword in django, and therefore cannot be used to name a kwarg")
    p('Whenever you want to use a reserved keyword for an attribute name you can always just add _ to the end, hypergen will know what you mean')
    p("Another way you can use base component functions is as context managers. Try adding the following to your views.py")
    pre(
        code(""" 
        ......
        @hypergen_view(perm=NO_PERM_REQUIRED)
        def step3(request):
            template3()
                    
        def template3():
            doctype()
            with html():
                with head():
                    link(href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css")
                with body():
                    h1("As Context managers")
                    strong("Hypergen base component functions can also be used as contextmanagers")
        """)
    )
    p("Go to localhost:8000/myapp/step3, and enjoy the result")
    p("Using base component functions as context managers are really great for keeping an easy readable indented structure, its easy to see whats inside what, "
      "buts it's also handy when you want to use python other than the base component functions, i.e. a loop that generates a list")
    pre(
        code("""
        with ul():
                for i in range(20):
                    li(f"I'm number {i}")
        """)
    )
    p("(Actually hypergen is so smart that the above could be writen by sending a list of base components as an argument to ul like so): ",
      pre(code("""ul([li(f"I'm number {i}") for i in range(20)])""")),
      "(but don't tell anyone)")
    p("But where context managers really shine is where we want to create a base template where we can yield only the code that changes between our views")
    p("Let's move all the boilerplate html code out in its own function. Make it into a @contextmanager and use it in step4")
    pre(
        code("""
        # Add this to the import section in the top of views.py
        from contextlib import contextmanager
        ......
        @contextmanager
        def base_template():
            doctype()
            with html():
                with head():
                    link(href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css")
                with body():
                    yield
        
        @hypergen_view(perm=NO_PERM_REQUIRED)
        def step4(request):
            template4()
        
        def template4():
            with base_template():
                h1("Now using a base template")
        """)
    )
    p("""Now that we have created a new base template, we can add our new base template as a keyword argument to the hypergen_vew decorator so that we ca avoid all the boilerplate and concentrate on the content part of our template""")
    pre(code("""
        ......
        @hypergen_view(perm=NO_PERM_REQUIRED, base_template=base_template)
        def step5(request):
            template5()
        
        def template5():
            h1("Step 5: Now reusing the base template")
            section("This view is reusing the same base template as step4")
        """)
        )
    p("""As you might have noticed our code get's a lot cleaner, now is the time for some user action.""")
    h3("Introducing hypergen callbacks")
    p("""A hypergen callback is a function view that that can be triggered from the client, And usually changes something in the view""")
    p("""In order to make hypergen callbacks available we need to include hypergen.js in the head section of the page, change your base_template so it looks like this""")
    pre(
        code("""
        from django.templatetags.static import static
        ....
        
        @contextmanager
        def base_template():
            doctype()
            with html():
                with head():
                    link(href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css")
                    script(src=static("/hypergen/hypergen.min.js"))
                with body():
                    with div(id_="content"):
                        yield
        ....
        """)


    )

    p("And create a new step6 view and template that takes an argument, num_clicks, which is defaulted to 0")
    pre(
        code("""
        .......
        @hypergen_view(perm=NO_PERM_REQUIRED, base_template=base_template)
            def step6(request):
                template6()
    
            def template6(num_clicks=0):
                if num_clicks>0:
                    h2("Step 6: Callback is a success")
                    p(f"You've successfully clicked on a button {num_clicks} time(s)- congratulations!")
                    button("click again", id_="button", onclick=callback(on_click, num_clicks + 1))
                else:
                    h2("Step 6: Callbacks")
                    p("Try clicking the button below - if you dare")
                    button("click me", id_="button", onclick=callback(on_click_callback, num_clicks + 1))
        """)
    )
    p("As you can see we've assigned an action on the onclick action on the button element, and referenced it to the on_click_callback, "
      "which we will create now ")
    pre(
        code("""
        ...
        @hypergen_callback(perm=NO_PERM_REQUIRED, target_id='content')
        def on_click(request, num_clicks=0):
            template6(num_clicks)
        """)
    )
    p("Callbacks are like views")
