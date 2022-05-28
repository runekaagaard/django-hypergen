from hypergen.imports import *
from contextlib import contextmanager
import codecs

from django.templatetags.static import static
from website.templates2 import show_sources

# Templates - as your app grows you probably want to move them to a templates.py file.

@contextmanager  # base templates must be context managers that yields where the main content will be.
def base_template():
    """
    This base template is meant to be shared between your views.
    """
    doctype()  # all html elements are available as functions.
    with html():  # elements can nest.
        with head():
            if title:
                title("Hello apptemplate")  # arguments to elements becomes the html innerText of the element.
            script(
                src=static("hypergen/hypergen.min.js"))  # keyword arguments becomes html attributes of the element.
            link("https://unpkg.com/simpledotcss@2.0.7/simple.min.css")  # include all you html5 boilerplate.
        with body():  # warning, don't set the target_id directly on the body element, does not work!
            h1("Hello apptemplate")
            p(i("Congratulations on installing your very first Django Hypergen app!"))  # elements can take elements.

            with div(id_="content"):  # see target_id below.
                # The html triggered inside your views will appear here.
                yield

            h1("Where to go from here?")
            with ul():
                li(
                    "Play around with the source at",
                    code("./apptemplate/views.py"),
                    sep=" ",  # arguments are joined by a " " separator.
                )
                li("Read the", a("getting started", href="https://hypergen.it/gettingstarted/begin/"), "guide",
                    sep=" ")
                li("Check out the full", a("documentation", href="https://hypergen.it/documentation/"), sep=" ")
                li("Drop by and", a("say hi", href="https://github.com/runekaagaard/django-hypergen/discussions"),
                    "- we would love to talk to you!", sep=" ")
                li(
                    "Submit ",
                    a("bug reports and feature requests",
                    href="https://github.com/runekaagaard/django-hypergen/issues"))
                li("Go crazy 24/7!")

            show_sources(__file__)

base_template.target_id = "content"

def content_template(encrypted_message=None):
    """
    This template is specific to your view and the actions belonging to it. Composes just like React functions.
    """
    p("Top secret agent? Encrypt your message with a super secret key:")
    input_(
        id_="message",
        # call "my_action" on each oninput event.
        # callback() takes all normal python datatypes and hypergen html elements as input.
        oninput=callback(my_action, THIS),  # 'THIS' means the value of the element it self.
    )
    pre(code(encrypted_message if encrypted_message else "Type something, dammit!"))

# Views - one view normally have multiple actions.

@liveview(perm=NO_PERM_REQUIRED, base_template=base_template)
def my_view(request):
    """
    Views renders html and binds frontend events to actions.
    """
    content_template()

# Actions - if you have a lot, move them to a actions.py file.

@action(perm=NO_PERM_REQUIRED, base_template=base_template)
def my_action(request, message):
    """
    Actions processes frontend events.
    
    This action tells the frontend to put the output of content_template into the 'content' div.

    The 'message' arg is the value of the <input> element.
    """
    content_template(codecs.encode(message if message is not None else "", 'rot_13'))
