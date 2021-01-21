# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)

import string, sys, json, datetime
from threading import local
from contextlib import contextmanager
from collections import OrderedDict
from functools import wraps, partial
from copy import deepcopy
from types import GeneratorType

### Python 2+3 compatibility ###

if sys.version_info.major > 2:
    from html import escape
    letters = string.ascii_letters

    def items(x):
        return x.items()

else:
    from cgi import escape
    letters = string.letters
    str = unicode

    def items(x):
        return x.iteritems()


### Globals ###

state = local()
UPDATE = 1

### Control ###


def hypergen(func, *args, **kwargs):
    flask_app = kwargs.pop("flask_app", None)
    kwargs = deepcopy(kwargs)
    auto_id = kwargs.pop("auto_id", False)
    target_id = kwargs.pop("target_id", False)
    as_deltas = kwargs.pop("as_deltas", False)
    try:
        state.html = []
        state.cache_client = kwargs.pop("cache_client", None)
        state.id_counter = base65_counter() if auto_id else None
        state.id_prefix = kwargs.pop("id_prefix", "")
        state.auto_id = auto_id
        state.liveview = kwargs.pop("liveview", False)
        state.callback_output = kwargs.pop("callback_output", None)
        state.flask_app = flask_app
        func(*args, **kwargs)
        html = "".join(str(x()) if callable(x) else str(x) for x in state.html)
    finally:
        state.html = []
        state.cache_client = None
        state.id_counter = None
        state.id_prefix = ""
        state.auto_id = False
        state.liveview = False
        state.callback_output = None
        state.flask_app = None

    if as_deltas:
        return [[UPDATE, target_id, html]]
    else:
        return html


hypergen(lambda: None)


class SkipException(Exception):
    pass


@contextmanager
def skippable():
    try:
        yield
    except SkipException:
        pass


### Building HTML, internal API ###


def _element_start_1(tag, attrs, into):
    attrs = _sort_attrs(attrs)
    raw(("<", tag), into=into)
    return attrs


def _element_start_2(k, v, into):
    k = t(k).rstrip("_").replace("_", "-")
    if type(v) is bool:
        if v is True:
            raw((" ", k), into=into)
    elif k == "style" and type(v) in (dict, OrderedDict):
        raw((" ", k, '="', ";".join(
            t(k1) + ":" + t(v1) for k1, v1 in items(v)), '"'),
            into=into)
    else:
        raw((" ", k, '="', t(v), '"'), into=into)


def _element_start_3(children, into, void, sep):
    if void:
        raw(("/"), into=into)
    raw(('>', ), into=into)
    write(*children, into=into, sep=sep)


def element_start(*args, **kwargs):
    return control_element_start(*args, **kwargs)


def element_end(tag, children, into=None, sep="", void=False):
    if void is False:
        write(*children, into=into, sep=sep)
        raw(("</", t(tag), ">"), into=into)


def element(tag, children, into=None, sep="", void=False, **attrs):
    element_start(tag, children, into=into, sep=sep, void=void, **attrs)
    element_end(tag, [], into=into, void=void)


def element_ret(tag, children, sep="", void=False, **attrs):
    into = Blob()
    element(tag, children, into=into, sep=sep, void=void, **attrs)
    return into


def element_con(tag, children, into=None, sep="", void=False, **attrs):
    element = element_start(
        tag, children, into=into, sep=sep, void=void, **attrs)
    yield element
    element_end(tag, [], into=into, void=void)


def element_dec(tag, children, into=None, sep="", void=False, **attrs):
    def _(f):
        @wraps(f)
        def __(*args, **kwargs):
            element_start(
                tag, children, into=into, sep=sep, void=void, **attrs)
            f(*args, **kwargs)
            element_end(tag, [], into=into, void=void)

        return __

    return _


### Building HTML, public API ###


