from hypergen.imports import *
# Import all html tag functions, etc.

from django.urls.base import reverse
from django.templatetags.static import static
from website.templates2 import base_head, show_sources

def pretty_indent(txt):
    """counts num of whitespaces in firstline, and removes from rest"""
    lines = txt.split("\n")
    count = 0
    for line in lines:
        if len(line.strip()) == 0:
            del lines[0]
        else:
            break
    for c in lines[0]:
        if c.isspace():
            count = count + 1
        else:
            break
    return "\n".join(x[count:] if len(x) > count else x for x in lines).strip()

_code = code

def code(txt):
    return _code(pretty_indent(txt))

# So this a hypergen view. If no "url" parameter is given one will be automatically assigned. "perm" is required.
# A LOT of stuff happens under the hood and the decorator can be configured in many ways. Just go with it for now.
@liveview(perm=NO_PERM_REQUIRED)
def begin(request):
    # liveview collects html and returns it as a Django response.
    doctype()  # standard html5 doctype.
    with html():  # tags can be nested
        with head():
            base_head()
        with body():
            # This id matches the "target_id" argument to the "increment" action.
            with div(id_="body"):
                # Render the dynamic content of the page. This happens in it's own function so that functionality
                # can be shared between the view and the action.
                template(1)

            show_sources(__file__)

