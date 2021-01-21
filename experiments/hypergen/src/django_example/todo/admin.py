from django.contrib import admin
from todo.models import Item, Category, Tag, Group


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    def get_fields(self, *args, **kwargs):
        return ("is_done", "text", "category", "tags")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass
