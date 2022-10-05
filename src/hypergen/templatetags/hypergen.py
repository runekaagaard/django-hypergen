from hypergen.imports import *
from hypergen.liveview import callback as cb
from hypergen.template import button as button_

d = dict

from django import template
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from django.templatetags.static import static

register = template.Library()

def str_to_element(x):
    try:
        if not x.startswith("#"):
            return x
    except AttributeError:
        return x

    x = x[1:]

    js_coerce_func = None
    for y in [".str", ".float", ".int", ".date", ".datetime", ".month", ".week"]:
        if x.endswith(y):
            x = x.replace(y, "")
            js_coerce_func = f"hypergen.coerce{y}"
            break

    return xelement(x, js_coerce_func)

@register.simple_tag
def xcallback(id_, event_name, url_or_view, *cb_args, **kwargs):
    return mark_safe('id="{}" {}'.format(id_, callbackn(id_, event_name, url_or_view, *cb_args, **kwargs)))

@register.simple_tag
def callback(url_or_view, *cb_args, **kwargs):
    if isinstance(url_or_view, str) and ":" in url_or_view:
        url_or_view = reverse(url_or_view)
    el = div(id_="todo-id")

    return mark_safe("".join(
        cb(url_or_view, *[str_to_element(x) for x in cb_args], **kwargs)(el, "todo-event-name", None)[2:]))

@register.simple_tag
def callbackn(id_, event_name, url_or_view, *cb_args, **kwargs):
    if isinstance(url_or_view, str) and ":" in url_or_view:
        url_or_view = reverse(url_or_view)
    el = div(id_=id_)
    return mark_safe("".join(cb(url_or_view, *[str_to_element(x) for x in cb_args], **kwargs)(el, event_name, None)))

@register.filter
def xelement(id_, js_coerce_func=None):
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
def button(*children, **attrs):
    print("FOOOOOOO", children, attrs)
    return mark_safe(hypergen(lambda: button_(*children, **attrs)))

@register.simple_tag
def hypergen_footer():
    if context.hypergen.event_handler_callbacks:
        command("hypergen.setClientState", 'hypergen.eventHandlerCallbacks', context.hypergen.event_handler_callbacks)
    return mark_safe("""
        <script src="{}"></script>
        <script>hypergen.ready(() => hypergen.applyCommands(JSON.parse('{}', hypergen.reviver)))</script>
    """.format(static("hypergen/v2/hypergen.min.js"), dumps(context.hypergen.commands)))

import datetime
from django import template

class ElementNode(template.Node):
    def __init__(self, nodelist, element_type):
        self.element_type = element_type
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return "button" + self.element_type + output + "/button>"

# @register.tag(name="element")
# @register.tag(name="element")
def element(parser, token):
    print("FOOOOOOOOOOOOO", parser)
    print("1111111111111", token)
    nodelist = parser.parse(('endelement',))
    parser.delete_first_token()
    return ElementNode(nodelist, "BUUT-ON")
