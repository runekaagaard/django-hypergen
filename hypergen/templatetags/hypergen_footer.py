# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)

from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static

from hypergen.core import context as c, dumps, command

d = dict

register = template.Library()

@register.simple_tag
def hypergen_footer():
    if c.hypergen.event_handler_callbacks:
        command("hypergen.setClientState", 'hypergen.eventHandlerCallbacks', c.hypergen.event_handler_callbacks)
    return mark_safe("""
        <script src="{}"></script>
        <script>ready(() => window.applyCommands(JSON.parse('{}', reviver)))</script>
    """.format(static("hypergen/hypergen.min.js"), dumps(c.hypergen.commands)))
