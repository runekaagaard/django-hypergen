# Only showing the essential code.
from hypergen.imports import *

@liveview(perm=NO_PERM_REQUIRED)
def counter(request):
    doctype()
    with html():
        with body():
            with div(id_="content"):
                template(1)

def template(n):
    with p():
        label("Current value: ")
        input_(type_="number", value=n)
        button("Increment", id_="increment", onclick=callback(increment, n))

@action(perm=NO_PERM_REQUIRED, target_id="content")
def increment(request, n):
    template(n + 1)
