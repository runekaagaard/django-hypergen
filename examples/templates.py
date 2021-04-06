# coding=utf-8
d = dict

from django.templatetags.static import static

from contextlib import contextmanager
from freedom.hypergen import *

NORMALISE = "https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css"
SAKURA = "https://unpkg.com/sakura.css/css/sakura.css"

@contextmanager
def base_template():
    doctype()
    with html():
        with head():
            title("Hypergen Examples")
            script(src=static("freedom/hypergen.min.js"))
            link(NORMALISE)
            link(SAKURA)

        with body(style=d(max_width="none")):
            with div(id_="content"):
                yield
