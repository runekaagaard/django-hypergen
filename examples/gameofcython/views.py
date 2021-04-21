# coding = utf-8
# pylint: disable=no-value-for-parameter
d = dict

import datetime

from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED
from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.core import context as c

import templates as shared_templates
from gameofcython.gameofcython import render

HYPERGEN_SETTINGS = dict(perm=NO_PERM_REQUIRED, base_template=shared_templates.base_template, target_id="content",
    namespace="gameofcython", app_name="gameofcython")

@hypergen_view(url="$^", **HYPERGEN_SETTINGS)
def gameofcython(request):
    raw(render())

@hypergen_callback(perm=NO_PERM_REQUIRED, namespace="gameofcython")
def submit(request, value, target_id):
    pass
