from hypergen.imports import *
from pprint import pformat
from django.http.response import HttpResponse

@action(perm=NO_PERM_REQUIRED)
def alert(request):
    command("alert", "I am lert")

@action(perm=NO_PERM_REQUIRED)
def alert2(request):
    commands = [["alert", "This is an alert!"]]
    return HttpResponse(dumps(commands), status=200, content_type='application/json')

@action(perm=NO_PERM_REQUIRED, target_id="serialized")
def serialization(request, round_tripped_data):
    write(pformat(round_tripped_data))

@action(perm=NO_PERM_REQUIRED)
def morph(request):
    command("hypergen.morph", "morphed", "MORPHED!")

@action(perm=NO_PERM_REQUIRED)
def remove(request):
    command("hypergen.remove", "remove-me")

@action(perm=NO_PERM_REQUIRED)
def hide(request):
    command("hypergen.hide", "hide-me")

@action(perm=NO_PERM_REQUIRED)
def redirect(request):
    command(
        "hypergen.redirect",
        "https://github.com/runekaagaard/django-hypergen/blob/main/src/hypergen/static/hypergen/hypergen.js#:~:text=redirect"
    )
