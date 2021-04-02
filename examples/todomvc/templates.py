# coding=utf-8

from django.templatetags.static import static
from freedom.hypergen import *
from freedom.hypergen import callback as cb
from contextlib import contextmanager

@contextmanager
def base():
    with html(lang="en"):
        with head():
            meta(charset="utf-8")
            meta(name="viewport", content="width=device-width, initial-scale=1")
            title("Hypergen • TodoMVC")
            script(src=static("freedom/hypergen.min.js"))
            link(static("todomvc.css"))
        with body():
            with div(id_="content"):
                yield
            with footer(class_="info"):
                p("Double-click to edit a todo")
                with p():
                    a("Sindre Sorhus", href="http://sindresorhus.com")
                with p():
                    a("Django Freedom", href="https://github.com/runekaagaard/django-freedom")
                with p():
                    a("TodoMVC", href="http://todomvc.com")

def todo_item(item):
    from todomvc.views import toggle_is_completed, delete
    with li(class_="completed" if item.is_completed else ""):
        with div(class_="view"):
            input_(class_="toggle", type_="checkbox", checked=item.is_completed,
                onclick=cb(toggle_is_completed, item.pk))
            label(item.description)
            button(class_="destroy", onclick=cb(delete, item.pk))
        input_(class_="edit", value=item.description)

def content(items, filtering):
    from todomvc.views import ALL, ACTIVE, COMPLETED, index, add
    with section(class_="todoapp"):
        with header(class_="header"):
            h1("todos")
            input_(id_="new-todo", class_="new-todo", placeholder="What needs to be done?", autofocus=True,
                onkeyup=cb(add, THIS, event_matches={"key": "Enter"}))
        with section(class_="main"):
            input_(id_="toggle-all", class_="toggle-all", type_="checkbox")
            label("Mark all as complete", for_="toggle-all")

            with ul(class_="todo-list"):
                for item in items:
                    todo_item(item)

        with footer(class_="footer"):
            with span(class_="todo-count"):
                strong("0")
            with ul(class_="filters"):
                with li():
                    a("All", class_="selected" if filtering == ALL else "", href=index.reverse(ALL))
                with li():
                    a("Active", class_="selected" if filtering == ACTIVE else "", href=index.reverse(ACTIVE))
                with li():
                    a("Completed", class_="selected" if filtering == COMPLETED else "", href=index.reverse(COMPLETED))
            button("Clear completed", class_="clear-completed")
