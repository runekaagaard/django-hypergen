from hypergen.imports import *
from contextlib import contextmanager
import codecs

from django.templatetags.static import static
from website.templates2 import base_example_template

@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def core(request):
    with open("coredocs/CORE.rst") as f:
        rst(f.read(), report_level=0)
