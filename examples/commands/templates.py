from hypergen.imports import *
from datetime import date, datetime
import inspect

from commands.actions import *

def fn(title, description, fun):
    if title:
        h3(title)
    if description:
        p(description)
    pre(code(inspect.getsource(fun)))

def show_button():
    button(
        "run",
        id_="serialization",
        onclick=callback(
        serialization,
        {
        "string": "hi",
        "int": 42,
        "float": 9.9,
        "list": [1, 2, 3],
        "range": range(1, 10, 2),
        "tuple": (1, 2, 3),
        "dict": {"key": "value"},
        "set": {1, 2, 3},
        "frozenset": frozenset({1, 2, 3}),
        "date": date(2022, 1, 1),
        "datetime": datetime(2022, 1, 1, 10, 11, 23),},
        ),
    )

def commands():
    h2("Client commands")
    p(
        "When in a hypergen context commands can be sent to the frontend for execution. A command is a list where the first element is a dotted path to a javascript function available from ",
        code("window"), " or in the executing script. The remaining elements are used as arguments to the function.",
        sep=" ")
    p("This command alerts the user:")
    pre(code('["alert", "Whats up?"]'))
    p("Commands lives in the", code("hypergen.commands"),
        "list in the global context. So to manually add commands one would:", sep=" ")
    pre(
        code("""
from hypergen.context import context

def my_view_or_callback(request):
    context.hypergen.commands.append(["alert", "Whats up?"])
""".strip()))

    p("The function", code("command()"), "available in hypergen.liveview is normally used as a shortcut:", sep=" ")
    pre(
        code("""
from hypergen.liveview import command
        
def my_view_or_callback(request):
    command("console.log", "Whats up?", [1, 2, 3])
    """.strip()))

    h2("Examples of client commands")
    fn("Run a generic javascript command", "It must be available in the window scope.", alert)
    button("run", id_="alert", onclick=callback(alert))

    fn("Run a generic javascript command 2", "Manually returns commands.", alert2)
    button("run", id_="alert2", onclick=callback(alert2))

    h3("Serialization")
    p("Data can move a round in different ways:")
    ol(
        li("server->client: As arguments to the callback (cb) function on e.g. onclick events on html elements."),
        li("client->server: As arguments to @action functions."),
        li("server->client: As arguments to client commands."),
    )
    fn(None, "Consider this template function:", show_button)
    fn(
        None, "The most popular python data types are supported. Notice that pythons json.dumps force converts "
        "tuples to lists :(", serialization)

    show_button()
    pre(code("Press the button!", id_="serialized"))

    h2("Hypergen commands")
    p(
        "These are the commands hypergen provides, see how they are implemented at ",
        a(
        "the source", href=
        "https://github.com/runekaagaard/django-hypergen/blob/main/src/hypergen/static/hypergen/hypergen.js#:~:text=morph"
        ), ".")

    fn("morph", "Takes an id and the content to replace it with.", morph)
    button("run", id_="morph", onclick=callback(morph))
    span("Old content", id_="morphed")
    p("Uses the great DOM diff/patching tool ", a("morphdom", href="https://github.com/patrick-steele-idem/morphdom"),
        ".")

    fn("remove", "Takes an id and removes it.", remove)
    button("run", id_="remove", onclick=callback(remove))
    span("Still here", id_="remove-me")

    fn("hide", "Takes an id and hides it.", hide)
    button("run", id_="hide", onclick=callback(hide))
    span("Still displayed", id_="hide-me")
    
    fn("display", "Takes an id and displays it by setting display to 'block' or a custom value.", display)
    button("run", id_="display", onclick=callback(display))
    span("I was hidden", id_="display-me", style={"display": "none"})
    
    fn("visible", "Takes an id and makes it visible by setting visibility to 'visible'.", visible)
    button("run", id_="visible", onclick=callback(visible))
    span("I was invisible", id_="visible-me", style={"visibility": "hidden"})
    
    fn("hidden", "Takes an id and makes it invisible by setting visibility to 'hidden'.", hidden)
    button("run", id_="hidden", onclick=callback(hidden))
    span("Soon to be invisible", id_="hidden-me")
    
    fn("append", "Takes an id and appends HTML to it.", append)
    button("run", id_="append-btn", onclick=callback(append))
    div("Original content", id_="append-me")
    
    fn("prepend", "Takes an id and prepends HTML to it.", prepend)
    button("run", id_="prepend-btn", onclick=callback(prepend))
    div("Original content", id_="prepend-me")

    fn("redirect", "Takes an url and redirects to it.", redirect)
    button("run", id_="redirect", onclick=callback(redirect))
    
    fn("setClientState", "Sets a value in the client-side state that persists between requests.", set_client_state)
    button("Store theme preference", id_="set-state-btn", onclick=callback(set_client_state))
    p("Open browser console to see the state")
    
    h3("State Management Example")
    p("Client state can be accessed from JavaScript with hypergen.clientState:")
    script("""
    document.addEventListener('DOMContentLoaded', function() {
        // Check if we have a stored theme preference
        if (hypergen.clientState && hypergen.clientState.preferences) {
            console.log('Found stored theme:', hypergen.clientState.preferences.theme);
            // Apply the theme
            document.getElementById('theme-indicator').textContent = 
                'Current theme: ' + hypergen.clientState.preferences.theme;
        }
    });
    """)
    p("Theme preference:", span("none set", id_="theme-indicator"))
    button("Set Dark Theme", id_="dark-theme", onclick=callback(set_dark_theme))
    button("Set Light Theme", id_="light-theme", onclick=callback(set_light_theme))
