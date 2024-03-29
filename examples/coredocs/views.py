from hypergen.imports import *

from website.templates2 import base_example_template

@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def template(request):
    with open("coredocs/CORE.rst") as f:
        rst(f.read(), report_level=0)

@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def liveviews(request):
    with open("coredocs/LIVEVIEW.rst") as f:
        rst(f.read(), report_level=0)

@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def django_templates(request):
    with open("coredocs/DJANGO_TEMPLATES.rst") as f:
        rst(f.read(), report_level=0)

@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def websockets(request):
    with open("coredocs/WEBSOCKETS.rst") as f:
        rst(f.read(), report_level=100)
