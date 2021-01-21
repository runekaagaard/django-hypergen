"""
Thoughts about autosaving data and general QOL improvements.
"""

## views.py ##

from hypergen import liveview
"""
Use @liveview to make the view become alive. It does the following:

- Sets up a url for the view.
- Monitors usage of models (view, create, etc.), and throws an exception if the user does not have
  the required permissions.
- If "mutates" is true starts a transaction.
- Hook up callback functions to the frontend.
- If "autosave" is true, automatically changes fields changed in the frontend.

To further remove boilerplate, you can add a django object directly in the url. The url should
persist of the objects primary key, and the view will be passed an instance of that object.
"""
from hypergen.dom import h1, p, fieldset, input_


@liveview(url="edit_blog_post/<obj:blog.Post>/", mutates=True, autosave=True)
def edit_blog_post(request, post):
    h1("Edit the post here.")
    p("Changes are automatically saved.")
    with fieldset.c():
        input_(post.title)
        input_(post.description)


##  urls.py ##

# Most of the time, it feels redundant to have to edit urls just to add a view, so lets allow a
# view function to define it's own url.

from hypergen import urls_from_views
from blog import views

urlpatterns = urls_from_views(views)

## model.py ##

from django import db
from hypergen import db as hdb, context
"""
Use the HypergenModelMixin class to enable automatic authorisation of view_(all|own|etc),
update_(all|own|etc), create_(all|own|etc) and delete_(all|own|etc) actions when inside a
@liveview context. Hypergen automatically creates permissions for defined perm_actions and
perm_access_types.
"""


class BaseModel(db.Model):
    owner = db.ForeignKey("auth.User")

    class Meta:
        abstract = True

    class HypergenMeta:
        """
        This creates 12 permissions for this model:
            view_all, view_own, view_other, update_all, update_own, ...
        """
        perm_actions = ("view", "update", "create", "delete")
        perm_access_types = ("all", "own", "other")

        # Define access types.

        def perm_access_type_all(self):
            return True

        def perm_access_type_own(self):
            return self.owner == context.request.user

        def perm_access_type_other(self):
            return self.owner != context.request.user


class Post(BaseModel, hdb.LiveviewModelMixin):
    title = db.TextField()
    content = db.TextField()
