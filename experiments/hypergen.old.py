# coding=utf-8
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import string, sys, json
from threading import local
from contextlib import contextmanager
from collections import OrderedDict
from functools import wraps

### Python 2+3 compatibility ###

if sys.version_info.major > 2:
    from html import escape

    def items(x):
        return x.items()

else:
    from cgi import escape
    str = unicode

    def items(x):
        return x.iteritems()


### Globals ###

state = local()
UPDATE = 1

### Control ###


def hypergen(func, *args, **kwargs):
    auto_id = kwargs.pop("auto_id", False)
    try:
        state.html = []
        state.cache_client = kwargs.pop("cache_client", None)
        state.id_counter = base65_counter() if auto_id else None
        state.id_prefix = (kwargs.pop("id_prefix") + "."
                           if "id_prefix" in kwargs else "")
        state.auto_id = kwargs.pop("auto_id", False)
        state.target_id = target_id = kwargs.pop("target_id", False)
        state.liveview = kwargs.pop("liveview", False)
        as_deltas = kwargs.pop("as_deltas", False)
        func(*args, **kwargs)
        html = "".join(state.html)
    finally:
        state.html = []
        state.cache_client = None
        state.id_counter = None
        state.id_prefix = ""
        state.auto_id = False
        state.liveview = False
        state.target_id = None

    if as_deltas:
        return [[UPDATE, target_id, html]]
    else:
        return html


hypergen(lambda: None)  # Reset global state.


class SkipException(Exception):
    pass


@contextmanager
def skippable():
    try:
        yield
    except SkipException:
        pass


@contextmanager
def cached(ttl=3600, **kwargs):
    hash_value = "HPG{}".format(
        hash(tuple((k, kwargs[k]) for k in sorted(kwargs.keys()))))

    client = state.cache_client
    html = client.get(hash_value)

    if html is not None:
        state.extend((html, ))
        raise SkipException()
    else:
        a = len(state.html)
        kwargs.update({'hash': hash_value})
        yield Bunch(kwargs)
        b = len(state.html)
        client.set(hash_value, "".join(x for x in state.html[a:b]), ttl)


### Building HTML ###


def element_open(tag,
                 children=[],
                 into=state.html,
                 liveview=state.liveview,
                 **attrs):
    """
    >>> element_open("div", class_="hello")
    '<div class="hello">'
    >>> element_open("li", [1, 2], a=3, b_=4, sep=".", style={1: 2}, x=True,
    ...    y=False, _sort_attrs=True)
    '<li a="3" b="4" style="1:2" x>1.2'
    """

    def get_liveview_arg(x, liveview_arg):
        if x == THIS:
            return json.dumps(liveview_arg)
        else:
            arg = getattr(x, "liveview_arg", None)
            if arg:
                return json.dumps(arg)
            else:
                return json.dumps(x)

    def sort_attrs(attrs):
        # For testing only, subject to change.
        sort_attrs = attrs.pop("_sort_attrs", False)
        if sort_attrs:
            attrs = OrderedDict((k, attrs[k]) for k in sorted(attrs.keys()))
            if "style" in attrs and type(attrs["style"]) is dict:
                attrs["style"] = OrderedDict(
                    (k, attrs["style"][k])
                    for k in sorted(attrs["style"].keys()))

        return attrs

    attrs = sort_attrs(attrs)
    void = attrs.pop("void", False)
    sep = attrs.pop("sep", "")
    liveview_arg = attrs.pop("liveview_arg", None)

    e = into.extend

    e(("<", tag))
    for k, v in items(attrs):
        k = t(k).rstrip("_").replace("_", "-")
        if liveview and k.startswith("on") and type(v) in (list, tuple):
            assert callable(v[0]), "First arg must be a callable."
            v = "H({})".format(",".join(
                get_liveview_arg(x, liveview_arg)
                for x in [v[0].hypergen_url] + list(v[1:])))
            e((" ", k, '="', t(v), '"'))
        elif type(v) is bool:
            if v is True:
                e((" ", k))
        elif k == "style" and type(v) in (dict, OrderedDict):
            e((" ", k, '="', ";".join(
                t(k1) + ":" + t(v1) for k1, v1 in items(v)), '"'))
        else:
            e((" ", k, '="', t(v), '"'))
    if void:
        e(("/"))
    e(('>', ))

    write(*children, into=into, sep=sep)


def element_close(tag, children, into=state.html, return_=True):
    """
    >>> element_close("label", [7, 9, 13]); "".join(state.html)
    '7913</label>'
    """
    write(*children, into=into, return_=return_)
    into.extend(("</", t(tag), ">"))