def _write(_t, children, **kwargs):
    into = kwargs.get("into", None)
    if into is None:
        into = state.html
    sep = _t(kwargs.get("sep", ""))

    for x in children:
        if x is None:
            continue
        elif type(x) is Blob:
            into.extend(x)
        elif type(x) in (list, tuple, GeneratorType):
            _write(_t, list(x), into=into, sep=sep)
        elif callable(x):
            into.append(x)
        else:
            into.append(_t(x))
        if sep:
            into.append(sep)
    if sep and children:
        into.pop()


def write(*children, **kwargs):
    _write(t, children, **kwargs)


def raw(*children, **kwargs):
    _write(lambda x: x, children, **kwargs)


### Flask helpers ###


def flask_liveview_hypergen(func, *args, **kwargs):
    from flask import request
    return hypergen(
        func,
        *args,
        as_deltas=request.is_xhr,
        auto_id=True,
        id_prefix=request.get_json()["id_prefix"] if request.is_xhr else "",
        liveview=True,
        **kwargs)


def flask_liveview_callback_route(app, path, *args, **kwargs):
    from flask import request, jsonify

    def _(f):
        @app.route(path, methods=["POST"], *args, **kwargs)
        @wraps(f)
        def __():
            with app.app_context():
                data = f(*request.get_json()["args"])
                if data is None and __.callback_output is not None:
                    data = __.callback_output()
                return jsonify(data)

        __.hypergen_callback_url = path
        return __

    return _


def flask_liveview_autoroute_callbacks(app, prefix, *args, **kwargs):
    from flask import request, jsonify
    setattr(app, "hypergen_autoroutes", {"prefix": prefix, "routes": {}})
    route = "{}<func_name>/".format(prefix)

    @app.route(route, methods=["POST", "GET"], *args, **kwargs)
    def router(func_name):
        func = app.hypergen_autoroutes["routes"][func_name]
        with app.app_context():
            data = func(*request.get_json()["args"])
            if data is None and func.callback_output is not None:
                data = func.callback_output()

            return jsonify(data)


### Misc ###


def _sort_attrs(attrs):
    # For testing only, subject to change.
    if attrs.pop("_sort_attrs", False):
        attrs = OrderedDict((k, attrs[k]) for k in sorted(attrs.keys()))
        if "style" in attrs and type(attrs["style"]) is dict:
            attrs["style"] = OrderedDict(
                (k, attrs["style"][k]) for k in sorted(attrs["style"].keys()))

    return attrs


def t(s, quote=True):
    return escape(str(s), quote=quote)


class Blob(object):
    def __init__(self, html=None, meta=None):
        self.html = html if html is not None else []
        self.meta = meta

    def append(self, x):
        return self.html.append(x)

    def extend(self, x):
        return self.html.extend(x)

    def pop(self, n=-1):
        return self.html.pop(n)

    def __getitem__(self, index):
        return self.html[index]


def base65_counter():
    # THX: https://stackoverflow.com/a/49710563/164449
    abc = letters + string.digits + "-_:"
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


### Form elements and liveview ###


class THIS(object):
    pass


def encoder(this, o):
    if o is THIS:
        return encoder.quote(this)
    elif type(o) is Blob:
        return encoder.quote(o.meta["this"])
    elif isinstance(o, datetime.datetime):
        assert False, "TODO"
        return str(o)
    else:
        raise TypeError(repr(o) + " is not JSON serializable")


encoder.quote = lambda x: "H_" + x + "_H"
encoder.unquote = lambda x: x.replace('"H_', "").replace('_H"', "")[1:-1]


def func_to_string(func):
    return ".".join((func.__module__, func.__name__))


def _callback(args, this, debounce=0):
    func = args[0]
    assert callable(func), ("First callback argument must be a callable, got "
                            "{}.".format(repr(func)))
    args = args[1:]
    if state.callback_output is not None:
        func.callback_output = state.callback_output

    if state.flask_app is not None and hasattr(state.flask_app,
                                               "hypergen_autoroutes"):
        state.flask_app.hypergen_autoroutes["routes"][func_to_string(
            func)] = func
        func.hypergen_callback_url = "{}{}/".format(
            state.flask_app.hypergen_autoroutes["prefix"],
            func_to_string(func))

    return "H.cb({})".format(
        t(
            encoder.unquote(
                json.dumps(
                    [func.hypergen_callback_url] + list(args),
                    default=partial(encoder, this),
                    separators=(',', ':')))))


