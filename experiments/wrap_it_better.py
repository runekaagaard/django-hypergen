from contextlib import contextmanager

def a():
    print("a0")
    # yield "i am a"
    return "xxx"

@contextmanager
def b():
    print("b1")
    yield
    print("b2")

@b()
def c():
    aval = a()
    print("aval", aval)

c()

# mycustomhypergenfeature.py # module
@contextmanager
def wrap_hypergen(template, *args, **kwargs):
    yield

@contextmanager
def wrap_element(element, *args, **kwargs):
    if element is head:
        script(src="hypergen.min.js")
        script("addevent_handler_cache.DOITNOW!")

    yield

@contextmanager
def wrap_t(v, quote=True, *args, **kwargs):
    yield

def wrap_attribute(element, k, v, *args, **kwargs):
    yield
