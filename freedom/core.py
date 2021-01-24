import threading
from contextlib import contextmanager

from pyrsistent import pmap, m

local = threading.local()


def evolver(data):
    def get(self, k, v="__NONE__"):
        try:
            return self[k]
        except KeyError:
            if v != "__NONE__":
                return v
            else:
                raise

    setattr(data._Evolver, 'get', get)
    return data.evolver()


@contextmanager
def context(mutator=None, **values):
    if not hasattr(local, "context"):
        local.context = pmap()

    context = local.context
    try:
        if mutator is not None:
            local.context = mutator(evolver(local.context)).persistent()
        local.context = local.context.update(m(**values))
        yield local.context
    finally:
        local.context = context


def context_middleware(get_response):
    def _(request):
        with context(user=request.user, request=request):
            return get_response(request)

    return _
