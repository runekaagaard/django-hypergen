Hypergens liveview functionality
================================

All liveview functionality is located in the ``hypergen.liveview`` module.

Import everything like this::

    from hypergen.liveview import *

Or TRULY everything::

    from hypergen.imports import *

Autourls
--------

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

The @liveview decorator
-----------------------

The point of the ``@liveview`` is that you decorate your views with it and *everything* works. Liveview ON ;)

**... more is on the way here.**

