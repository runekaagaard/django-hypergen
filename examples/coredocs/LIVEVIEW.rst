Liveview
========

A *liveview* is a server-side view that instructs the browser to update parts of the page when DOM events occur. The
HTML for the updated parts is also rendered on the server. The benefits of this is that you can build dynamic webpages without the overhead of a thick client.

The concept was popularized by `Phoenix Liveview <https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html>`_.  Other known liveviews are `StimulusReflex <https://docs.stimulusreflex.com/>`_ for Ruby on Rails and `Liveview <https://laravel-livewire.com/>`__ for PHP's Laravel.

In contrast to Phoenix Liveview and Stimulusreflex, Hypergen is not websockets first. We advocate vanilla HTTP requests as the best choice in most cases. The reason for that is that async programming in Python `is hard <https://superfastpython.com/why-hate-asyncio-python/>`_ and not a very enjoyable experience.

Should you need lower latencies and/or bi-directional communication websockets *are* first class citizens in Hypergen with `documentation available </coredocs/websockets/>`_.

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

@liveview outputs the html to the page, connects client side events to actions and includes javascript media on the page.

Use the ``path``, ``re_path``, ``login_url``, ``redirect_field_name`` and ``raise_exception`` keyword arguments to configure autourls. Hypergen will automatically assign an url to the liveview if ``path`` and ``re_path`` is ommitted.

Set the required permissions with the ``perm`` and ``any_perm`` keyword arguments. Set ``perm`` to ``NO_PERM_REQUIRED`` to allow anonymous access.

Set a base template with the ``base_template`` keyword argument.

You can reverse the url for a liveview by calling the ``myview.reverse(*args, **kwargs)`` function that Hypergen adds for you, e.g.::

    myview.reverse(name=jack) # /myapp/myvyiew/jack/

Arguments and the keyword arguments are passed to the view function.

The full signature is:

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
    session storage. It's available at ``context.hypergen.appstate``. Manipulate that variable and it's automatically stored
    at the end of each request.
*target_id (None)*
    Used internally for partial loading, not very useful in userland.
*autourl (True)*
    Set to False to disable autourls for this view.
*partial (True)*
    Set to False to disable partial loading for this view.
    
@action
=======

The @action decorator return commands to the client to execute. Most of the time partial html to update the ``target_id`` id with. However, it's capable of instructing the client to do `anything you want </commands/commands/>`__.

The arguments to the action comes from the ``callback`` function and Hypergen automatically sends them to the ``action`` function after the request and the path parameters if any.

Most of the time you wouldn't assign a custom url to an action but you *can* use the ``path``, ``re_path`` keyword arguments to configure autourls. Hypergen will automatically assign an url to the action if ``path`` and ``re_path`` is ommitted.

Set the required permissions with the ``perm`` and ``any_perm`` keyword arguments. Set ``perm`` to ``NO_PERM_REQUIRED`` to allow anonymous access.

Make partial loading work by setting a ``base_template`` keyword argument.

You can reverse the url for a action by calling the ``myview.reverse(*args, **kwargs)`` function that Hypergen adds for you, e.g.::

    myview.reverse(name=jack) # /myapp/myvyiew/jack/

Arguments and the keyword arguments are passed to the action function.

For more advanced usages you can write to multiple locations by setting the ``target_id`` variable in the `global context </globalcontext/globalcontext/>`_, e.g::

    @action(perm=NO_PERM_REQUIRED, target_id="foo")
    def my_action(request):
        p("A") # will write to "foo"
        with context(at="hypergen", target_id="bar"):
            p("B") # will write to "bar"
            with context(at="hypergen", target_id="baz"):
                p("C") # will write to "baz"
            p("D") # will write to "bar"

Use the ``base_view`` keyword argument to have that view executed after the action has completed. The base template of the base view will not be called, so the inner template will partially replace the correct content on the page.

The full signature is:
    
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

Callback creates a binding from a client-side DOM event to a server-side @action view. Use it on event handler attributes to html elements, e.g. an ``onclick`` attribute to a ``div`` element::

    div("Click me!", id="my-id", onclick=callback(my_action, {"key": "value"}, [1, 2, 3], {5, 6, 7}))

and the signature of the corresponding action should be::

    @action(perm="myapp.myperm")
    def my_action(request, my_list, my_list, my_set):
        ...

Arguments can be all datatypes that can be json serialized/deserialized, and Hypergen offers special support for the following datatypes: datetime, time, deque, set, frozenset and range.

Reference the value of `form input elements </inputs/>`__ with variables::

    my_input = input_(id="my-input", type="number", value=10)
    button("Submit", id="submit", onclick=callback(save_form, my_input))

Use the contant ``THIS`` to reference the element itself the callback is being defined on::

    textarea(id="my-id", onblur=callback(my_action, THIS))

which would send the value of the textarea to the action when the onblur event occurs.

The full signature is:

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
    Stub
*clear (False)*
    Clear the input element after the event has occured.
*headers (None)*
    Send these HTTP headers back to the server.
*meta (None)*
    Send this meta data back to the server.
*when (None)*
    A dotted path to a frontend predicate function that decides whether to trigger the callback.


call_js
=======

Use this where you would use the ``callback`` function, only it's will not call the server but execute a function on the client. The ``command_path`` should be a dotted path that is available from the ``window`` variable on the client. So for instance::

        div("Hover me", onmouseover=call_js("console.log", "HI"))

would ``console.log`` "HI" everytime you put the mouse over the text.

*call_js(function_path, *args)*
    It's first argument is a dotted path to the function to execute and the arguments will be used as arguments
    to the function.

command
=======

While ``call_js`` is called when a client-side event occurs, commands can be send to the server whenever you want, both inside liveviews and actions, e.g.::

    command("alert", "Remember the milk!")

Read more about commands on the `Client Commands </commands/commands/>`__ page.

*command(function_path, *args)*
    It's first argument is a dotted path to the function to execute and the arguments will be used as arguments
    to the function.
