from django.contrib import admin
from hypergen.models import KV

class KVAdmin(admin.ModelAdmin):
    list_display = ("key", "value", "id")

admin.site.register(KV, KVAdmin)
