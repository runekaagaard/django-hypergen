from django.db import models as m

class Item(m.Model):
    description = m.CharField("Description", max_length=100)
    is_completed = m.BooleanField("Is completed?", default=False)
