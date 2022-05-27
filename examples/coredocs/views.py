from contextlib import contextmanager
import codecs

from hypergen.core import *
from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED, base_template

from django.templatetags.static import static
from website.templates import base_example_template

@hypergen_view(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def core(request):
    with open("coredocs/CORE.rst") as f:
        rst(f.read(), report_level=0)