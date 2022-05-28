from hypergen.imports import *

from website.templates2 import base_example_template, show_sources

from commands import templates

@liveview(perm=NO_PERM_REQUIRED)
def commands(request):
    with base_example_template():
        templates.commands()

        show_sources(__file__)