def element(tag, children, into=state.html, return_=True, **attrs):
    """
    >>> element("div", [42, 21], return_=True, data_x=100, sep=".")
    >>> "".join(state.html)
    '<div data-x="100">42.21</div>'
    """
    element_open(tag, children, into=into, **attrs)
    element_close(tag, [], into=into)


def element_ret(tag, children, **attrs):
    """
    >>> element_ret("p", [2, 4], class_="ret")
    '<p class="ret">24</p>'
    """
    return element(tag, children, return_=True, **attrs)


def write(*children, **kwargs):
    """
    >>> into=[]; write("a", "<", Safe("<"), into=into, sep=","); into
    ['a,&lt;,<']
    """
    into = kwargs.pop("into")
    sep = kwargs.pop("sep", "")
    into.extend((t(sep).join((t(x) if not isinstance(x, Safe) else x)
                             for x in children if x is not None), ))


def raw(*children, **kwargs):
    """
    >>> into=[]; raw("a", "<", Safe("<"), into=into, sep=","); into
    ok
    """
    sep = kwargs.pop("sep", "")
    into = kwargs.pop("into")
    into.extend((sep.join(children), ))


### LIVEVIEW ###

THIS = "THIS_"


def flask_liveview_hypergen(func, *args, **kwargs):
    from flask import request
    return hypergen(
        func,
        *args,
        as_deltas=request.is_xhr,
        auto_id=True,
        liveview=True,
        **kwargs)


def flask_liveview_callback_route(app, path, *args, **kwargs):
    from flask import request, jsonify

    def _(f):
        @app.route(path, methods=["POST"], *args, **kwargs)
        @wraps(f)
        def __():
            with app.app_context():
                return jsonify(f(*request.get_json()))

        __.hypergen_url = path
        return __

    return _


### Misc ###


def t(s, quote=True):
    return escape(str(s), quote=quote)


class Safe(str):
    pass


def base65_counter():
    # THX: https://stackoverflow.com/a/49710563/164449
    abc = string.letters + string.digits + "-_:"
    base = len(abc)
    i = -1
    while True:
        i += 1
        num = i
        output = abc[num % base]  # rightmost digit

        while num >= base:
            num //= base  # move to next digit to the left
            output = abc[num % base] + output  # this digit

        yield output


class Bunch(dict):
    def __getattr__(self, k):
        return self[k]


### Input ###

INPUT_TYPES = dict(checkbox="c", month="i", number="i", range="f", week="i")


def input_(**attrs):
    if state.auto_id and "id_" not in attrs:
        attrs["id_"] = next(state.id_counter)
    if "id_" in attrs:
        attrs["id_"] = state.id_prefix + attrs["id_"]
    if state.liveview:
        type_ = attrs.get("type_", "text")
        liveview_arg = attrs["liveview_arg"] = [
            "H_", INPUT_TYPES.get(type_, "s"), attrs["id_"]
        ]
    element_void("input", **attrs)

    return Bunch({"liveview_arg": attrs["liveview_arg"]})


### All the elements ###


def div_open(into=state.html, return_=False, *children, **attrs):
    return element_open("div", *children, **attrs)


def div_close():
    return element_close("div")


def div(*children, **attrs):
    element = div_open(*children, **attrs)
    div_close()
    return element


@contextmanager
def div_con(*children, **attrs):
    element = element_open("div", *children, **attrs)
    yield element
    element_close("div")


def div_dec(*children, **attrs):
    element_dec(*children, **attrs)


# class div(element):
#     tag = "div"

# class p(element):
#     tag = "p"

# class h1(element):
#     tag = "h1"

# class ul(element):
#     tag = "ul"

# class li(element):
#     tag = "li"

# class code(element):
#     tag = "code"

# class pre(element):
#     tag = "pre"

# class table(element):
#     tag = "table"

# class tr(element):
#     tag = "tr"

# class th(element):
#     tag = "th"

# class td(element):
#     tag = "td"

# class a(element):
#     tag = "a"

# class label(element):
#     tag = "label"

# class html(element):
#     tag = "html"

# class head(element):
#     tag = "head"

# class body(element):
#     tag = "body"

# class script(element):
#     tag = "script"
#     attr_forces_eval = ("src", )

# class style(element):
#     tag = "style"
#     attr_forces_eval = ("href", )

# class link(element):
#     tag = "link"
#     attr_forces_eval = ("href", )

### Tests ###

