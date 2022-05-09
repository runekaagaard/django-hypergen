from django.conf import settings

if getattr(settings, "HYPERGEN_ENABLE_INCUBATION", False) is True:
    from django.contrib import admin
    from hypergen.models import KV

    class KVAdmin(admin.ModelAdmin):
        list_display = ("key", "value", "id")

    admin.site.register(KV, KVAdmin)
