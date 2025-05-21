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
def display(request):
    command("hypergen.display", "display-me")

@action(perm=NO_PERM_REQUIRED)
def visible(request):
    command("hypergen.visible", "visible-me")

@action(perm=NO_PERM_REQUIRED)
def hidden(request):
    command("hypergen.hidden", "hidden-me")

@action(perm=NO_PERM_REQUIRED)
def append(request):
    command("hypergen.append", "append-me", "<span style='color: green;'> - Appended content</span>")

@action(perm=NO_PERM_REQUIRED)
def prepend(request):
    command("hypergen.prepend", "prepend-me", "<span style='color: blue;'>Prepended content - </span>")

@action(perm=NO_PERM_REQUIRED)
def redirect(request):
    command(
        "hypergen.redirect",
        "https://github.com/runekaagaard/django-hypergen/blob/main/src/hypergen/static/hypergen/hypergen.js#:~:text=redirect"
    )

@action(perm=NO_PERM_REQUIRED)
def set_client_state(request):
    command("hypergen.setClientState", "preferences", {"theme": "dark", "fontSize": "large"})
    # Also log to console so we can see it worked
    command("console.log", "Client state updated:", {"theme": "dark", "fontSize": "large"})

@action(perm=NO_PERM_REQUIRED)
def set_dark_theme(request):
    command("hypergen.setClientState", "preferences.theme", "dark")
    command("document.getElementById('theme-indicator').textContent = 'Current theme: dark'")

@action(perm=NO_PERM_REQUIRED)
def set_light_theme(request):
    command("hypergen.setClientState", "preferences.theme", "light")
    command("document.getElementById('theme-indicator').textContent = 'Current theme: light'")
