# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)
import re

from contextlib2 import ContextDecorator
from django.test.client import RequestFactory

from freedom.core import _init_context, context, context_middleware, ContextMiddleware
from freedom.core import context as c
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
        return ctx.set("i", ctx.get("i", 0) + 1)

    with context(inc):
        assert context["i"] == 1

        with context(inc, foo=9):
            assert context["foo"] == 9
            assert context["i"] == 2
            with context(bar=42):
                assert context["i"] == 2
                assert context["bar"] == 42
            assert context["i"] == 2

        assert context["i"] == 1
        assert "foo" not in context


def test_context_middleware():
    def view(request):
        assert context.user.pk == 1
        assert context["request"].user.pk == 1
        return HttpResponse()

    get_response = lambda request: view(request)
    context_middleware(get_response)(Request())


def test_context_middleware_old():
    middleware = ContextMiddleware()
    middleware.process_request(Request())
    assert context.request.user.pk == 1


def test_hypergen_context():
    def transform(ctx):
        return ctx.set("hypergen", ctx["hypergen"].set("liveview", False))

    def transform2(hpg):
        return hpg.set("liveview", 900)

    with context(hypergen=hypergen_context()):
        assert context["hypergen"]["liveview"] is True
        with context(transform):
            assert context["hypergen"]["liveview"] is False
            with context(transform2, at="hypergen"):
                assert context["hypergen"]["liveview"] == 900
            assert context["hypergen"]["liveview"] is False

        assert context["hypergen"]["liveview"] is True
        assert context.hypergen.liveview is True


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


def f():
    return re.sub(r'[0-9]{5,}', '1234', join_html(c.hypergen.into))


def test_element():
    with context(hypergen=hypergen_context()):
        div("hello world!")
        assert str(join_html(c.hypergen.into)) == '<div>hello world!</div>'
    with context(hypergen=hypergen_context()):
        with div("a", class_="foo"):
            div("b", x_foo=42)
        assert f() == '<div class="foo">a<div x-foo="42">b</div></div>'
    with context(hypergen=hypergen_context()):

        @div("a", class_="foo")
        def f1():
            div("b", x_foo=42)

        f1()
        assert f() == '<div class="foo">a<div x-foo="42">b</div></div>'
    with context(hypergen=hypergen_context()):
        div("a", None, div("b", x_foo=42), class_="foo")
        assert f() == '<div class="foo">a<div x-foo="42">b</div></div>'

    with context(hypergen=hypergen_context()):
        div(None, [1, 2], sep="-")
        assert f() == '<div>1-2</div>'

    with context(hypergen=hypergen_context()):
        ul([li([li(y) for y in range(3, 4)]) for x in range(1, 2)])
        assert f() == "<ul><li><li>3</li></li></ul>"

    with context(hypergen=hypergen_context()):
        ul(li(li(y) for y in range(3, 4)) for x in range(1, 2))
        assert f() == "<ul><li><li>3</li></li></ul>"

    with context(hypergen=hypergen_context()):
        div([1, 2],
            div(1, 2, div(1, None, 2, ul(list(li(x) for x in range(1, 3))))))
        assert f(
        ) == '<div>12<div>12<div>12<ul><li>1</li><li>2</li></ul></div></div></div>'
    with context(hypergen=hypergen_context()):
        ul(None, [
            li(None, (li(li(z) for z in range(1, 2))
                      for y in range(3, 4)), None) for x in range(5, 6)
        ], None)
        assert f() == "<ul><li><li><li>1</li></li></li></ul>"


def test_live_element():
    setup()

    with context(is_test=True):

        @callback
        def my_callback():
            pass

        with context(is_test=True, hypergen=hypergen_context()):
            div("hello world!", onclick=(my_callback, 42))
            assert f(
            ) == """<div id="A" onclick="e('__main__',1234)">hello world!</div>"""

        with context(is_test=True, hypergen=hypergen_context()):
            div("hello world!", onclick=(my_callback, [42]))
            assert f(
            ) == """<div id="A" onclick="e('__main__',1234)">hello world!</div>"""

        with context(is_test=True, hypergen=hypergen_context()):
            a = input_(name="a")
            input_(name="b", onclick=(my_callback, a))
            assert f(
            ) == """<input name="a"/><input id="A" name="b" onclick="e('__main__',1234)"/>"""

        with context(is_test=True, hypergen=hypergen_context()):
            el = textarea(placeholder=u"myplace")
            with div(class_="message"):
                with div(class_="action-left"):
                    span(u"Annullér", class_="clickable")
                with div(class_="action-right"):
                    span(
                        u"Send", class_="clickable", onclick=(my_callback, el))
                div(el, class_="form form-write")

            assert f(
            ) == """<div class="message"><div class="action-left"><span class="clickable">Annull\xe9r</span></div><div class="action-right"><span class="clickable" onclick="e('__main__',1234)" id="A">Send</span></div><div class="form form-write"><textarea placeholder="myplace"></textarea></div></div>"""

        with context(is_test=True, hypergen=hypergen_context()):
            input_(autofocus=True)
            assert join_html(c.hypergen.into) == '<input autofocus/>'


def test_live_element2():
    setup()

    with context(is_test=True):

        @callback
        def my_callback():
            pass

        with context(is_test=True, hypergen=hypergen_context()):
            el1 = input_(
                id_="id_new_password",
                placeholder="Adgangskode",
                oninput=(my_callback, THIS, ""))
            el2 = input_(
                placeholder="Gentag Adgangskode",
                oninput=(my_callback, THIS, el1))

            h2(u"Skift Adgangskode")
            p(u"Rules:")
            with div(class_="form"):
                with div():
                    with ul(id_="password_verification_smartassness"):
                        div("TODO")
                    with div(class_="form"):
                        div(el1, class_="form-field")
                        div(el2, class_="form-field")
                        div(u"Skift adgangskode", class_="button disabled")

            assert f(
            ) == """<h2>Skift Adgangskode</h2><p>Rules:</p><div class="form"><div><ul id="password_verification_smartassness"><div>TODO</div></ul><div class="form"><div class="form-field"><input id="id_new_password" oninput="e('__main__',1234)" placeholder="Adgangskode"/></div><div class="form-field"><input id="A" oninput="e('__main__',1234)" placeholder="Gentag Adgangskode"/></div><div class="button disabled">Skift adgangskode</div></div></div></div>"""


def test_callback():
    setup()
    with context(is_test=True, hypergen=hypergen_context()):

        @callback
        def cb(foo, punk=300):
            pass

        element = input_(oninput=cb(THIS, punk=200, debounce=500))
        assert type(cb("foo", bar=42, debounce=42)(element, "oninput")) is int


def test_components():
    def f1():
        div("a")

    @component
    def f2():
        div("a")

    with context(is_test=True, hypergen=hypergen_context()):
        div(1, f1(), 2)
        assert f() == "<div>a</div><div>12</div>"

    with context(is_test=True, hypergen=hypergen_context()):
        div(1, f2(), 2)
        assert f() == "<div>1<div>a</div>2</div>"


def test_components2():
    @component
    def comp1():
        @component
        def comp2():
            input_(value="a")

        comp2()

    with context(is_test=True, hypergen=hypergen_context()):

        with tr():
            td(comp1())
        assert f() == '<tr><td><input value="a"/></td></tr>'

    with context(is_test=True, hypergen=hypergen_context()):
        with tr():
            with td():
                comp1()
        assert f() == '<tr><td><input value="a"/></td></tr>'
