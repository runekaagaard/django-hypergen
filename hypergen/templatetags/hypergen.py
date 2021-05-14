# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)

from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static

from hypergen.core import django_templates_callback, context as c, dumps, command

d = dict

register = template.Library()

@register.simple_tag
def callback(url_or_view, *cb_args, **config):
    return django_templates_callback(url_or_view, *cb_args, **config)

@register.filter
def element(id_, js_coerce_func=None):
    return ["_", "element_value", ["hypergen.read.value", js_coerce_func, id_]]

@register.simple_tag
def hypergen_footer():
    if c.hypergen.event_handler_callbacks:
        command("hypergen.setClientState", 'hypergen.eventHandlerCallbacks', c.hypergen.event_handler_callbacks)
    return mark_safe("""
        <script src="{}"></script>
        <script>ready(() => window.applyCommands(JSON.parse('{}', reviver)))</script>
    """.format(static("hypergen/hypergen.min.js"), dumps(c.hypergen.commands)))
