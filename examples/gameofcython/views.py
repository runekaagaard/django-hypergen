# coding = utf-8
# pylint: disable=no-value-for-parameter
d = dict

import datetime

from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED
from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.core import context as c

import templates as shared_templates
from gameofcython.gameofcython import render, reset, step as step_

HYPERGEN_SETTINGS = dict(perm=NO_PERM_REQUIRED, target_id="content", namespace="gameofcython",
    app_name="gameofcython", base_template=shared_templates.base_template)

reset()

@hypergen_view(url="$^", **HYPERGEN_SETTINGS)
def gameofcython(request):
    style("""
        table {
            border-collapse: collapse;
        }
        td {
            width: 4px;
            height: 4px;
            max-height: 4px;
            max-width: 4px;
            padding: 0;
            margin: 0;
            border: 0;
        }
        td.black {
            background-color: black;
        }
    """)
    with div(id_="gameoflife"):
        render()
    div(id_="step", onclick=cb(step))
    script('''
        function fastSetTable(html) {
            document.getElementById("gameoflife").innerHTML = html
        }
        ready(() => document.getElementById("step").click())
    ''')

@hypergen_callback(view=gameofcython, **HYPERGEN_SETTINGS)
def step(request):
    step_()
