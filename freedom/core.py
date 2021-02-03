import threading
from contextlib import contextmanager

from pyrsistent import pmap, m


class Context(threading.local):
    ctx = pmap()
    
    def replace(self, **items):
        self.ctx = m(**items)

    def __getattr__(self, k):
        return self.__dict__['ctx'][k]

    def __contains__(self, k):
        return k in self.ctx

    @contextmanager
    def __call__(self, mutator=None, **items):
        try:
            ctx = self.ctx
            if mutator is not None:
                self.ctx = mutator(evolver(self.ctx)).persistent()
            self.ctx = self.ctx.update(m(**items))
            yield self.ctx
        finally:
            self.ctx = ctx

    # def ns(self, mutator=None, **items):
    #     return Context()(mutator=mutator, **items)
        
def namespace(**items):
    from bunch import Bunch
    return Bunch(**items)

context = Context()


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


def _init_context(request):
    return dict(user=request.user, request=request)


def context_middleware(get_response):
    def _(request):
        with context(**_init_context(request)):
            return get_response(request)

    return _


class ContextMiddleware(object):
    def process_request(self, request):
        # TODO. Change to MIDDLEWARE and not MIDDLEWARE_CLASSES
        context.replace(**_init_context(request))
