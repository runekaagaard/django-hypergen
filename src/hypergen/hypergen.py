from hypergen.utils import *

from html import escape
from functools import update_wrapper

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
try:
    from django.utils.encoding import force_text as force_str
except ImportError:
    from django.utils.encoding import force_str

__all__ = ["OMIT"]

### Constants ###

OMIT = "__OMIT__"

### Helpers internal to hypergen, DONT use these! ###

def make_string(s):
    if s is None:
        return ""
    else:
        return force_str(s)

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

# Permissions

class __PERMS_OK:
    pass

def check_perms(request, perm, login_url=None, raise_exception=False, any_perm=False, redirect_field_name=None):
    from hypergen.liveview import NO_PERM_REQUIRED
    matched_perms = set()

    if perm == NO_PERM_REQUIRED:
        return True, None, matched_perms

    def check_perms_for_user(user):
        nonlocal matched_perms
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm

        if any_perm is not True:
            if user.has_perms(perms):
                matched_perms = set(perms)
                return True
        else:
            for p in perms:
                if user.has_perm(p):
                    matched_perms.add(p)

            if matched_perms:
                return True

        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False

    @user_passes_test(check_perms_for_user, login_url=login_url, redirect_field_name=redirect_field_name)
    def perm_fake_view(request):
        return __PERMS_OK

    check = perm_fake_view(request)

    if check is __PERMS_OK:
        return True, None, matched_perms
    else:
        return False, check, matched_perms
