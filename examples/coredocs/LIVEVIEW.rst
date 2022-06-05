Liveview
========

A *liveview* is a server-side view that instructs the browser to update parts of the page when DOM events occur. The
HTML for the updated parts is also rendered on the server. The benefits of this is that you can build dynamic webpages without the overhead of a thick client.

The concept was popularized by `Phoenix Liveview <https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html>`_.  Other known liveviews are `StimulusReflex <https://docs.stimulusreflex.com/>`_ for Ruby on Rails and `Liveview <https://laravel-livewire.com/>`_ for PHP's Laravel.

In contrast to Phoenix Liveview and Stimulusreflex, Hypergen does not communicate via websockets but uses Djangos vanilla Response/Request cycle. This avoids the land-of-async but adds a bit more latency. Hypergen is great for webpages but not for games says ours experiences.

All liveview functionality lives in the ``hypergen.liveview`` module. Import everything like this::

    from hypergen.liveview import *

or truly everything::

    from hypergen.imports import *

Basics
======

The cornerstones of Hypergen liveview are the two view decorators, ``@liveview`` and ``@action``. The former renders the full HTML page via a GET http response, and the latter renders partial HTML via a POST ajax response. Both are vanilla Django views under the hood. The missing link between the two is the function ``callback()`` that binds DOM events to callbacks. A simple counter with a liveview, an action and a callback looks like this::

    @liveview(path="counter/", perm=NO_PERM_REQUIRED)
    def counter(request):
        doctype()
        with html(), body(), div(id="content"):
            template(1)

    def template(n):
        p("The number is", n, sep=" ", end="")
        button("Increment", id="increment-it", onclick=callback(increment, n))

    @action(path="increment", perm=NO_PERM_REQUIRED, target_id="content")
    def increment(request, n):
        template(n + 1)

Both liveviews and actions automatically collects HTML and outputs it to the page. The difference being that actions only renders the inner content of the page. We tell the action into which DOM *id* to render it's output with the ``target_id`` keyword argument.


Autourls
========

First a little sidenote. Hypergens liveview features works best if you are using autourls. That means that in your apps ``urls.py`` module you should be doing::

    from hypergen.hypergen import autourls
    from myapp import views

    app_name = 'myapp'

    # Automatically creates urlpatterns for all functions in views.py decorated with @liveview or @action.
    urlpatterns = autourls(views, namespace="myapp")

And in your ``views.py`` file your should reverse urls to other views directly on the views as::

    from hypergen.imports import *
    
    @liveview(path="view1/<int:user_id>/", perm=NO_PERM_REQUIRED)
    def view1(request, user_id):
        with html(), body():
            a("Go to view2", href=view2.reverse())

    @liveview(perm=NO_PERM_REQUIRED)
    def view2(request):
        with html(), body():
            a("Go to view1", href=view1.reverse(user_id=42))

Going live in 1...2...3
=======================

With the autourls out of the way, you need to know about three functions and you are ready to fly:

1. ``@liveview``: Decorate your view with ``@liveview`` and it's a live. Liveviews generates a full HTML
   page. 
2. ``callback``: Binds an event on the client to a view on the server. These kind of views are called actions.
3. ``@action``: Decorate your view with ``@action`` and it's an action. Actions can do anything, but most of the
   time it partially updates the inner content of the html page.

See the details below.

Base templates
--------------

To enjoy the full joy of Hypergens liveview always start by defining a base template with `html5 boilerplate <https://github.com/h5bp/html5-boilerplate/blob/v8.0.0/dist/doc/html.md>`_ that can be shared between your views::

    from contextlib import contextmanager
    from hypergen.template import *

    @contextmanager
    def my_base_template():
        doctype()
        with html():
            with head():
                title("My awesome page")
            with body():
                with div(id="content"): # Matches below.
                    # Inner content goes here.
                    yield

    my_base_template.target_id = "content" # Matches above.

You must set the ``target_id`` attribute!. Then just pass ``base_template=my_base_template`` to the ``@liveview`` and ``@action`` decorators and Hypergen loves you.

