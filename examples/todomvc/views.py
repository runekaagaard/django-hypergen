from hypergen.imports import *
# pylint: disable=no-value-for-parameter

from todomvc import templates
from todomvc.models import Item

HYPERGEN_SETTINGS = dict(perm=NO_PERM_REQUIRED, base_template=templates.base, appstate=lambda: {"edit_item_pk": None})
ALL, ACTIVE, COMPLETED = "", "active", "completed"

@liveview(re_path=r'^(active|completed|)$', **HYPERGEN_SETTINGS)
def todomvc(request, filtering):
    items = Item.objects.all()
    if filtering == ACTIVE:
        items = items.filter(is_completed=False)
    elif filtering == COMPLETED:
        items = items.filter(is_completed=True)

    all_completed = items and not Item.objects.filter(is_completed=False)

    templates.content(items, filtering, all_completed)

@action(base_view=todomvc, **HYPERGEN_SETTINGS)
def add(request, description):
    if description is None:
        return [["alert", "Please write something to do"]]

    Item(description=description).save()

@action(base_view=todomvc, **HYPERGEN_SETTINGS)
def toggle_is_completed(request, pk):
    item = Item.objects.get(pk=pk)
    item.is_completed = not item.is_completed
    item.save()

@action(base_view=todomvc, **HYPERGEN_SETTINGS)
def delete(request, pk):
    Item.objects.filter(pk=pk).delete()

@action(base_view=todomvc, **HYPERGEN_SETTINGS)
def clear_completed(request):
    Item.objects.filter(is_completed=True).delete()

@action(base_view=todomvc, **HYPERGEN_SETTINGS)
def toggle_all(request, is_completed):
    Item.objects.update(is_completed=is_completed)

@action(base_view=todomvc, **HYPERGEN_SETTINGS)
def start_edit(request, pk):
    context.hypergen.appstate["edit_item_pk"] = pk

@action(base_view=todomvc, **HYPERGEN_SETTINGS)
def submit_edit(request, pk, description):
    item = Item.objects.get(pk=pk)
    item.description = description
    item.save()
    context.hypergen.appstate["edit_item_pk"] = None
