from hypergen.imports import *
from hypergen.hypergen import t

from django.contrib.messages import get_messages
from django.http.response import HttpResponseRedirect

def alertify_messages():
    for message in get_messages(context.request):
        command("alertify.notify", t(message), message.level_tag)

class AlertifyPlugin:
    def __init__(self, position="bottom-center", delay=5):
        self.position = position
        self.delay = delay

    def process_html(self, html):
        def template():
            script(
                src="https://cdnjs.cloudflare.com/ajax/libs/AlertifyJS/1.13.1/alertify.min.js", integrity=
                "sha512-JnjG+Wt53GspUQXQhc+c4j8SBERsgJAoHeehagKHlxQN+MtCCmFDghX9/AcbkkNRZptyZU4zC8utK59M5L45Iw==",
                crossorigin="anonymous", referrerpolicy="no-referrer")
            link(
                rel="stylesheet",
                href="https://cdnjs.cloudflare.com/ajax/libs/AlertifyJS/1.13.1/css/alertify.min.css", integrity=
                "sha512-IXuoq1aFd2wXs4NqGskwX2Vb+I8UJ+tGJEu/Dc0zwLNKeQ7CW3Sr6v0yU3z5OQWe3eScVIkER4J9L7byrgR/fA==",
                crossorigin="anonymous", referrerpolicy="no-referrer")
            script(f"""
                alertify.set('notifier','position', '{self.position}')
                alertify.set('notifier','delay', {self.delay});
                """)
            style("""
                    .alertify-notifier .ajs-info {
                        background-color: rgba(245, 245, 245, 0.95);
                    }
                """)

        # Inject media.
        if "<head>" in html:
            assert html.count("<head>") == 1, "Ooops, multiple <head> tags found. There can be only one!"
            return html.replace("<head>", "<head>" + hypergen(template))
        elif "<html>" in html:
            assert html.count("<html>") == 1, "Ooops, multiple <html> tags found. There can be only one!"
            return html.replace("<html>", "<html><head>" + hypergen(template) + "</head>")
        else:
            return hypergen(template) + html

    def template_after(self, template_result, **kwargs):
        # Don't empty message list when we are redirecting to a new page.
        if isinstance(template_result, HttpResponseRedirect) or "hypergen.redirect" in (x[0]
            for x in context.hypergen.commands):
            return
        alertify_messages()
