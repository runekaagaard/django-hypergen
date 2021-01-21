import threading
from django.db import models as m

global_context = threading.local()


def update_global_context(data):
    for k, v in data.items():
        setattr(global_context, k, v)


def global_context_middleware(get_response):
    def _(request):
        update_global_context({"user": request.user})
        return get_response(request)

    return _
