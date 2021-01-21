# coding=utf-8
# yapf: disable
from flask import Flask
from hypergen import *
from hypergen import flask_liveview_hypergen as hypergen

app = Flask(__name__, static_url_path='', static_folder='')

# Automatically setup flask routes for callbacks.
flask_liveview_autoroute_callbacks(app, "/cbs/")

# This is our base template, that can be shared between pages.
def base_template(content_func):
    doctype()
    with html.c():
        with head.c():
            title("We <3 hypergen")
            script(src="/dependencies.js")
            script(src="/hypergen.js")
            link(href="/readme_example.css", rel="stylesheet", type_="text/css")
        with body.c():
            with div.c(id_="content"):
                content_func()

# State.
TODOS = {
    "items": [
        {"task": "Remember the milk", "is_done": False},
        {"task": "Walk the dog", "is_done": False},
        {"task": "Get the kids to school", "is_done": True},
    ],
    "toggle_all": False,
    "filt": None,
}

# Now follows callbacks.

def toggle_all(is_done):
    TODOS["toggle_all"] = is_done

    for item in TODOS["items"]:
        item["is_done"] = is_done

def toggle_one(i, is_done):
    TODOS["items"][i]["is_done"] = is_done

def add(task):
    TODOS["items"].append({"task": task, "is_done": False})

def clear_completed():
    TODOS["items"] = [x for x in TODOS["items"] if not x["is_done"]]

def set_filter(filt):
    TODOS["filt"] = filt

# App template.
def template():
    input_(type_="checkbox", checked=TODOS["toggle_all"], onclick=(toggle_all, THIS))
    new_item = input_(placeholder="What needs to be done?")
    input_(type_="button", value="Add", onclick=(add, new_item))
    with ul.c():
        for i, item in enumerate(TODOS["items"]):
            if TODOS["filt"] is not None and TODOS["filt"] != item["is_done"]:
                continue
            with li.c():
                input_(type_="checkbox", checked=item["is_done"], onclick=(toggle_one, i, THIS))
                write(item["task"])

    span("All", onclick=(set_filter, None))
    span("Active", onclick=(set_filter, False))
    span("Completed", onclick=(set_filter, True))
    input_(type_="button", value="Clear completed", onclick=(clear_completed, ))

# App route.
@app.route('/')
def todo():
    def callback_output():
        return hypergen(template, target_id="content", flask_app=app)

    return hypergen(base_template, template, flask_app=app, callback_output=callback_output)
