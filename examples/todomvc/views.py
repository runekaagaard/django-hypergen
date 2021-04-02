# coding = utf-8
# pylint: disable=no-value-for-parameter

from freedom.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED
from freedom.core import context as c

from todomvc import templates
from todomvc.models import Item

appstate_init = lambda: {
    "selected": set(),}

HYPERGEN_SETTINGS = dict(perm=NO_PERM_REQUIRED, base_template=templates.base, target_id="content",
    namespace="todomvc", app_name="todomvc", appstate_init=appstate_init)
ALL, ACTIVE, COMPLETED = "", "active", "completed"

def get_items(filtering):
    items = Item.objects.order_by("is_completed", "description").all()
    if filtering == ACTIVE:
        items = items.filter(is_completed=False)
    elif filtering == COMPLETED:
        items = items.filter(is_completed=True)

    return items

@hypergen_view(url=r'^(active|completed|)$', **HYPERGEN_SETTINGS)
def index(request, filtering):
    templates.content(get_items(filtering), filtering)

@hypergen_callback(**HYPERGEN_SETTINGS)
def add(request, description):
    filtering = c.referer_resolver_match[0]
    description = description.strip()
    if not description:
        return [["alert", "Please write something to do"]]

    Item(description=description).save()
    templates.content(get_items(ALL), filtering)

@hypergen_callback(**HYPERGEN_SETTINGS)
def toggle_is_completed(request, pk):
    filtering = c.referer_resolver_match[0]
    item = Item.objects.get(pk=pk)
    item.is_completed = not item.is_completed
    item.save()

    templates.content(get_items(ALL), filtering)

@hypergen_callback(**HYPERGEN_SETTINGS)
def delete(request, pk):
    filtering = c.referer_resolver_match[0]
    Item.objects.filter(pk=pk).delete()

    templates.content(get_items(ALL), filtering)

@hypergen_callback(**HYPERGEN_SETTINGS)
def clear_completed(request, pk):
    filtering = c.referer_resolver_match[0]
    Item.objects.filter(is_completed=True).delete()

    templates.content(get_items(ALL), filtering)
