# coding = utf-8
# pylint: disable=no-value-for-parameter
d = dict

from hypergen.imports import *

from website.templates2 import base_template, show_sources

try:
    from gameofcython.gameofcython import render, reset, step as cstep
    module_found = True
except ImportError:  # ModuleNotFoundError not in python3.5
    module_found = False

HYPERGEN_SETTINGS = dict(perm=NO_PERM_REQUIRED, base_template=base_template)

RUNNING, STOPPED = "RUNNING", "STOPPED"
STATE = STOPPED

def is_ajax(request=None):
    if request is None:
        request = context.request

    return request.META.get('HTTP_X_REQUESTED_WITH', None) == 'XMLHttpRequest'

@liveview(re_path="^$", **HYPERGEN_SETTINGS)
def gameofcython(request):
    if not module_found:
        p("Cython files are not compiled. Run 'make cython-compile' from the root of the repository.")
        return

    if not is_ajax():
        reset()

    style("""
        table {
            border-collapse: collapse;
            width: 600px;
        }
        td {
            width: 6px;
            height: 6px;
            margin: 0;
            border: 0;
            padding: 0;
        }
        td.black {
            background-color: black;
        }
    """)
    script("""
        function run() {
            setInterval(function() {
                document.getElementById("step").click()
            }, 50)
        }
    """)
    with div(id_="gameoflife"):
        render(str(step.reverse()))

    if not is_ajax():
        show_sources(__file__)

@action(base_view=gameofcython, **HYPERGEN_SETTINGS)
def step(request, *args):
    context.hypergen = context.hypergen.set("target_id", "gameoflife")
    cstep()
