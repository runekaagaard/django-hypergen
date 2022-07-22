from hypergen.imports import *
from hypergen.changeset import *

@liveview(perm=NO_PERM_REQUIRED, user_plugins=[ChangeSet(autosave=True, css_framework=BOOTSTRAP_5)])
def myliveview(request):
    render_messages()
    
    for mine in queryset_changeset(Mine.objects.filter(owner=request.user)):
        h2("Mines")
        with section():
            render_fields(
                mine, "-name", "-description", "*", "extra_info",
                name={"label": "Your name, guy"},
                description={"required": False},
                extra_info={"render": lambda mine: p("I am extra info")},
                validators=[is_owner],
            )
        with section():
            render_fields(mine, "name", "description")

        h2("Thines")
        with section():
            for thine in queryset_changeset(mine.thines.all()):
                render_fields(
                    thine, "thing", "thuse", "more_info", "blouse", h3("Subthings"),
                    thing={"default": "The thing is...."},
                    thuse={"render": render_thuse},
                    more_info={"render": "Go away!"},
                    blouse={"validators": [validate_size]},
                    wrapper=render_very_special_form_group,
                )
                button("Delete this thine", onclick=callback_delete(thine))

            button("Add new thine", onclick=callback_add(thine))