.. raw:: html

    <details>
        <summary>Make your base templates configurable with a HOF</summary>
        <p>Since we are using Python it's super easy to e.g. customize the title
           of your base template:
        </p>
        
    <pre><code>def my_base_template(title):
        @contextmanager
        def _my_base_template(): 
            doctype()
            with html():
                with head():
                    title(title)
                with body():
                    with div(id="content"): # Matches below.
                        # Inner content goes here.
                        yield

        _my_base_template.target_id = "content" # Matches above.

        return _my_base_template</code></pre>

    <p>
        Then pass <code>base_template=my_base_template(title="My awesome title")</code> to the
        <code>@liveview</code> and <code>@action</code> decorators.
    </p>

    </details>

Actually using liveview
-----------------------

With your autourls setup, a fresh base template, boldly go where extremely few have ever gone and make two *liveviews*, one *action* and bind a client side event to the action by defining a *callback*::

    @liveview(perm=NO_PERM_REQUIRED, base_template=my_base_template)
    def page1(request):
        h1("Hello page 1")
        with p():
            a("You should go to page2", href=page2.reverse())

    @liveview(perm=NO_PERM_REQUIRED, base_template=my_base_template)
    def page2(request):
        el = input_(placeholder="Write a number", type="number", id="input")
        button("Double it", id="button", onclick=callback(double, el))

    @action(perm=NO_PERM_REQUIRED, base_template=my_base_template)
    def double(request, n):
        p("The double of", n, "is", n * 2, sep=" ", end=".")
        command("alert", n * 2)

You get a beautiful website that looks like `so </misc/page1/>`_. Lets try and unpack whats going on:

- Get the url as a string with additional metadata that hypergen needs like ``page2.reverse()``. Args and kwargs
  given to the reverse function will be reversed as argument and keywork arguments to the view. 
- Inside both @liveview and @action just start writing html and hypergen will draw it on the screen.
- The base_template argument to @action instructs hypergen where to put the html. In this case inside
  the div element with the id ``content``. Remember ``my_base_template.target_id = "content"``.
- The ``callback(double, el)`` bit invokes the double action with the n argument as the value of the input
  element.
- Html elements having a callback as well as elements used in the callback must have ids. Hypergen will warn you
  if you forget.
- The ``command("alert", n * 2)`` line instructs the frontend to show an alert.

Check the documentation pages "Form inputs", "Client commands" and "Partial loading and history support".
  
@liveview
---------

@liveview outputs the html to the page, connects client side events to actions and includes hypergen.js on the page. The full signature is:

*@liveview(path=None, re_path=None, base_template=None, perm=None, any_perm=False, login_url=None, raise_exception=False, redirect_field_name=None, autourl=True, partial=True, target_id=None, appstate=None)*
    ``perm`` is required. It is configured by these keyword arguments:
*perm (None)*
    Accepts one or a list of permissions, all of which the user must have. See Djangos `has_perm() <https://docs.djangoproject.com/en/dev/ref/contrib/auth/#django.contrib.auth.models.User.has_perm>`_
*any_perm (False)*
    The user is only required to have one of the given perms. Check which he has in ``context.hypergen.matched_perms``.
*path (None)*
    Autourls registers the view using Djangos `path <https://docs.djangoproject.com/en/dev/ref/urls/#path>`_ function.
*re_path (None)*
    Autourls registers the view using Djangos `re_path <https://docs.djangoproject.com/en/dev/ref/urls/#re-path>`_ function.
*base_template (None)*
    Wrap the html written inside the view with a base template contextmanager function. This makes it simple for
    multiple views to share the same base template, and enables automatic partial page loading. The base template
    function must have a ``my_base_template.target_id = "my-inner-id"`` attribute set for partial loading to work.
*login_url (None)*
    Redirect to this url if the user doesn't have the required permissions.
*redirect_field_name (None)*
    Use this as this name as the next parameter on the login page, defaults to ``?next=/myapp/myview``.
*raise_exception (False)*
    Raise an exception instead if the user does not have the required permissions.
*appstate (None)*
    Executes a callback function the return of which initializes a persistent datastructure living in Djangos
    session storage. It's available at ``context.appstate``. Manipulate that variable and it's automatically stored
    at the end of each request.
*target_id (None)*
    Used internally, not a public variable.
*autourl (True)*
    Set to False to disable autourls for this view.
*partial (True)*
    Set to False to disable partial loading for this view.
    
@action
-------

@callback
---------

call_js
-------

THIS
----

Life cycle
==========
