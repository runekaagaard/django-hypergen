# coding=utf-8
d = dict

from django.templatetags.static import static

from contextlib import contextmanager
from .hypergen.core import *

NORMALISE = "https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css"
SAKURA = "https://unpkg.com/sakura.css/css/sakura.css"

@contextmanager
def base_template():
    doctype()
    with html():
        with head():
            title("Hypergen Examples")
            script(src=static("hypergen/hypergen.min.js"))
            # link(NORMALISE)
            # link(SAKURA)
            style("""
                html { margin: auto; max-width: 1200px; }
                dt { font-weight: bold; }
                @media screen and (max-width: 800px) {
                  table thead {
                    display: none;
                  }
                  table td {
                    display: flex;
                  }

                  table td::before {
                    content: attr(label);
                    font-weight: bold;
                    width: 120px;
                    min-width: 120px;
                  }
                }
            """)

        with body():
            p(a("Home", href="/"))
            with div(id_="content"):
                yield
