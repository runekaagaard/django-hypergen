# coding = utf-8
# pylint: disable=no-value-for-parameter
d = dict

from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED
from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.core import context as c

import templates as shared_templates

try:
    from gameofcython.gameofcython import render, reset, step as cstep
    module_found = True
except ModuleNotFoundError:
    module_found = False

HYPERGEN_SETTINGS = dict(perm=NO_PERM_REQUIRED, target_id="content", namespace="gameofcython",
    app_name="gameofcython", base_template=shared_templates.base_template)

RUNNING, STOPPED = "RUNNING", "STOPPED"
STATE = STOPPED

@hypergen_view(url="", **HYPERGEN_SETTINGS)
def gameofcython(request):
    if not module_found:
        p("Cython files are not compiled. Run 'make compile-cython' from the root of the repository.")
        return

    if not c.request.is_ajax():
        reset()

    style("""
        table {
            border-collapse: collapse;
        }
        td {
            width: 6px;
            height: 6px;
            margin: 0;
            border: 0;
        }
        td.black {
            background-color: black;
        }
    """)
    with div(id_="gameoflife"):
        render(str(step.reverse()))
    # div(id_="step", onclick=cb(step))
    script('''
        //ready(() => document.getElementById("step").click())
    ''')

@hypergen_callback(view=gameofcython, **HYPERGEN_SETTINGS)
def step(request, *args):
    c.hypergen = c.hypergen.set("target_id", "content")
    print("STEP ARGS", args)
    if STATE == RUNNING:
        cstep()
    cstep()
