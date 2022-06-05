Liveview
========

A *liveview* is a server-side view that instructs the browser to update parts of the page when DOM events occur. The
HTML for the updated parts is also rendered on the server. The benefits of this is that you can build dynamic webpages without the overhead of a thick client.

The concept was popularized by `Phoenix Liveview <https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html>`_.  Other known liveviews are `StimulusReflex <https://docs.stimulusreflex.com/>`_ for Ruby on Rails and `Liveview <https://laravel-livewire.com/>`__ for PHP's Laravel.

In contrast to Phoenix Liveview and Stimulusreflex, Hypergen does not communicate via websockets but uses Djangos vanilla Response/Request cycle. This avoids the land-of-async but adds a bit more latency. Hypergen is great for webpages but not for games says ours experiences.

All liveview functionality lives in the ``hypergen.liveview`` module. Import everything like this::

    from hypergen.liveview import *

or truly everything::

    from hypergen.imports import *

Basics
======

The cornerstones of Hypergen liveview are the two view decorators, ``@liveview`` and ``@action``. The former renders the full HTML page via a GET http response, and the latter renders partial HTML via a POST ajax response. Both are vanilla Django views under the hood. The missing link between the two is the function ``callback()`` that binds DOM events to actions. A simple counter with a liveview, an action and a callback looks like `this </misc/counter/>`__::

    @liveview(path="counter/", perm=NO_PERM_REQUIRED)
    def counter(request):
        doctype()
        with html(), body(), div(id="content"):
            template(1)

    def template(n):
        p("The number is ", n)
        button("Increment", id="increment-it", onclick=callback(increment, n))

    @action(path="increment/", perm=NO_PERM_REQUIRED, target_id="content")
    def increment(request, n):
        template(n + 1)

Both liveviews and actions automatically collects HTML and outputs it to the page. The difference being that actions only renders the inner content of the page. We tell the action into which DOM *id* to render it's output with the ``target_id`` keyword argument. A common pattern is to have the liveview and it's actions share a common inner template.

The callback sends ``n`` to the ``increment`` action.

Html elements having a callback as well as elements used in the callback must have ids. Hypergen will warn you if you forget.

Liveviews, actions and callbacks can do a lot more but before we get into that, please read about autourls and base templates below. Also be sure to check out the documentation pages `Form inputs </inputs/>`__, `Client commands </commands/commands/>`_ and `Partial loading and history support </partialload/page1/>`_.

Autourls
========

Hypergens liveview are smoother to work with when using autourls. That means that in your apps ``urls.py`` module you should be doing::

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

Base templates
==============

To enjoy the full joy of Hypergens liveview define a base template with `html5 boilerplate <https://github.com/h5bp/html5-boilerplate/blob/v8.0.0/dist/doc/html.md>`_ and share it between your views::

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

Setting the ``target_id`` attribute on the base template function tells the action where to render it's output and makes partial loading work automatically. Just pass ``base_template=my_base_template`` to the ``@liveview`` and ``@action`` decorators and Hypergen loves you.

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
  
@liveview
=========

@liveview outputs the html to the page, connects client side events to actions and includes javascript media on the page. The full signature is:

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
=======

The @action decorator return commands to the client to execute. Most of the time partial html to update the ``target_id`` id with. However, it's capable of instructing the client to do anything you want.
    
*@action(path=None, re_path=None, base_template=None, target_id=None, perm=None, any_perm=False, autourl=True, partial=True, base_view=None, appstate=None)*
    ``perm`` is required. It is configured by these keyword arguments:
*target_id (None)*
    Render the generated HTML into this DOM id.
*base_template (None)*
    Uses the ``target_id`` attribute from this function if present.
*base_view* (None)*
    Calls the base_view function after the action has executed. Will not render the base template.
*perm (None)*
    Accepts one or a list of permissions, all of which the user must have. See Djangos `has_perm() <https://docs.djangoproject.com/en/dev/ref/contrib/auth/#django.contrib.auth.models.User.has_perm>`__
*any_perm (False)*
    The user is only required to have one of the given perms. Check which he has in ``context.hypergen.matched_perms``.
*path (None)*
    Autourls registers the view using Djangos `path <https://docs.djangoproject.com/en/dev/ref/urls/#path>`__ function.
*re_path (None)*
    Autourls registers the view using Djangos `re_path <https://docs.djangoproject.com/en/dev/ref/urls/#re-path>`__ function.
*autourl (True)*
    Set to False to disable autourls for this view.
*partial (True)*
    Set to False to disable partial loading for this view.

callback
========

Stub.

Use the contant ``THIS`` to reference the element itself the callback is being defined on. 

*callback(url, *cb_args, debounce=0, confirm_=False, blocks=False, upload_files=False, clear=False, headers=None, meta=None, when=None)*
    ``url`` is required. It is configured by these arguments:
*url*
    A string or an action function to callback to.
*debounce (0)*
    Debounce the DOM event by this number of miliseconds.
*confirm_ (False)*
    Confirm event via a `confirm <https://developer.mozilla.org/en-US/docs/Web/API/Window/confirm>`_ dialog with this confirmation message.
*blocks (False)*
    Block any other hypergen events until the callback has finished.
*upload_files (False)*
    TBD
*clear (False)*
    Clear the input element after the event has occured.
*headers (None)*
    Send these HTTP headers back to the server.
*meta (None)*
    Send this meta data back to the server.
*when (None)*
    A dotted path to a frontend predicate function that decides whether to trigger the callback.

call_js
-------

*call_js(command_path, *args)*

Stub
----
