from django.test.client import RequestFactory
from freedom.core import _init_context, context, context_middleware, ContextMiddleware
from freedom.hypergen import *

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
    sys.path.append(DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
    import django
    django.setup()
    context.replace(request=Request(), user=User())


def render_hypergen(func):
    return hypergen(func).content


def test_element():
    def _1():
        div("foo", id_="x", class_="y")

    def _2():
        with div.c():
            div("a")

    def _3():
        with div2():
            div2("a")

    def _4():
        @div2(id_="4")
        def _():
            div("5")

        _()

    def _5():
        div2("a", div2("b"))

    assert render_hypergen(_1) == '<div id="x" class="y">foo</div>'
    assert render_hypergen(_2) == '<div id="A"><div id="B">a</div></div>'
    assert render_hypergen(_3) == '<div id="A"><div id="B">a</div></div>'
    assert render_hypergen(_4) == '<div id="4"><div id="A">5</div></div>'
    assert render_hypergen(_5) == '<div id="A">a<div id="B">b</div></div>'
