# coding = utf-8
# pylint: disable=no-value-for-parameter

from freedom.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED
from freedom.core import context as c

from todomvc import templates
from todomvc.models import Item

ALL, ACTIVE, COMPLETED = "", "active", "completed"

def appstate_init():
    return {
        "selected": set(),}

def get_items(filtering):
    items = Item.objects.all()
    if filtering == ACTIVE:
        items = items.filter(is_completed=False)
    elif filtering == COMPLETED:
        items = items.filter(is_completed=True)

    return items

@hypergen_view(url=r'^(active|completed|)$', perm=NO_PERM_REQUIRED, base_template=templates.base, target_id="content",
    namespace="todomvc", app_name="todomvc", appstate_init=appstate_init)
def index(request, filtering):
    templates.content(get_items(filtering), filtering)

@hypergen_callback(perm=NO_PERM_REQUIRED, base_template=templates.base, target_id="content", namespace="todomvc",
    app_name="todomvc", appstate_init=appstate_init)
def add(request, description):
    filtering = c.referer_resolver_match[0]
    description = description.strip()
    if not description:
        return [["alert", "Please write something to do"]]

    Item(description=description).save()
    templates.content(get_items(ALL), filtering)

@hypergen_callback(perm=NO_PERM_REQUIRED, base_template=templates.base, target_id="content", namespace="todomvc",
    app_name="todomvc", appstate_init=appstate_init)
def complete(request, pk):
    filtering = c.referer_resolver_match[0]
    Item.objects.filter(pk=pk).update(is_completed=True)

    templates.content(get_items(ALL), filtering)

@hypergen_callback(perm=NO_PERM_REQUIRED, base_template=templates.base, target_id="content", namespace="todomvc",
    app_name="todomvc", appstate_init=appstate_init)
def delete(request, pk):
    filtering = c.referer_resolver_match[0]
    Item.objects.filter(pk=pk).delete()

    templates.content(get_items(ALL), filtering)

@hypergen_callback(perm=NO_PERM_REQUIRED, base_template=templates.base, target_id="content", namespace="todomvc",
    app_name="todomvc", appstate_init=appstate_init)
def clear_completed(request, pk):
    filtering = c.referer_resolver_match[0]
    Item.objects.filter(is_completed=True).delete()

    templates.content(get_items(ALL), filtering)

@hypergen_callback(perm=NO_PERM_REQUIRED, base_template=templates.base, target_id="content", namespace="todomvc",
    app_name="todomvc", appstate_init=appstate_init)
def toggle_one(request, pk):
    filtering = c.referer_resolver_match[0]

    c.appstate["selected"].add(pk)

    templates.content(get_items(ALL), filtering)
