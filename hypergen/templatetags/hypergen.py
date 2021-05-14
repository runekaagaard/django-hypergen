# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)

from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static

from hypergen.core import callback as cb, context as c, dumps, command, div

d = dict

register = template.Library()

@register.simple_tag
def callback(id_, event_name, url_or_view, *cb_args, **kwargs):
    # Fake element to use with the callback func.
    el = div(id_=id_)
    return mark_safe("".join(cb(url_or_view, *cb_args, **kwargs)(el, event_name, None)))

@register.filter
def element(id_, js_coerce_func=None):
    return ["_", "element_value", ["hypergen.read.value", js_coerce_func, id_]]

@register.filter
def coerce_float(data):
    data[2][1] = "hypergen.coerce.float"
    return data

@register.filter
def coerce_int(data):
    data[2][1] = "hypergen.coerce.int"
    return data

@register.simple_tag
def hypergen_footer():
    if c.hypergen.event_handler_callbacks:
        command("hypergen.setClientState", 'hypergen.eventHandlerCallbacks', c.hypergen.event_handler_callbacks)
    return mark_safe("""
        <script src="{}"></script>
        <script>ready(() => window.applyCommands(JSON.parse('{}', reviver)))</script>
    """.format(static("hypergen/hypergen.min.js"), dumps(c.hypergen.commands)))
