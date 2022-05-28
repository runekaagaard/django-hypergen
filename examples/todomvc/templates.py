from hypergen.imports import *
# coding=utf-8

from django.templatetags.static import static
from django.urls.base import reverse
from contextlib import contextmanager

from website.templates2 import show_sources

@contextmanager
def base():
    with html(lang="en"):
        with head():
            meta(charset="utf-8")
            meta(name="viewport", content="width=device-width, initial-scale=1")
            title("Hypergen • TodoMVC")
            link(static("todomvc.css"))
            link(href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/default.min.css")
            script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js")
            script(src=static("website/website.js"), defer=True)
        with body():
            p(a("Back to documentation", href=reverse("website:documentation")),
                style={"padding": "16px", "font-size": "150%"})
            p("Todos are shared between all users.", style={"padding": "16px", "font-size": "150%"})
            with div(id_="content"):
                yield
            with footer(class_="info"):
                p("Double-click to edit a todo")
                p(a("Django Hypergen", href="https://github.com/runekaagaard/django-hypergen"))
                p(a("TodoMVC", href="http://todomvc.com"))

        show_sources(__file__)

base.target_id = "content"

@component
def todo_item(item):
    from todomvc.views import toggle_is_completed, delete, start_edit, submit_edit
    is_editing = item.pk == context.appstate["edit_item_pk"]
    classes = []
    if item.is_completed:
        classes.append("completed")
    if is_editing:
        classes.append("editing")

    with li(class_=classes):
        if not is_editing:
            with div(class_="view"):
                input_(id_=("toggle_is_completed", item.pk), class_="toggle", type_="checkbox",
                    checked=item.is_completed, onclick=callback(toggle_is_completed, item.pk))
                label(item.description, id_=("start_edit", item.pk), ondblclick=callback(start_edit, item.pk))
                button(class_="destroy", id_=("destroy", item.pk), onclick=callback(delete, item.pk))
        else:
            input_(id_="edit-item", class_="edit", autofocus=True, value=item.description,
                onblur=callback(submit_edit, item.pk, THIS))

def content(items, filtering, all_completed):
    from todomvc.views import ALL, ACTIVE, COMPLETED, todomvc, add, clear_completed, toggle_all
    with section(class_="todoapp"):
        with header(class_="header"):
            h1("todos")
            input_(id_="new-todo", class_="new-todo", placeholder="What needs to be done?",
                autofocus=not context.appstate["edit_item_pk"],
                onkeyup=callback(add, THIS, clear=True, when=["hypergen.when.keycode", "Enter"]))

        if filtering == ALL and not items:
            return

        with section(class_="main"):
            input_(id_="toggle-all", class_="toggle-all", type_="checkbox", checked=all_completed,
                onclick=callback(toggle_all, not all_completed))
            label("Mark all as complete", for_="toggle-all")

        ul([todo_item(item) for item in items], class_="todo-list")

        with footer(class_="footer"):
            span(strong(len(items), "items" if len(items) > 1 else "item", sep=" "), class_="todo-count")

            with ul(class_="filters"):
                li(
                    a("All", class_="selected" if filtering == ALL else "", href=todomvc.reverse(ALL),
                    id_="filter-all"))
                li(
                    a("Active", class_="selected" if filtering == ACTIVE else "", href=todomvc.reverse(ACTIVE),
                    id_="filter-active"))
                li(
                    a("Completed", class_="selected" if filtering == COMPLETED else "",
                    href=todomvc.reverse(COMPLETED), id_="filter-completed"))

            if items.filter(is_completed=True):
                button("Clear completed", id_="clear-completed", class_="clear-completed",
                    onclick=callback(clear_completed))
