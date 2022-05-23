from hypergen.utils import *

from html import escape
from functools import wraps, update_wrapper

try:
    from django.utils.encoding import force_text as force_str
except ImportError:
    from django.utils.encoding import force_str

__all__ = ["OMIT"]

### Constants ####

OMIT = "__OMIT__"

### Helpers internal to hypergen, DONT use these.

def t(s, quote=True):
    return escape(make_string(s), quote=quote)

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

def make_string(s):
    if s is None:
        return ""
    else:
        return force_str(s)
