from django.db import models as m
from l1ve.models import AddedUpdatedMixin, OwnerMixin, TreeVersioningMixin


class Tag(AddedUpdatedMixin):
    text = m.CharField(max_length=25)


class Group(AddedUpdatedMixin):
    text = m.CharField(max_length=25)


class Category(AddedUpdatedMixin):
    text = m.CharField(max_length=25)
    group = m.ForeignKey(Group, on_delete=m.CASCADE)


class Item(AddedUpdatedMixin, OwnerMixin, TreeVersioningMixin):
    is_done = m.BooleanField(default=False)
    text = m.TextField()
    category = m.ForeignKey(Category, on_delete=m.PROTECT)
    tags = m.ManyToManyField(Tag)
    version_main = m.PositiveIntegerField(
        "Version number for the 'all' versioning tree.",
        default=1,
        db_index=True)

    class L1veMeta:
        versioning_trees = {
            "all": ("__self__", "tags", "category", "category__group")
        }


"""
CREATE TRIGGER todo__item__versioning_tree__all_0 UPDATE ON todo_item 
  BEGIN
    UPDATE todo_item SET version_main = old.version_main + 1 WHERE id = new.id;
  END;
"""
