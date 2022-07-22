from hypergen.imports import *
from hypergen.changeset import *

@liveview(perm=NO_PERM_REQUIRED, user_plugins=[ChangeSet(autosave=True)])
def myliveview(request):
    render_messages()
    
    for mine in Mine.objects.filter(owner=request.user).as_changeset():
        h2("Mines")
        with section():
            render_fields(
                mine, "-name", "-description", "*", "extra_info",
                name={"label": "Your name, guy"},
                description={"required": False},
                extra_info={"render": lambda mine: p("I am extra info")}
                validators=[is_owner],
            )
        with section():
            render_fields(mine, "name", "description")

        h2("Thines")
        with section():
            for thine in mine.thines.all().as_changeset():
                render_fields(
                    thine, "thing", "thuse", "blouse",
                    thing={"default": "The thing is...."},
                    thuse={"render": render_thuse},
                    blouse={"validators": [validate_size]},
                )
                button("Delete this thine", onclick=thine.callback_delete())

            button("Add new thine", onclick=thines.thine.callback_add())
