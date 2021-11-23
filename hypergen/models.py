from django.db import models as m

class KV(m.Model):
    key = m.CharField(max_length=120, unique=True)
    value = m.TextField()

    class Meta:
        permissions = [('kv_hypergen_translations', 'Can edit translations')]
