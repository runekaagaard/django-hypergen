# coding=utf-8

from django.templatetags.static import static
from freedom.hypergen import *
from contextlib import contextmanager


@contextmanager
def base():
    with html(lang="en"):
        with head():
            meta(charset="utf-8")
            meta(name="viewport",
                 content="width=device-width, initial-scale=1")
            title("Hypergen • TodoMVC")
            script(src=static("freedom/hypergen.min.js"))
            link(static("todomvc.css"))
        with body():
            yield
            with footer(class_="info"):
                p("Double-click to edit a todo")
                with p():
                    a("Sindre Sorhus", href="http://sindresorhus.com")
                with p():
                    a("Django Freedom",
                      href="https://github.com/runekaagaard/django-freedom")
                with p():
                    a("TodoMVC", href="http://todomvc.com")


def content():
    with section(class_="todoapp"):
        with header(class_="header"):
            h1("todos")
            input_(class_="new-todo", placeholder="What needs to be done?",
                   autofocus="")
        with section(class_="main"):
            input_(id_="toggle-all", class_="toggle-all", type_="checkbox")
            label("Mark all as complete", for_="toggle-all")
            with ul(class_="todo-list"):
                with li(class_="completed"):
                    with div(class_="view"):
                        input_(class_="toggle", type_="checkbox", checked="")
                        label("Taste JavaScript")
                        button(class_="destroy")
                    input_(class_="edit", value="Create a TodoMVC template")
                with li():
                    with div(class_="view"):
                        input_(class_="toggle", type_="checkbox")
                        label("Buy a unicorn")
                        button(class_="destroy")
                    input_(class_="edit", value="Rule the web")
        with footer(class_="footer"):
            with span(class_="todo-count"):
                strong("0")
            with ul(class_="filters"):
                with li():
                    a("All", class_="selected", href="#/")
                with li():
                    a("Active", href="#/active")
                with li():
                    a("Completed", href="#/completed")
            button("Clear completed", class_="clear-completed")