if __name__ == "__main__":
    import doctest, sys, logging, re
    from doctest import DocTestFinder, DocTestRunner
    # Support print in doctests.
    L_ = logging.getLogger(":")
    logging.basicConfig(level=logging.DEBUG)
    pr = print = lambda *xs: L_.debug(" ".join(repr(x) for x in xs))

    # Make doctest think u"" and "" is the same.
    class Py23DocChecker(doctest.OutputChecker, object):
        RE = re.compile(r"(\W|^)[uU]([rR]?[\'\"])", re.UNICODE)

        def remove_u(self, want, got):
            if sys.version_info[0] < 3:
                return (re.sub(self.RE, r'\1\2', want), re.sub(
                    self.RE, r'\1\2', got))
            else:
                return want, got

        def check_output(self, want, got, optionflags):
            want, got = self.remove_u(want, got)
            return super(Py23DocChecker, self).check_output(
                want, got, optionflags)

        def output_difference(self, example, got, optionflags):
            example.want, got = self.remove_u(example.want, got)
            return super(Py23DocChecker, self).output_difference(
                example, got, optionflags)

    global master
    m = sys.modules.get('__main__')
    finder = DocTestFinder()
    runner = DocTestRunner(checker=Py23DocChecker())
    for test in finder.find(m, m.__name__):
        runner.run(test)
    runner.summarize()
    import sys
    sys.exit()

    # yapf: disable
    class Cache(object):
        def __init__(self):
            self.cache = {}

        def set(self, k, v, ttl):
            self.cache[k] = v

        def get(self, k):
            return self.cache.get(k, None)
    cache_client = Cache()

    _h = None
    _t = False
    def test_cache(a, b):
        global _h, _t
        _t = False
        with skippable(), cached(ttl=5, key=test_cache, a=a, b=b) as value:
            div(*(value.a+value.b), data_hash=value.hash)
            _h = value.hash
            _t = True

    assert hypergen(test_cache, (1, 2), (3, 4), cache_client=cache_client)\
        == '<div data-hash="{}">1234</div>'.format(_h)
    assert _t is True
    assert hypergen(test_cache, (1, 2), (3, 4), cache_client=cache_client)\
        == '<div data-hash="{}">1234</div>'.format(_h)
    assert _t is False
    assert hypergen(test_cache, (1, 2), (3, 5), cache_client=cache_client)\
        == '<div data-hash="{}">1235</div>'.format(_h)
    assert _t is True

    def test_div1():
        div("Hello, world!")
    assert hypergen(test_div1) == "<div>Hello, world!</div>"

    def test_div2(name):
        div("Hello", name, class_="its-hyper", data_x=3.14, hidden=True,
            selected=False, style={"height": 42, "display": "none"}, sep=" ",
            _sort_attrs=True)
    assert hypergen(test_div2, "hypergen!") == '<div class="its-hyper" '\
        'data-x="3.14" hidden style="display:none;height:42">'\
        'Hello hypergen!</div>'

    def test_div3():
        with div_cm("div", "cm", x=1, sep="_"):
            div_o(1, 2, y=1, sep="-")
            div_c(5, 6, sep=" ")
    assert hypergen(test_div3) == '<div x="1">div_cm<div y="1">1-25 6</div>'\
        '</div>'

    def test_div_4():
        div(x=1)
    assert hypergen(test_div_4) == ""

    def test_div_5():
        div(None, x=1)
    assert hypergen(test_div_5) == '<div x="1"></div>'


    def test_unicorn_class1(x):
        div("yo", blink="true")
        with div():
            write(1, x)
    assert hypergen(test_unicorn_class1, 2) == \
        '<div blink="true">yo</div><div>12</div>'

    @div
    def test_unicorn_class2(x):
        write(19, x)
    assert hypergen(test_unicorn_class2, 1) == '<div>191</div>'

    @div(id_=100)
    def test_unicorn_class3(x):
        write("hello", x)
    assert hypergen(test_unicorn_class3, 2) == '<div id="100">hello2</div>'

    def test_input():
        input_(value=1)
        input_(value=2, id_="custom")
        input_(value=3, type="number")
    assert hypergen(test_input, id_prefix="t9") == '<input value="1"/><input '\
        'id="t9.custom" value="2"/><input type="number" value="3"/>'
    assert hypergen(test_input, id_prefix="e", liveview=True,
                    auto_id=True) == '<input '\
        'id="e.a" value="1"/><input id="e.custom" value="2"/><input '\
        'id="e.b" type="number" value="3"/>'

    def test_liveview_events():
        def callback1(x):
            pass
        callback1.hypergen_url = "/hpg/cb1/"
        input_(value=91, onchange=(callback1, 9, [1], True, "foo"))
    assert hypergen(test_liveview_events, id_prefix="I", liveview=True,
                    auto_id=True) == \
        '<input id="I.a" onchange="H(&quot;/hpg/cb1/&quot;,9,[1],true,&quot;'\
        'foo&quot;)" value="91"/>'
