# coding=utf-8
import re

from contextlib2 import ContextDecorator
from django.test.client import RequestFactory

from freedom.core import _init_context, context, context_middleware, ContextMiddleware
from freedom.core import context as c, namespace as ns
from freedom.hypergen import *

d = dict

### Python 2+3 compatibility ###
if sys.version_info.major > 2:
    from html import escape
    from html.parser import HTMLParser
    letters = string.ascii_letters

    def items(x):
        return x.items()

else:
    from cgi import escape
    from HTMLParser import HTMLParser

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


def e(s):
    h = HTMLParser()
    return h.unescape(s)


def test_element():
    with context(hypergen=hypergen_context()):
        div("hello world!")
        assert str(join_html(c.hypergen.into)) == '<div>hello world!</div>'
    with context(hypergen=hypergen_context()):
        with div("a", class_="foo"):
            div("b", x_foo=42)
        print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", c.hypergen.into
        print str(join_html(c.hypergen.into))
        assert str(join_html(c.hypergen.into)
                   ) == '<div class="foo">a<div x-foo="42">b</div></div>'
    with context(hypergen=hypergen_context()):

        @div("a", class_="foo")
        def f1():
            div("b", x_foo=42)

        f1()
        assert str(join_html(c.hypergen.into)
                   ) == '<div class="foo">a<div x-foo="42">b</div></div>'
    with context(hypergen=hypergen_context()):
        div("a", div("b", x_foo=42), class_="foo")
        assert str(join_html(c.hypergen.into)
                   ) == '<div class="foo">a<div x-foo="42">b</div></div>'

    with context(hypergen=hypergen_context()):
        div([1, 2], sep="-")
        # div([1, 2], (x for x in range(3, 4)), style={1: 2})
        assert str(join_html(c.hypergen.into)) == '<div>1-2</div>'


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

        with context(is_test=True, hypergen=hypergen_context()):
            div("hello world!", onclick=(my_callback, [42]))
            assert re.match(
                """<div id="A" onclick="H.cb\(&quot;/path/to/my_callback/&quot;,H.e\['__main__'\]\[[0-9]+\]\)">hello world!</div>""",
                join_html(c.hypergen.into))

        with context(is_test=True, hypergen=hypergen_context()):
            print "BEGIN"
            a = input_(name="a")
            input_(name="b", onclick=(my_callback, a))
            print 9999999999999999999999, join_html(c.hypergen.into)
            print 9999999999999999999999, e(join_html(c.hypergen.into))
            assert e(
                join_html(c.hypergen.into)
            ) == """<input id="B" name="a"/><input id="A" name="b" onclick="H.cb("/path/to/my_callback/",["_","element_value",{"cb_name":"s","id":"B"}])"/>"""

        with context(is_test=True, hypergen=hypergen_context()):
            el = textarea.r(
                placeholder=
                u"Skriv dit spørgsmål her og du vil få svar hurtigst muligt af en rådgiver."
            )
            with div.c(class_="message"):
                with div.c(class_="action-left"):
                    span(u"Annullér", class_="clickable")
                with div.c(class_="action-right"):
                    span(
                        u"Send", class_="clickable", onclick=(my_callback, el))
                div(el, class_="form form-write")

            print e(join_html(c.hypergen.into))
            assert 0 > 1
