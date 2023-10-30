from hypergen.imports import *
from hypergen.liveview import callback as cb
from hypergen.template import button as button_

d = dict

from django import template
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.template.loader import render_to_string

try:
    from render_block import render_block_to_string
    render_block_ok = True
except ImportError:
    render_block_ok = False

__all__ = ["django_template"]

register = template.Library()

def django_template(f):
    def _(*args, **kwargs):
        return hypergen(f, *args, **kwargs, settings=dict(returns=FULL, liveview=True))["template_result"]

    return _

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

    return element_value(x, js_coerce_func)

@register.simple_tag
def callback(url_or_view, *cb_args, **kwargs):
    if isinstance(url_or_view, str) and ":" in url_or_view:
        url_or_view = reverse(url_or_view)
    id_ = kwargs.pop("id", None)
    assert id_, "id must be passed to the {% callback %} tag as a keyword argument."
    event = kwargs.pop("event", None)
    assert event, "event must be passed to the {% callback %} tag as a keyword argument."
    add_id = kwargs.pop("add_id", True)
    el = div(id_=id_)

    into = ([' id="', id_, '"'] if add_id else []) + cb(url_or_view, *[str_to_element(x)
        for x in cb_args], **kwargs)(el, event, None)

    return mark_safe("".join(into))

def element_value(id_, js_coerce_func=None):
    return ["_", "element_value", ["hypergen.read.value", js_coerce_func, id_]]

@register.simple_tag
def hypergen_media_header():
    return mark_safe('<script src="{}"></script>'.format(static("hypergen/dist/hypergen.js")))

@register.simple_tag
def hypergen_media_footer():
    if context.hypergen.event_handler_callbacks:
        command("hypergen.setClientState", 'hypergen.eventHandlerCallbacks', context.hypergen.event_handler_callbacks)
    return mark_safe(
        "<script>hypergen.ready(() => hypergen.applyCommands(JSON.parse('{}', hypergen.reviver)))</script>".format(
        dumps(context.hypergen.commands)))

def render_to_hypergen(template_name, context=None, request=None, using=None, block=None):
    if block is None:
        raw(render_to_string(template_name, context=context, request=request))
    else:
        assert render_block_ok, ("To use the block render functionality, "
            "you need to 'pip install django-render-block'.")
        assert using is None, "'using' is not supported for block rendering."
        raw(render_block_to_string(template_name, block, context=context, request=request))
