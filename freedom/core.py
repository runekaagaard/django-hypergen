import threading
from contextlib import contextmanager

from pyrsistent import pmap, m


class Context(threading.local):
    def __init__(self):
        self.ctx = pmap()
        super(Context, self).__init__()

    def replace(self, **items):
        self.ctx = m(**items)

    def __getattr__(self, k):
        return self.__dict__['ctx'][k]

    def __getitem__(self, k):
        return self.__dict__['ctx'][k]

    def __contains__(self, k):
        return k in self.ctx

    @contextmanager
    def __call__(self, transformer=None, at=None, **items):
        try:
            ctx = self.ctx
            if at is None:
                if transformer is not None:
                    self.ctx = transformer(self.ctx)
                self.ctx = self.ctx.update(m(**items))
            else:
                if transformer is not None:
                    self.ctx = self.ctx.set(at, transformer(self.ctx[at]))
                self.ctx = self.ctx.set(at, self.ctx[at].update(m(**items)))
            yield
        finally:
            self.ctx = ctx


context = Context()


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
