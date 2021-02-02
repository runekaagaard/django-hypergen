from functools import wraps, update_wrapper
from contextlib import contextmanager


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

        @decorator
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