# Hypergen html is very easy to compose, just use functions.
def template(n):
    # Tags can take other tags as arguments.
    p(a("Back to documentation", href=reverse("website:documentation")))

    h1("Getting Started")
    i("- A very basic, step by step getting started tutorial")
    p("The purpose of this tutorial is getting you up and running with hypergen, let you code you first liveview, and give you an idea of how Django Hypergen can contribute to your workflow"
     )
    h2("Step 0: Getting ready for hypergen")
    p("Lets install Django")
    p("If you already have a Django project you can use as a testbed for hypergen, feel free to skip this section. "
        "But if you are new to Django or want to have a clean installation for messing around with hypergen, read on."
     )

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
        """))

    p("If you go to ", a("localhost:8000", href="localhost:8000"),
        " you should see a space rocket! Congrats you're now ready to dive in to the world of hypergen")
    h4("Install hypergen")
    p("Before we can actually work with hypergen we need to install it, ctrl-c to exit the runserver and execute the following:"
     )
    pre(code("""pip install django-hypergen"""))

    p("Further more we need to add the middleware class that keeps track of the hypergen context, add 'hypergen.context.context_middleware', to MIDDLEWARE in settings.py, so it looks like this:"
     )
    pre(
        code("""
        MIDDLEWARE = [
            ...
            'hypergen.context.context_middleware',
            ...
        ]
        """))

    h2("Step 1: Make the app")
    p("Lets start a new app, so we can give hypergen a test run")
    pre(code("""python manage.py startapp myapp"""))
    p("This will create a new folder called myapp")
    p("Add the app to INSTALLED_APPS in myproject/settings.py")
    pre(
        code("""
        INSTALLED_APPS = [
            ...
            'myapp',
            ...
        ]
        """))

    p("In the myapp/views.py file we will create our first hypergen view")
    p("Delete everything in this file and make it look like this:")
    pre(
        code("""
        
        from hypergen.imports import *
        
        @liveview(perm=NO_PERM_REQUIRED)
        def step1(request):
            doctype()
            html(
                head(),
                body(
                    h1("Step 1: This is rendered with hypergen"),
                    strong("An awesome HTML rendering engine, where you define templates using python only")
                )
            )
        """))
    p("In order to view this in a browser we can add the view to myapp/urls.py and include the namespaced app in myproject/urls.py."
     )
    p("In the myapp folder create a file named urls.py, and add this content")
    pre(
        code("""
        
        from hypergen.hypergen import autourls
        from myapp import views

        # app_name is important for the liveview and action decoraters 
        app_name = 'myapp'

        # Automatically creates urlpatterns for all functions in views.py decorated with @liveview or @action.
        urlpatterns = autourls(views, namespace="myapp")
        """))
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
        """))
    p("Startup the dev server (python manage.py runserver) and go to localhost:8000/myapp/step1")
    p("If all went well you should see a beautifully rendered HTML page, like in the good old days, no css, no JS just plain HTML."
     )
    p("How is this exciting you might ask... And really its not.. at least not yet. So far we what we have could be acquired just as easy using normal Django template without hypergen."
     )

    h2("Step 2: Base component functions and composablity")
    p("Lets take all this hypergen template rendering out of the view and make it into its own function. Add this new view to myapp/views.py"
     )
    pre(
        code("""
        
        ...
        
        @liveview(perm=NO_PERM_REQUIRED)
        def step2(request):
            template2()
        
        def template2():
            doctype()
            html(
                head(
                    link(href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css")
                ),
                body(
                    h1("Step 2: This is rendered with hypergen "),
                    strong("An awesome HTML rendering engine, where you define templates using python only"),
                    h2("And because hypergen defines html templates in pure python functions these can be refactored into separate functions")
                )
            )
        """))
    p("No need to edit urls.py. Your new view is instantly available and located at localhost:8000/myapp/step2")
    p("How come It looks a lot different now, you might ask. "
        "That's because we took the liberty of adding the water.css stylesheet to this page, using the link() function. "
        "In general: All html tags (<html><div><span><audio> etc.) has an equivalent hypergen function, which was imported from hypergen.template in the beginning of views.py in "
        " this line:")
    pre(code("from hypergen.imports import *"))
    p("Hypergen calls these 'tag-rendering' python functions for html elements. An element takes args and kwargs. Args beeing either text or other elements,"
        " which will be nested inside the corresponding element when rendered. Kwargs will become the named attributes of the element"
     )
    p("Here's is an example:")
    pre(
        code("""
        section(
            "This is a section, with an ", a("link", id_="im-one-of-a-kind", class_="clickable", href="#"), " inside", br(),
            "The link has the id ", i("im-one-of-a-kind")
        )
        """))
    p("which when rendered as html looks like this:")
    pre(
        code("""
        <section>
             This is a section, with an <a id="im-one-of-a-kind" class="clickable" href="#">link</a> inside <br/>
             The link has the id <i>im-one-of-a-kind</i> and a class attribute named <i>clickable</i>
        </section>
        """))
    p("As you can see we can define html elements with python functions; their children with other python functions as arguments; and their attributes with kwargs."
     )
    p(
        'You might have noticed that the class attribute of the a tag, is defined as class_="clickable" instead of just class. ',
        "This is because class is a reserved keyword in django, and therefore cannot be used to name a kwarg. "),
    'Whenever you want to use a reserved keyword for an attribute name you can always just add _ to the end, hypergen will know what you mean'

    h2("Step 3: Behold the ", i("with"), " statement")
    p("Another way you can use base component functions is as context managers. Try adding the following to your views.py"
     )
    pre(
        code("""
        
        ...
        
        @liveview(perm=NO_PERM_REQUIRED)
        def step3(request):
            template3()
                    
        def template3():
            doctype()
            with html():
                with head():
                    link(href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css")
                with body():
                    h1("Step 3: As Context managers")
                    strong("Hypergen base component functions can also be used as context managers")
        """))
    p("Go to localhost:8000/myapp/step3, and enjoy the result")
    p(
        "Using base component functions as context managers with the ", i("with"),
        " statement is a great way to maintain an easy readable indented structure - its easy to see whats inside what - "
        "but also handy when you want to use python other than the base component functions, i.e. a loop that generates a list"
    )
    pre(code("""
        with ul():
            for i in range(20):
                li("I'm number ", i)
        """))
    p(
        "(Actually hypergen is so smart that the above could be writen by sending a list of base components as an argument to ul like so): ",
        pre(code("""ul([li("I'm number ", i) for i in range(20)])""")), "(but don't tell anyone)")

    h2("Step 4: The base template")
    p("Let's move all the boilerplate html code out in its own function. Make it into a @contextmanager and use it in step4"
     )
    pre(
        code("""
        # Add this to the import section in the top of views.py
        from contextlib import contextmanager

        ...
        
        @contextmanager
        def base_template():
            doctype()
            with html():
                with head():
                    link(href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css")
                with body():
                    yield
        
        @liveview(perm=NO_PERM_REQUIRED)
        def step4(request):
            template4()
        
        def template4():
            with base_template():
                h1("Step 4: Now using a base template")
                p("Our code is much simpler now")
        """))

    h2("Step 5: Reusing the base template")
    p("""Now that we have created a new base template, we can add our new base template as a keyword argument to the liveview decorator so that we can avoid all the boilerplate and concentrate on the content part of our template"""
     )
    pre(
        code("""
        
        ...
        
        @liveview(perm=NO_PERM_REQUIRED, base_template=base_template)
        def step5(request):
            template5()
        
        def template5():
            h1("Step 5: Now reusing the base template")
            section("This view is reusing the same base template as step 4")
        """))
    p("""As you might have noticed our code gets a lot cleaner; now is the time for some user action.""")

    h2("Step 6: Introducing hypergen actions")
    p(
        "A hypergen action is a function view that that can be triggered from the client, and usually changes something in the view.",
        "Now, create a new step6 view and template that takes an argument, num_clicks, which is defaulted to 0")

    pre(
        code("""
        
        ...
        
        @liveview(perm=NO_PERM_REQUIRED, base_template=base_template)
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
                button("click me", id_="button", onclick=callback(on_click, num_clicks + 1))
        """))
    p("As you can see we've assigned a callback on the onclick action on the button element, and referenced it to the on_click action, "
        "which we will create now ")
    pre(
        code("""
        ...
        @action(perm=NO_PERM_REQUIRED, target_id='content')
        def on_click(request, num_clicks=0):
            template6(num_clicks)
        """))
    p("Visit localhost:8000/myapp/step6")
    p("The page is now dynamic! When you click the button it calls the on_click action view, and the page updates automatically."
     )

    h2("Conclusion")
    p("This is the end of this very basic step by step getting started tutorial. You now have the basic knowledge for building hypergen liveviews, and using callbacks and actions 💪."
     )
    p("Please check out the", a("examples and documentation", href=reverse("website:documentation")),
        "for more ways to build your web apps using django and hypergen.", "Specifically read up on",
        a("Templates", href=reverse("coredocs:template")), "and", a("Liveviews",
        href=reverse("coredocs:liveviews")), sep=" ", end=".")
