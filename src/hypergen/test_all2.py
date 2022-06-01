d = dict
from hypergen.imports import *
from hypergen.context import contextlist

import re, sys
from datetime import date, datetime

from contextlib import ContextDecorator, contextmanager
from django.test.client import RequestFactory
from pyrsistent import pmap

import pytest
from pytest import raises

import django

class User(object):
    pk = 1
    id = 1

class Request(object):
    user = User()
    session = {}

    def is_ajax(self):
        return False

    def get_full_path(self):
        return "mock"

class HttpResponse(object):
    pass

def setup():
    import os
    DIR = os.path.realpath(os.path.dirname(__file__))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
    sys.path.append(DIR)
    import django
    django.setup()
    # context.replace(request=Request(), user=User())

def indent_html(html):
    from yattag import indent
    return indent(
        html,
        indentation='    ',
        newline='\n',
        indent_text=True,
    )

def mock_hypergen_callback(f):
    f.reverse = lambda *a, **k: "/path/to/cb/"
    return f

@contextmanager
def mock_middleware():
    with context(request=Request()):
        yield

@mock_middleware()
def test_plugins():
    setup()
    html1 = hypergen(template, 2, settings=d(plugins=[TemplatePlugin(), LiveviewPlugin()], indent=True))

    html2 = hypergen(template2, 2, settings=d(plugins=[TemplatePlugin(), LiveviewPlugin()], indent=True))

    assert html1.strip() == html2.strip() == HTML

def template(n):
    with html():
        with head():
            title(2)
        with body():
            h1("4")

def template2(n):
    html(head(title(2)), body(h1("4")))

HTML = """
<html>
    <head>
        <title>
            2
        </title>
    </head>
    <body>
        <h1>
            4
        </h1>
        <!--hypergen_liveview_media-->
        <script src="hypergen/v2/hypergen.min.js"></script>
        <script type="application/json" id="hypergen-apply-commands-data">[["hypergen.setClientState","hypergen.eventHandlerCallbacks",{}],["history.replaceState",{"callback_url":"mock"},"","mock"]]</script>
        <script>
                hypergen.ready(() => hypergen.applyCommands(JSON.parse(document.getElementById(
                    'hypergen-apply-commands-data').textContent, hypergen.reviver)))
            </script>
    </body>
</html>
""".strip()

def test_multilist():
    with context(at="hypergen"):
        into = contextlist()
        into.append(1)
        assert len(into) == 1
        assert into == [1]
    with context(at="hypergen", target_id="bar"):
        into.append(2)
        into.append(3)

    assert into.context == {'__hypergen__main__': [1], 'bar': [2, 3]}

@mock_middleware()
def test_multitargets():
    html = hypergen(multitarget_template)
    print(html)
    assert html == "<p>main</p>"

def multitarget_template():
    p("main")
    with context(at="hypergen", target_id="foo"):
        p("foo1")
    with context(at="hypergen", target_id="bar"):
        p("bar1")
