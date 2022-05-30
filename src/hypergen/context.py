d = dict

from abc import abstractmethod
from collections import defaultdict
import threading
from contextlib import contextmanager
from pyrsistent import pmap, m

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object  # Backwards compatibility.

__all__ = ["context"]

class Context(threading.local):
    def __init__(self):
        self.ctx = pmap()
        super(Context, self).__init__()

    def replace(self, **items):
        self.ctx = m(**items)

    def __getattr__(self, k):
        try:
            return self.__dict__['ctx'][k]
        except KeyError:
            raise AttributeError("No such attribute: " + k)

    def __setattr__(self, k, v):
        if k == "ctx":
            return super(Context, self).__setattr__(k, v)
        else:
            self.ctx = self.ctx.set(k, v)

    def __getitem__(self, k):
        return self.__dict__['ctx'][k]

    def __setitem__(self, k, v):
        raise Exception("TODO")

    def __contains__(self, k):
        return k in self.ctx

    def clone(self):
        c = Context()
        c.ctx = self.ctx

        return c

    @contextmanager
    def __call__(self, transformer=None, at=None, **items):
        try:
            # Store previous value.
            ctx = self.ctx
            if at is None:
                if transformer is not None:
                    self.ctx = transformer(self.ctx)
                self.ctx = self.ctx.update(m(**items))
            else:
                if at not in self.ctx:
                    self.ctx = self.ctx.set(at, pmap(items))
                else:
                    new_value_at = self.ctx[at].update(pmap(items))
                    if not new_value_at:
                        raise Exception("Not immutable context variable attempted updated. If you want to nest "
                            "with context() statements you must use a pmap() or another immutable hashmap type.")

                    self.ctx = self.ctx.set(at, new_value_at)

                if transformer is not None:
                    self.ctx = self.ctx.set(at, transformer(self.ctx[at]))

            yield
        finally:
            # Reset to previous value.
            self.ctx = ctx

context = Context()
c = context

def _init_context(request):
    return dict(request=request)

def context_middleware(get_response):
    def _(request):
        with context(**_init_context(request)):
            return get_response(request)

    return _

class ContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        context.replace(**_init_context(request))

from collections import UserList

class contextlist(UserList):
    def __init__(self, *args, **kwargs):
        self.target_ids = defaultdict(list)
        super(contextlist, self).__init__(*args, **kwargs)

    @property
    def data(self):
        return self.target_ids[context.hypergen.get("target_id", "__hypergen__main__")]

    @data.setter
    def data(self, value):
        self.target_ids[context.hypergen.get("target_id", "__hypergen__main__")] = value
