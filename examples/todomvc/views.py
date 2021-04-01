from freedom.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED
from todomvc import templates


@hypergen_view(perm=NO_PERM_REQUIRED, base_template=templates.base,
               target_id="content", namespace="todomvc")
def index(request):
    templates.content()
