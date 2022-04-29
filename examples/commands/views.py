from hypergen.contrib import hypergen_view, NO_PERM_REQUIRED
from hypergen.core import *
from hypergen.core import callback as cb

from website.templates import base_example_template, show_sources

from commands import templates

@hypergen_view(perm=NO_PERM_REQUIRED)
def commands(request):
    with base_example_template():
        templates.commands()

        show_sources(__file__)