def control_element_start(tag,
                          children,
                          lazy=False,
                          into=None,
                          void=False,
                          sep="",
                          add_to=None,
                          js_cb="s",
                          **attrs):
    assert "add_to" not in attrs
    if state.auto_id and "id_" not in attrs:
        attrs["id_"] = next(state.id_counter)
    if "id_" in attrs:
        attrs["id_"] = state.id_prefix + attrs["id_"]
    attrs = _element_start_1(tag, attrs, into)

    meta = {}
    if state.liveview is True:
        meta["this"] = "H.cbs.{}('{}')".format(js_cb, attrs["id_"])
    if into is not None:
        into.meta = meta

    for k, v in items(attrs):
        if state.liveview is True and k.startswith("on") and type(v) in (
                list, tuple):
            tmp1 = v
            tmp2 = lambda: _callback(tmp1, meta["this"])
            raw(" ", k, '="', into=into)
            raw(tmp2 if lazy else tmp2(), into=into)
            raw('"', into=into)
        else:
            _element_start_2(k, v, into)

    _element_start_3(children, into, void, sep)

    blob = Blob(into, meta)
    if add_to is not None:
        add_to.append(blob)
    return blob


def control_element(tag,
                    children,
                    lazy=False,
                    into=None,
                    void=False,
                    sep="",
                    add_to=None,
                    **attrs):
    blob = control_element_start(
        tag,
        children,
        lazy=lazy,
        into=into,
        void=void,
        sep="",
        add_to=add_to,
        **attrs)
    element_end(tag, [], into=into, void=void)
    return blob


def control_element_ret(tag,
                        children,
                        lazy=False,
                        into=None,
                        void=False,
                        sep="",
                        add_to=None,
                        **attrs):
    into = Blob()
    control_element_start(
        tag,
        children,
        lazy=lazy,
        into=into,
        void=void,
        sep="",
        add_to=add_to,
        **attrs)
    return into


### Input ###

INPUT_TYPES = dict(checkbox="c", month="i", number="i", range="f", week="i")


def input_(**attrs):
    return control_element(
        "input", [],
        void=True,
        js_cb=INPUT_TYPES.get(attrs.get("type_", "text"), "s"),
        **attrs)


def input_ret(**attrs):
    return control_element_ret("input", [], **attrs)


input_.r = input_ret

### Select ###


def _js_cb_select(attrs):
    type_ = attrs.pop("js_cb", None)
    if type_ is str:
        attrs["js_cb"] = "s"
    elif type_ is int:
        attrs["js_cb"] = "i"
    elif type_ is float:
        attrs["js_cb"] = "f"
    elif type_ is None:
        attrs["js_cb"] = "g"
    else:
        raise Exception(
            "Bad coercion, {}. Only str, unicode, int and float are"
            " supported")


def select_sta(*children, **attrs):
    _js_cb_select(attrs)
    return control_element_start("select", children, **attrs)


def select_end(*children, **kwargs):
    return element_end("select", children, **kwargs)


def select_ret(*children, **attrs):
    _js_cb_select(attrs)
    return control_element_ret("select", children, **attrs)


@contextmanager
def select_con(*children, **attrs):
    _js_cb_select(attrs)
    for x in control_element_con("select", children, **attrs):
        yield x


def select_dec(*children, **attrs):
    _js_cb_select(attrs)
    return control_element_dec("select", children, **attrs)


def select(*children, **attrs):
    _js_cb_select(attrs)
    return control_element("select", children, **attrs)


select.s = select_sta
select.e = select_end
select.r = select_ret
select.c = select_con
select.d = select_dec

