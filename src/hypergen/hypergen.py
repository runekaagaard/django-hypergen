d = dict
import logging

logger = logging.getLogger(__file__)

from hypergen.context import context

from contextlib import ExitStack, contextmanager
from django.urls.base import reverse

from html import escape
from functools import update_wrapper

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
try:
    from django.utils.encoding import force_text as force_str
except ImportError:
    from django.utils.encoding import force_str

try:
    from django.conf.urls import url as re_path_, path as path_
except ImportError:
    try:
        from django.urls import re_path as re_path_, path as path_
    except:
        from django.conf.urls import url as re_path_

        def path_(*a, **kw):
            logger.error("This version of Django does not support the django.conf.urls.path() function. Sorry!")
            return re_path_(*a, **kw)

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

def compare_funcs(a, b):
    return all(getattr(a, k) == getattr(b, k) for k in ("__doc__", "__name__", "__module__", "__qualname__"))

def is_collection(x):
    if type(x) in [str, metastr]:
        return False
    try:
        iter(x)
        return True
    except TypeError:
        return False

# Permissions

class __PERMS_OK:
    pass

def check_perms(request, perm, login_url=None, raise_exception=False, any_perm=False, redirect_field_name=None):
    from hypergen.liveview import NO_PERM_REQUIRED
    matched_perms = set()

    if perm == NO_PERM_REQUIRED:
        return True, None, matched_perms

    assert perm, "perm= is required"

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

### Auto urls ###

class metastr(str):
    @staticmethod
    def make(string, meta):
        s = metastr(string)
        s.meta = meta

        return s

_URLS = {}

def autourl_register(func, base_template=None, path=None, re_path=None):
    def _reverse(*view_args, **view_kwargs):
        ns = _reverse.hypergen_namespace
        return metastr.make(reverse("{}:{}".format(ns, func.__name__), args=view_args, kwargs=view_kwargs),
            d(base_template=base_template))

    func.reverse = _reverse

    module = func.__module__
    if module not in _URLS:
        _URLS[module] = set()

    if (path, re_path) == (None, None):
        tmp = (re_path_, func, r"^{}/$".format(func.__name__))
    elif path:
        tmp = (path_, func, path)
    elif re_path:
        if re_path == "":
            raise Exception('Use "^$" for an empty re_path in {}.{}'.format(module, func.__name__))
        tmp = (re_path_, func, re_path)

    _URLS[module].add(tmp)

    return func

def autourls(module, namespace):
    patterns = []
    for path_func, func, path_ in _URLS.get(module.__name__, []):
        func.reverse.hypergen_namespace = namespace
        patterns.append(path_func(path_, func, name=func.__name__))

    return patterns

### Plugins ###

@contextmanager
def plugins_exit_stack(method_name):
    with ExitStack() as stack:
        [stack.enter_context(plugin.context()) for plugin in context.hypergen.plugins if hasattr(plugin, method_name)]
        yield

def plugins_method_call(method_name, *args, **kwargs):
    for plugin in context.hypergen.plugins:
        method = getattr(plugin, method_name, None)
        if method:
            method(*args, **kwargs)

def plugins_pipeline(method_name, data):
    for plugin in context.hypergen.plugins:
        method = getattr(plugin, method_name, None)
        if method:
            data = method(data)

    return data
