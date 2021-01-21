from django.db import models as m
from l1ve import global_context

relations = dict(related_name="+", related_query_name="+")


class AddedUpdatedMixin(m.Model):
    added = m.DateTimeField(auto_now_add=True)
    updated = m.DateTimeField(auto_now=True)
    added_by = m.ForeignKey(
        "auth.User", on_delete=m.CASCADE, editable=False, **relations)
    updated_by = m.ForeignKey(
        "auth.User", on_delete=m.CASCADE, editable=False, **relations)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        print("SAVING 1")
        if self.pk is None:
            self.added_by = global_context.user
        self.updated_by = global_context.user

        return super().save(*args, **kwargs)


class OwnerMixin(m.Model):
    owner = m.ForeignKey("auth.User", on_delete=m.CASCADE, **relations)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        print("SAVING 2")
        assert global_context.user.is_authenticated
        if self.pk is None:
            self.owner = global_context.user

        return super().save(*args, **kwargs)

    @classmethod
    def objects_own(cls):
        return cls.objects.filter(owner=global_context.user)


class TreeVersioningMixin(object):
    pass
