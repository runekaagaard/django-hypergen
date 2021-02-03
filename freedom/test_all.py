from django.test.client import RequestFactory
from freedom.core import _init_context, context, context_middleware, ContextMiddleware
from freedom.core import context as c, namespace as ns
from freedom._hypergen import *
from contextlib2 import ContextDecorator

d = dict

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


class User(object):
    pk = 1
    id = 1


class Request(object):
    user = User()

    def is_ajax(self):
        return False


class HttpResponse(object):
    pass


def test_context():
    context.replace(request=Request(), user=User())
    assert context.request.user.id == 1
    assert "request" in context


def test_context_cm():
    def inc(ctx):
        ctx["i"] = ctx.get("i", 0) + 1
        return ctx

    with context(inc) as ctx:
        assert ctx["i"] == 1

        with context(inc, foo=9) as ctx2:
            assert ctx2["foo"] == 9
            assert ctx2["i"] == 2
            with context(bar=42) as ctx3:
                assert ctx3["i"] == 2
                assert ctx3["bar"] == 42
            assert ctx2["i"] == 2

        assert ctx["i"] == 1
        assert "foo" not in ctx


def test_context_middleware():
    def view(request):
        with context() as ctx:
            assert ctx["user"].pk == 1
            assert ctx["request"].user.pk == 1
        return HttpResponse()

    get_response = lambda request: view(request)
    context_middleware(get_response)(Request())


def test_context_middleware_old():
    middleware = ContextMiddleware()
    middleware.process_request(Request())
    assert context.request.user.pk == 1


def setup():
    import os
    DIR = os.path.realpath(os.path.dirname(__file__))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
    sys.path.append(DIR)
    import django
    django.setup()
    context.replace(request=Request(), user=User())


def render_hypergen(func):
    return hypergen(func).content


def raw(*children):
    return "".join(children)


class base_element(ContextDecorator):
    js_cb = "H.cbs.s"
    void = False
    auto_id = True

    def __init__(self, *children, **attrs):
        assert "hypergen" in c, "Missing global context: hypergen"
        self.children = children
        self.attrs = attrs
        self.i = len(c.hypergen.into)
        for child in children:
            if issubclass(type(child), base_element):
                c.hypergen.into[child.i] = DELETED
        c.hypergen.into.append(lambda: join_html((self.start(), self.end())))
        super(base_element, self).__init__()

    def __enter__(self):
        c.hypergen.into.append(lambda: self.start())
        c.hypergen.into[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        if not self.void:
            c.hypergen.into.append(lambda: self.end())

    def __str__(self):
        return join_html((self.start(), self.end()))

    def __unicode__(self):
        return self.__str__()

    def callback(self, args):
        func = args[0]
        assert callable(func), (
            "First callback argument must be a callable, got "
            "{}.".format(repr(func)))
        args = args[1:]

        args2 = []
        for arg in args:
            if type(arg) in NON_SCALARS:
                state.kv[id(arg)] = arg
                args2.append(
                    freedom.quote("H.e['{}'][{}]".format(
                        state.target_id, id(arg))))
            else:
                args2.append(arg)

        return "H.cb({})".format(
            freedom.dumps(
                [func.hypergen_callback_url] + list(args2),
                unquote=True,
                escape=True,
                this=self))

    def start(self):
        if self.auto_id and "id_" not in self.attrs:
            self.attrs[
                "id_"] = c.hypergen.id_prefix + next(c.hypergen.id_counter)

        into = ["<", self.tag]
        for k, v in items(self.attrs):
            if c.hypergen.liveview is True and k.startswith("on") and type(
                    v) in (list, tuple):
                into.append(raw(" ", k, '="', self.callback(v), '"'))
            else:
                k = t(k).rstrip("_").replace("_", "-")
                if type(v) is bool:
                    if v is True:
                        into.append(raw((" ", k)))
                elif k == "style" and type(v) in (dict, OrderedDict):
                    into.append(
                        raw((" ", k, '="', ";".join(
                            t(k1) + ":" + t(v1) for k1, v1 in items(v)), '"')))
                else:
                    into.append(raw(" ", k, '="', t(v), '"'))

        if self.void:
            into.append(raw(("/")))
        into.append(raw('>', ))
        into.extend(self.children)

        return join_html(into)

    def end(self):
        return "</{}>".format(self.tag)


class div(base_element):
    tag = "div"


def join_html(html):
    def fmt(html):
        for item in html:
            if issubclass(type(item), base_element):
                yield str(item)
            elif callable(item):
                yield str(item())
            else:
                yield str(item)

    return "".join(fmt(html))


def test_element():
    with context(hypergen=hypergen_context()):
        div("hello world!")
        assert str(
            join_html(c.hypergen.into)) == '<div id="A">hello world!</div>'
    with context(hypergen=hypergen_context()):
        with div("a", class_="foo"):
            div("b", x_foo=42)
        assert str(
            join_html(c.hypergen.into)
        ) == '<div class="foo" id="A">a<div x-foo="42" id="B">b</div></div>'
    with context(hypergen=hypergen_context()):

        @div("a", class_="foo")
        def f1():
            div("b", x_foo=42)

        f1()
        assert str(
            join_html(c.hypergen.into)
        ) == '<div class="foo" id="A">a<div x-foo="42" id="B">b</div></div>'
    with context(hypergen=hypergen_context()):
        div("a", div("b", x_foo=42), class_="foo")
        assert str(
            join_html(c.hypergen.into)
        ) == '<div class="foo" id="A">a<div x-foo="42" id="B">b</div></div>'


def test_live_element():
    setup()

    with context(is_test=True):

        @callback
        def my_callback():
            pass

        with context(is_test=True, hypergen=hypergen_context()):
            div("hello world!", onclick=(my_callback, 42))
            assert str(
                join_html(c.hypergen.into)
            ) == '<div id="A" onclick="H.cb(&quot;/path/to/my_callback/&quot;,42)">hello world!</div>'
