# coding=utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *

from django.contrib import admin
from hypergen.models import KV

class KVAdmin(admin.ModelAdmin):
    list_display = ("key", "value", "id")

admin.site.register(KV, KVAdmin)
