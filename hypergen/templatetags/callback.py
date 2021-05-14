# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)
from django import template
from hypergen.core import django_templates_callback

d = dict

register = template.Library()

@register.simple_tag
def callback(url_or_view, *cb_args, **config):
    return django_templates_callback(url_or_view, *cb_args, **config)
