# Local Variables:
# flycheck-mode: nil
# End:

from threading import local

S = local()

def page(title, content):
    menu()
    with div_cm("outer"), div_cm("inner"):
        h1(title)
        content()
    footer()

def update_item(item_id, form_data):
    item = db.update_title(item_id, form_data["title"])
    todo_item(item)

def complete(item_id):
    item = db.update_title(item_id, form_data["title"])
    index()

@li(signature=lambda f, item: [f, item.id, item.version])
def todo_item(item, edit=False):
    if not edit:
        write(item.title)
        span("edit", onclick=(complete, item.id))
    else:
        with form_cm(signature=["form"]) as form:
            input_(type_="text", name="title", value=item.title)
            button("save", onclick=(update_item, item.id, form.data))

    span("complete", onclick=(complete, item.id))

def index(reverse=False):
    p("Show last first" if reverse else "Show first first", onclick=(index, not reverse))

    todo_lists = db.todo_lists(reverse=reverse)
    for todo_list in todo_lists:
        h2(todo_list.title)
        with ul_cm():
            for item in todo_list.items:
                todo_item()

print(hypergen(page, partial(index)))
