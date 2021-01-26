import threading
from contextlib import contextmanager

from pyrsistent import pmap, m

local = threading.local()
local.context = pmap()


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
def local_context(mutator=None, **values):
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


def set_context(request):
    local.context = pmap(_init_context(request))


def _init_context(request):
    return dict(user=request.user, request=request)


def context_middleware(get_response):
    def _(request):
        with local_context(**_init_context(request)):
            return get_response(request)

    return _


def context():
    return local.context


class ContextMiddleware(object):
    def process_request(self, request):
        # TODO. Change to MIDDLEWARE and not MIDDLEWARE_CLASSES
        local.context = pmap(_init_context(request))
