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

# liveview.py # module
@contextmanager
def wrap_hypergen(template, *args, **kwargs):
    with context(at="hypergen_liveview", event_handler_callbacks=[], target_id="__main__"):
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

@contextmanager
def hypergen_view():
    with c(at="hypergen", plugins=[translate, liveview]):
        yield

@contextmanager
def base_template():
    print("<body>")
    yield
    print("</body>")

def template():
    print("    <p>Hi</p>")

print("----- A -----")

with base_template():
    template()

print("----- B -----")

@base_template()
def template2():
    print("    <p>Hi2</p>")

template2()

print("----- C -----")

base_template()(template)()

class metastr(str):
    @staticmethod
    def make(string, meta):
        s = metastr(string)
        s.meta = meta

        return s

m = metastr("Hello")
m.meta = 200

print("FOOOOO", m, m.meta)

m2 = metastr.make("I am string", {1, 2, 3})
print("BAR", m2, m2.meta, type(m2), type(m2) is str, isinstance(m2, str))
