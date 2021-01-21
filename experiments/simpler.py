from framework import path, perm, db
from hypergen import hypergen
from hypergen.elements import ul, li, span, input_, button, h2, textarea


@hypergen(dom_id="todos")
@perm("todos")
@path("todos")
def todos(request, errors=None):
    def update(item_id, title, description):
        db.update_item(item_id, title, description)

    def mark_all(todo_list_id, is_done):
        db.mark_all(todo_list_id, is_done)

    def mark_one(item_id, is_done):
        db.mark_one(item_id, is_done)

    def add(todo_list_id, title, description):
        db.add(todo_list_id, title, description)

    for todo_list in db.todo_lists(user=request.user):
        h2(todo_list.title)
        with ul(class_="todos"):
            button(
                "Mark all completed", onclick=(mark_all, todo_list.id, True))

            for item in todo_list:
                with li():
                    title = span(item.title, contenteditable=True)
                    description = input_(value=item.description)
                    button(
                        "Update",
                        onclick=(update, item.id, title, description))

            title = input_()
            description = textarea()
            button("Add new", onclick=(add, todo_list.id, title, description))
