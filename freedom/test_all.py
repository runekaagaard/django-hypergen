from django.test.client import RequestFactory
from freedom.core import _init_context, context, context_middleware, ContextMiddleware


class User(object):
    pk = 1
    id = 1


class Request(object):
    user = User()


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
