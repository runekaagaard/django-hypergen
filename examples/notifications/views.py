from hypergen.imports import *
from hypergen.hypergen import t

from django.contrib.messages import get_messages
from django.contrib import messages

from website.templates2 import base_example_template

from notifications import templates

def alertify():
    link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/AlertifyJS/1.13.1/css/alertify.min.css",
        integrity="sha512-IXuoq1aFd2wXs4NqGskwX2Vb+I8UJ+tGJEu/Dc0zwLNKeQ7CW3Sr6v0yU3z5OQWe3eScVIkER4J9L7byrgR/fA==",
        crossorigin="anonymous", referrerpolicy="no-referrer")
    script(
        src="https://cdnjs.cloudflare.com/ajax/libs/AlertifyJS/1.13.1/alertify.min.js",
        integrity="sha512-JnjG+Wt53GspUQXQhc+c4j8SBERsgJAoHeehagKHlxQN+MtCCmFDghX9/AcbkkNRZptyZU4zC8utK59M5L45Iw==",
        crossorigin="anonymous", referrerpolicy="no-referrer")

    script("""
        alertify.set('notifier','position', 'top-center')
        alertify.set('notifier','delay', 2);
    """)
    style("""
        .alertify-notifier .ajs-info {
            background-color: rgba(245, 245, 245, 0.95);
        }
    """)

def alert_messages(request):
    for message in get_messages(request):
        command("alertify.notify", t(message), message.level_tag)

@liveview(perm=NO_PERM_REQUIRED)
def notifications(request):
    with base_example_template():
        messages.info(request, "Please notify me!")
        alertify()
        alert_messages(request)
        templates.notifications()

@action(perm=NO_PERM_REQUIRED, target_id=OMIT)
def mycallback(request):
    messages.error(request, "Consider yourself notified...")
    alert_messages(request)
