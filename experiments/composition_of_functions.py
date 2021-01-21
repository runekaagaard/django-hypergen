"""
Whats the best way of composing the HTML builder functions?

state.html is a flat list of either string or callable. It gets joined in
the very end of hypergen. Callables are called and treated like children
to the write function. No one else should join to string but return a list
if needed.
"""


class Meta(object):
    pass


class Html(list):
    def __init__(self, L=None, meta=None):
        super(Html, self).__init__(L if L is not None else [])
        self.meta = Meta()


class state(object):
    html = Html()


def write(*children, **kwargs):
    into = kwargs.get("into", state.html)
    for x in children:
        into.append(x)


def element_start(tag, children, **attrs):
    write("<tag ", ((k, v) for k, v in attrs), ">", **attrs)


def element_end(tag):
    write("</tag>")


def element(tag, children, lazy=False, **attrs):
    # Needs to return nothing.
    if lazy is True:
        write(lambda: element(tag, children, **attrs))
        return
    else:
        element_start(tag, children, **attrs)
        element_end(tag)


def element_ret(tag, children, **attrs):
    # Needs to return a list of html.
    into = Html()
    element(tag, children, into=into, **attrs)
    return into


def input_(**attrs):
    # Return how to use as a callback argument (client element value).
    pass


def input_ret(**attrs):
    # Return:
    #     - How to use as a callback argument (client element value).
    #       Or just the id and type?
    #     - A list of html.
    pass


def div(*children, **attrs):
    # Needs to returns nothing.
    return element("div", children, **attrs)


def div_ret(*children, **attrs):
    # Returns a list of html.
    pass


x = Html([10, 20, 30], {"foo": 92})
x.meta.foo = 91919
print x, x.meta.foo

for y in x:
    print y

x.mega = 91
print x.mega

z = Html([9, 19])
x.extend(z)
print x
