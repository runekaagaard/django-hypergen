Hypergens liveview functionality
================================

The concept *liveview* was popularized by `Phoenix Liveview <https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html>`_.  Other known liveviews are `StimulusReflex <https://docs.stimulusreflex.com/>`_ for Ruby on Rails and `Liveview <https://laravel-livewire.com/>`_ for PHP's Laravel.

In contrast to Phoenix Liveview and Stimulusreflex, Hypergen does not communicate via websockets but uses Djangos vanilla Response/Request cycle. This avoids the land-of-async but adds a bit more latency. Hypergen is great for webpages but not for games says ours experiences.

All liveview functionality is located in the ``hypergen.liveview``. Import everything like this::

    from hypergen.liveview import *

Or TRULY everything::

    from hypergen.imports import *

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
            
The @liveview decorator
-----------------------

The full signature of @liveview is:

*@liveview(path=None, re_path=None, base_template=None, perm=None, any_perm=False, login_url=None, raise_exception=False, redirect_field_name=None, autourl=True, partial=True, target_id=None, appstate=None)*
    ``perm`` is required. It is configured by these keyword arguments:
*perm (None)*
    Accepts one are at list of permissions all of which the user must have. See Djangos `has_perm() <https://docs.djangoproject.com/en/dev/ref/contrib/auth/#django.contrib.auth.models.User.has_perm>`_
*any_perm (False)*
    The user is only required to have one of the given perms. Check which one in ``context.hypergen.matched_perms``.
*path (None)*
    Autourls registers the view using Djangos `path <https://docs.djangoproject.com/en/dev/ref/urls/#path>`_ function.
*re_path (None)*
    Autourls registers the view using Djangos `re_path <https://docs.djangoproject.com/en/dev/ref/urls/#re-path>`_ function.
*base_template (None)*
    Wrap the html written inside with view with a base template contextmanager function. This makes it simple for
    multiple views to share the same base template, and enables automatic partial page loading. The base template
    function must have a ``my_base_template.target_id = "my-inner-id"`` attribute set for partial loading to work.
    
*login_url (None)*
    Redirect to this url if the user doesn't have the required permissions.
*redirect_field_name (None)*
    Use this as this name as the next parameter on the login page, defaults to ``?next=/myapp/myview``.x
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
    