### Special tags ###


def doctype(type_="html"):
    raw("<!DOCTYPE ", type_, ">")


### TEMPLATE-ELEMENT ###
def div_sta(*children, **attrs):
    return element_start("div", children, **attrs)


def div_end(*children, **kwargs):
    return element_end("div", children, **kwargs)


def div_ret(*children, **kwargs):
    return element_ret("div", children, **kwargs)


@contextmanager
def div_con(*children, **attrs):
    for x in element_con("div", children, **attrs):
        yield x


def div_dec(*children, **attrs):
    return element_dec("div", children, **attrs)


def div(*children, **attrs):
    return element("div", children, **attrs)


div.s = div_sta
div.e = div_end
div.r = div_ret
div.c = div_con
div.d = div_dec


### TEMPLATE-ELEMENT ###
### TEMPLATE-VOID-ELEMENT ###
def link(*children, **attrs):
    return element("link", children, void=True, **attrs)


def link_ret(*children, **attrs):
    return element_ret("link", children, void=True, **attrs)


link.r = link_ret

### TEMPLATE-VOID-ELEMENT ###

### RENDERED-ELEMENTS ###

### RENDERED-VOID-ELEMENTS ###

### Tests ###

if __name__ == "__main__":

    def test_div1():
        div("Hello, world!")

    assert hypergen(test_div1) == "<div>Hello, world!</div>"

    def test_div2(name):
        div("Hello",
            name,
            class_="its-hyper",
            data_x=3.14,
            hidden=True,
            selected=False,
            style={"height": 42,
                   "display": "none"},
            sep=" ",
            _sort_attrs=True)

    assert hypergen(test_div2, "hypergen!") == '<div class="its-hyper" '\
        'data-x="3.14" hidden style="display:none;height:42">'\
        'Hello hypergen!</div>'

    def test_div3():
        with div.c("div", "c", x=1, sep="."):
            div.s(1, 2, y=1, sep="-")
            div.e(5, 6, sep=" ")

    assert hypergen(test_div3) == '<div x="1">div.c<div y="1">1-25 6</div>'\
        '</div>'

    def test_div_5():
        div(None, x=1)

    assert hypergen(test_div_5) == '<div x="1"></div>'

    def test_context_manager(x):
        div("yo", blink="true")
        with div.c():
            div("12")

    assert hypergen(test_context_manager, 2) == \
        '<div blink="true">yo</div><div><div>12</div></div>'

    @div.d(1, class_="f")
    def test_decorator(x):
        div(2, 3, y=4)

    assert hypergen(test_decorator,
                    1) == '<div class="f">1<div y="4">23</div></div>'

    def test_input():
        input_(value=1, _sort_attrs=True)
        input_(value=2, id_="custom", _sort_attrs=True)
        input_(value=3, type="number", _sort_attrs=True)

    assert hypergen(test_input, id_prefix="t9.") == '<input value="1"/><input '\
        'id="t9.custom" value="2"/><input type="number" value="3"/>'

    assert hypergen(test_input, id_prefix="e.", liveview=True,
                    auto_id=True) == '<input '\
        'id="e.a" value="1"/><input id="e.custom" value="2"/><input '\
        'id="e.b" type="number" value="3"/>'

    def test_liveview_events():
        def callback1(x):
            pass

        callback1.hypergen_callback_url = "/hpg/cb1/"
        input_(
            value=91,
            onchange=(callback1, 9, [1], True, "foo"),
            _sort_attrs=True)

    assert hypergen(test_liveview_events, id_prefix="I.", liveview=True,
                    auto_id=True) == \
        '<input id="I.a" onchange="H.cb(&quot;/hpg/cb1/&quot;,9,[1],true,&quot;'\
        'foo&quot;)" value="91"/>'

    def test_collections_as_children():
        div((div.r(x) for x in [3]), [1], (2, ))

    assert hypergen(
        test_collections_as_children) == '<div><div>3</div>12</div>'
