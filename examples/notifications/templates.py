from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.core import context as c, t
from website.templates import show_sources

def notifications():
    from notifications.views import mycallback

    h2("How to use a notifications library")
    p(button("Click me for a notification", onclick=cb(mycallback), id_="mycallback"))
    p("So it's important to remember that what both @hypergen_view and @hypergen_callback does is to send a",
        " list of commands to the client to execute. Thus it's trivial to implement a frontend notification system.")
    p("Firstly include your notification library of choice: ")
    pre(
        code("""
script(
    src="https://cdnjs.cloudflare.com/ajax/libs/AlertifyJS/1.13.1/alertify.min.js", integrity=
    "sha512-JnjG+Wt53GspUQXQhc+c4j8SBERsgJAoHeehagKHlxQN+MtCCmFDghX9/AcbkkNRZptyZU4zC8utK59M5L45Iw==",
    crossorigin="anonymous", referrerpolicy="no-referrer")
link(
    rel="stylesheet",
    href="https://cdnjs.cloudflare.com/ajax/libs/AlertifyJS/1.13.1/css/alertify.min.css", integrity=
    "sha512-IXuoq1aFd2wXs4NqGskwX2Vb+I8UJ+tGJEu/Dc0zwLNKeQ7CW3Sr6v0yU3z5OQWe3eScVIkER4J9L7byrgR/fA==",
    crossorigin="anonymous", referrerpolicy="no-referrer")
        """.strip()))

    p("Secondly configure it as you wish:")
    pre(
        code('''
script("""
    alertify.set('notifier','position', 'top-center')
    alertify.set('notifier','delay', 2);
""")
style("""
    .alertify-notifier .ajs-info {
        background-color: rgba(245, 245, 245, 0.95);
    }
""")
        '''.strip()))

    p("Thirdly create a function to iterate over Djangos messages and add an notification command for each ",
        "message:")
    pre(
        code("""
def alert_messages(request):
    for message in get_messages(request):
        command("alertify.notify", t(message), message.level_tag)
        """.strip()))

    p(mark('Notice the use of the "t()" function that makes sure the message is properly escaped.'))
    p("Lastly call that function in both your view and your callbacks:")
    pre(
        code("""
@hypergen_view(perm=NO_PERM_REQUIRED)
def myview(request):
    alert_messages()
    ...

@hypergen_callback(perm=NO_PERM_REQUIRED)
def mycallback(request):
    alert_messages()
    ...

        """.strip()))

    p("Be sure to trust the source Luke :) ↓")
    show_sources(__file__)
