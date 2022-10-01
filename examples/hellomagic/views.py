from hypergen.imports import *
from website.templates2 import base_template

HYPER = dict(perm=NO_PERM_REQUIRED, base_template=base_template)

@liveview(**HYPER)
def counter(request):
    template(0)

@action(**HYPER)
def increment(request, n):
    template(n + 1)

def template(n):
    label("Current value: ")
    input_(id_="n", type_="number", value=n)
    button("Increment", id_="increment", onclick=callback(increment, n))
