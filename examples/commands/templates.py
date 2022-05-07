from datetime import date, datetime
import inspect

from hypergen.core import *
from hypergen.core import callback as cb

from commands.callbacks import *

def fn(title, description, fun):
    if title:
        h3(title)
    if description:
        p(description)
    pre(code(inspect.getsource(fun)))

def show_button():
    button(
        "run", id_="serialization", onclick=cb(
        serialization, {
        "scalars": [1, 2.2, "string"],
        "lists": [1, 2, 3],
        "tuples": (1, 2, 3),
        "dicts": {"key": "value"},
        "date": date(2022, 1, 1),
        "datetime": datetime(2022, 1, 1, 10, 11, 23),}))

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
from hypergen.core import context

def my_view_or_callback(request):
    context.hypergen.commands.append(["alert", "Whats up?"])
""".strip()))

    p("The function", code("command()"), "available in hypergen.core is normally used as a shortcut:", sep=" ")
    pre(
        code("""
from hypergen.core import *

def my_view_or_callback(request):
    command("console.log", "Whats up?", [1, 2, 3])
    """.strip()))

    h2("Examples of client commands")
    fn("Run a generic javascript command", "It must be available in the window scope.", alert)
    button("run", id_="alert", onclick=cb(alert, "This is an alert!"))

    fn("Run a generic javascript command 2", "Manually returns commands.", alert2)
    button("run", id_="alert2", onclick=cb(alert2, "This is an alert!"))

    h3("Serialization")
    p("Data can move a round in different ways:")
    ol(
        li("server->client: As arguments to the callback (cb) function on e.g. onclick events on html elements."),
        li("client->server: As arguments to @liveview_callback functions."),
        li("server->client: As arguments to client commands."),
    )
    fn(None, "Consider this template function:", show_button)
    fn(None, "The most popular python data types are supported.", serialization)

    show_button()
    pre(code(id_="serialized"))

    h2("Hypergen commands")
    p(
        "These are the commands hypergen provides, see how they are implemented at ",
        a(
        "the source", href=
        "https://github.com/runekaagaard/django-hypergen/blob/main/src/hypergen/static/hypergen/hypergen.js#:~:text=morph"
        ), ".")

    fn("morph", "Takes an id and the content to replace it with.", morph)
    button("run", id_="morph", onclick=cb(morph, "MORPHED!"))
    span("Old content", id_="morphed")
    p("Uses the great DOM diff/patching tool ", a("morphdom", href="https://github.com/patrick-steele-idem/morphdom"),
        ".")

    fn("remove", "Takes an id and removes it.", remove)
    button("run", id_="remove", onclick=cb(remove))
    span("Still here", id_="remove-me")

    fn("hide", "Takes an id and hides it.", hide)
    button("run", id_="hide", onclick=cb(hide))
    span("Still displayed", id_="hide-me")

    fn("redirect", "Takes an url and redirects to it.", redirect)
    button("run", id_="redirect", onclick=cb(redirect))
