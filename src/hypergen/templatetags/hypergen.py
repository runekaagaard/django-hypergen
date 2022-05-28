# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)

from django.conf import settings
if getattr(settings, "HYPERGEN_ENABLE_OLD", False):
    from django import template
    from django.urls.base import reverse
    from django.utils.safestring import SafeString, mark_safe
    from django.templatetags.static import static

    from hypergen.core import callback as cb, context as c, dumps, command, div

    d = dict

    register = template.Library()

    @register.simple_tag
    def callback(id_, event_name, url_or_view, *cb_args, **kwargs):
        return mark_safe('id="{}" {}'.format(id_, callbackn(id_, event_name, url_or_view, *cb_args, **kwargs)))

    @register.simple_tag
    def callbackn(id_, event_name, url_or_view, *cb_args, **kwargs):
        if isinstance(url_or_view, str) and ":" in url_or_view:
            url_or_view = reverse(url_or_view)
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
