# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)
d = dict

import threading
from contextlib2 import contextmanager
from functools import wraps, update_wrapper

from django.conf.urls import url
from django.urls.base import reverse_lazy
from pyrsistent import pmap, m


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
            return AttributeError("No such attribute: " + k)

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


def wrap2(f):
    """
    A a decorator decorator, allowing the decorator to be used as:
        @decorator(with, arguments, and=kwargs)
    or
        @decorator
    
    It does not work for a wrapped function that takes a callback as the only input.

    It looks like this:

        @wrap2
        def mydecorator(func, *dargs, **dkwargs):
            @wraps(func)
            def _(*fargs, **fkwargs):
                return func(*fargs, **fkwargs)

            return _


        @mydecorator
        def myfunc(x, y=19):
            return x + y


        @mydecorator(42, foo=True)
        def myfunc2(x, y=19):
            return x + y
    """

    def _(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            f2 = f(args[0])
            update_wrapper(f2, args[0])
            return f2
        else:

            def f3(f4):
                f5 = f(f4, *args, **kwargs)
                update_wrapper(f5, f4)
                return f5

            return f3

    return _


def wrap3(dfunc):
    """
    A a decorator decorator, allowing the decorator to be used as:
        @decorator(with, arguments, and=kwargs)
    or
        @decorator

    It does not work for a wrapped function that takes a callback as the only input.

    It looks like this:

        @wrap3
        def mydecorator(func, fargs, fkwargs, *dargs, **dkwargs):
            print "Decorator args, kwargs are", dargs, dkwargs
            func(*fargs, **fkwargs)


        @mydecorator
        def myfunc(x, y=19):
            return x + y


        @mydecorator(42, foo=True)
        def myfunc2(x, y=19):
            return x + y
    """

    def _(*xargs, **xkwargs):
        if len(xargs) == 1 and len(xkwargs) == 0 and callable(xargs[0]):
            # Without decorator args, kwargs.
            func = xargs[0]

            @wraps(func)
            def __(*fargs, **fkwargs):
                dfunc(func, fargs, fkwargs)

            return __
        else:
            # With decorator args, kwargs.
            dargs, dkwargs = xargs, xkwargs

            def __(func):
                @wraps(func)
                def ___(*fargs, **fkwargs):
                    return dfunc(func, fargs, fkwargs, *dargs, **dkwargs)

                return ___

            return __

    return _


def insert(source_str, insert_str, pos):
    return ''.join((source_str[:pos], insert_str, source_str[pos:]))


class SkipException(Exception):
    pass


@contextmanager
def skippable():
    try:
        yield
    except SkipException:
        pass


class adict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name] if type(self[name]) is not dict else adict(
                self[name])
        else:
            raise AttributeError("No such attribute: " + name)

    def __getitem__(self, name):
        value = super(adict, self).__getitem__(name)
        return value if value is not dict else adict(value)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


_URLS = {}


@wrap2
def autourl(func, *dargs, **dkwargs):
    namespace = dkwargs.get("namespace", "")

    module = func.__module__
    if module not in _URLS:
        _URLS[module] = []

    view_name = "{}__{}".format(module.replace(".", "__"), func.__name__)
    func.hypergen_view_name = view_name
    func.hypergen_namespace = namespace
    func.hypergen_callback_url = reverse_lazy(
        ":".join((namespace, func.hypergen_view_name)))

    _URLS[module].append(func)

    @wraps(func)
    def _(*fargs, **fkwargs):
        return func(*fargs, **fkwargs)

    return _


def autourl_patterns(namespace, module):
    patterns = []
    for func in _URLS.get(module.__name__, []):
        patterns.append(
            url('^{}/$'.format(func.__name__),
                func,
                name=func.hypergen_view_name))

    return patterns
