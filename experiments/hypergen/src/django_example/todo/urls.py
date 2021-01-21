from l1ve import view

PERM_ITEMS = ("items", "Can edit todo items")


@view("/todo/items", perm=PERM_ITEMS)
def items(request):
    pass
