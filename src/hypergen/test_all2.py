d = dict
from hypergen.imports import *

import re, sys
from datetime import date, datetime

from contextlib import ContextDecorator
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
        newline='\r\n',
        indent_text=True,
    )

def mock_hypergen_callback(f):
    f.reverse = lambda *a, **k: "/path/to/cb/"
    return f

def test_plugins():
    setup()
    html0 = hypergen(template, 2, hypergen_plugins=[TemplatePlugin(), LiveviewPlugin()])
    html = indent_html(html0)
    print(html0)
    print(html)
    print("-------------------------")

    html0 = hypergen(template2, 2, hypergen_plugins=[TemplatePlugin(), LiveviewPlugin()])
    html2 = indent_html(html0)
    print(html0)
    print(html2)

    assert html2 == html

    assert html == 0

def template(n):
    with html():
        with head():
            title(2)
        with body():
            h1("4")

def template2(n):
    html(head(title(2)), body(h1("4")))
