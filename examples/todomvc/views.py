from freedom.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED
from freedom.core import context as c

from todomvc import templates
from todomvc.models import Item

ALL, ACTIVE, COMPLETED = "", "active", "completed"

def get_items(filtering):
    items = Item.objects.all()
    if filtering == ACTIVE:
        items = items.filter(is_completed=False)
    elif filtering == COMPLETED:
        items = items.filter(is_completed=True)

    return items

@hypergen_view(url=r'^(active|completed|)$', perm=NO_PERM_REQUIRED, base_template=templates.base, target_id="content",
    namespace="todomvc")
def index(request, filtering):
    templates.content(get_items(filtering), filtering)

@hypergen_callback(perm=NO_PERM_REQUIRED, base_template=templates.base, target_id="content", namespace="todomvc")
def add(request, description):
    filtering = c.referer_resolver_match[0]
    description = description.strip()
    if not description:
        return [["alert", "Please write something to do"]]

    Item(description=description).save()
    templates.content(get_items(ALL), filtering)

@hypergen_callback(perm=NO_PERM_REQUIRED, base_template=templates.base, target_id="content", namespace="todomvc")
def complete(request, pk):
    Item.objects.filter(pk=pk).update(is_completed=True)

@hypergen_callback(perm=NO_PERM_REQUIRED, base_template=templates.base, target_id="content", namespace="todomvc")
def delete(request, pk):
    Item.objects.filter(pk=pk).delete()

@hypergen_callback(perm=NO_PERM_REQUIRED, base_template=templates.base, target_id="content", namespace="todomvc")
def clear_completed(request, pk):
    Item.objects.filter(is_completed=True).delete()
