from hypergen.imports import *
from hypergen.liveview import callback as cb

d = dict

from django import template
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from django.templatetags.static import static

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
    if context.hypergen.event_handler_callbacks:
        command("hypergen.setClientState", 'hypergen.eventHandlerCallbacks', context.hypergen.event_handler_callbacks)
    return mark_safe("""
        <script src="{}"></script>
        <script>hypergen.ready(() => hypergen.applyCommands(JSON.parse('{}', hypergen.reviver)))</script>
    """.format(static("hypergen/v2/hypergen.min.js"), dumps(context.hypergen.commands)))
