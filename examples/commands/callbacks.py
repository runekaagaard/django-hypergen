from pprint import pformat

from hypergen.contrib import NO_PERM_REQUIRED, hypergen_callback
from hypergen.core import OMIT, command, write

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id=OMIT)
def alert(request, message):
    command("alert", message)

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id=OMIT)
def alert2(request, message):
    return [["alert", message]]

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id="serialized")
def serialization(request, round_tripped_data):
    write(pformat(round_tripped_data))

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id=OMIT)
def morph(request, message):
    command("hypergen.morph", "morphed", message)

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id=OMIT)
def remove(request):
    command("hypergen.remove", "remove-me")

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id=OMIT)
def hide(request):
    command("hypergen.hide", "hide-me")

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id=OMIT)
def redirect(request):
    command(
        "hypergen.redirect",
        "https://github.com/runekaagaard/django-hypergen/blob/main/src/hypergen/static/hypergen/hypergen.js#:~:text=redirect"
    )
