# coding = utf-8
# pylint: disable=no-value-for-parameter
d = dict

from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED
from hypergen.core import *
from hypergen.core import callback as cb
from hypergen.core import context as c

HYPERGEN_SETTINGS = dict(perm=NO_PERM_REQUIRED, target_id="content", namespace="gameofcython",
    app_name="gameofcython", base_template="foo")

@hypergen_view(url="^$", **HYPERGEN_SETTINGS)
def gameofcython(request):
    pass
