from django.db import models as m
from django.conf import settings

if getattr(settings, "HYPERGEN_ENABLE_INCUBATION", False) is True:

    class KV(m.Model):
        key = m.CharField(max_length=120, unique=True)
        value = m.TextField()

        class Meta:
            permissions = [('kv_hypergen_translations', 'Can edit translations')]

        def save(self, *args, **kwargs):
            super(KV, self).save(*args, **kwargs)
            from hypergen.core import set_translations
            set_translations(self)
