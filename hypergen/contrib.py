#coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)
from functools import wraps

try:
    import cPickle as pickle
except ImportError:
    import pickle

from contextlib2 import contextmanager

from django.urls.base import resolve, reverse
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import ensure_csrf_cookie

from hypergen.core import context as c, wrap2
from hypergen.core import loads, command, hypergen, hypergen_response, StringWithMeta

d = dict
_URLS = {}
NO_PERM_REQUIRED = "__NO_PERM_REQUIRED__"

def register_view_for_url(func, namespace, base_template, url=None):
    def _reverse(*view_args, **view_kwargs):
        return StringWithMeta(reverse("{}:{}".format(namespace, func.__name__), args=view_args, kwargs=view_kwargs),
            d(base_template=base_template))

    func.reverse = _reverse

    module = func.__module__
    if module not in _URLS:
        _URLS[module] = set()

    if url is None:
        url = r"^{}/$".format(func.__name__)

    _URLS[module].add((func, url))

    return func

@contextmanager
def appstate(app_name, appstate_init):
    if app_name is None or appstate_init is None:
        yield
        return

    k = "hypergen_appstate_{}".format(app_name)
    appstate = c.request.session.get(k, None)
    if appstate is not None:
        appstate = pickle.loads(appstate.encode('latin1'))
    else:
        appstate = appstate_init()
    with c(appstate=appstate):
        yield
        c.request.session[k] = pickle.dumps(c.appstate, pickle.HIGHEST_PROTOCOL).decode('latin1')

@wrap2
def hypergen_view(func, url=None, perm=None, base_template=None, base_template_args=None, base_template_kwargs=None,
    namespace=None, login_url=None, raise_exception=False, target_id=None, app_name=None, appstate_init=None):

    assert perm is not None or perm == NO_PERM_REQUIRED, "perm is required"
    assert base_template is not None, "base_template required"
    assert target_id is not None, "target_id required"
    assert namespace is not None, "namespace required"

    if base_template_args is None:
        base_template_args = tuple()
    if base_template_kwargs is None:
        base_template_kwargs = {}

    @wraps(func)
    def _(request, *fargs, **fkwargs):
        path = c.request.get_full_path()
        c.base_template = base_template

        func_return = {}

        @appstate(app_name, appstate_init)
        def wrap_base_template(request, *fargs, **fkwargs):
            with base_template(*base_template_args, **base_template_kwargs):
                func_return["value"] = func(request, *fargs, **fkwargs)
                command("history.replaceState", d(callback_url=path), "", path)

        @appstate(app_name, appstate_init)
        def wrap_view_with_hypergen():
            func_return["value"] = func(request, *fargs, **fkwargs)

        if not c.request.is_ajax():
            html = hypergen(wrap_base_template, request, *fargs, **fkwargs)
            if func_return["value"] is not None:
                html = func_return["value"]
            return hypergen_response(html)
        else:
            commands = hypergen(wrap_view_with_hypergen, target_id=target_id)
            if func_return["value"] is not None:
                commands = func_return["value"]

            data = loads(c.request.POST["hypergen_data"])
            if not ("meta" in data and "is_popstate" in data["meta"]
                and data["meta"]["is_popstate"]) and type(commands) in (list, tuple):
                commands.append(command("history.pushState", d(callback_url=path), "", path, return_=True))
            return hypergen_response(commands)

    if perm != NO_PERM_REQUIRED:
        _ = permission_required2(perm, login_url=login_url, raise_exception=raise_exception)(_)

    _ = ensure_csrf_cookie(_)
    _ = register_view_for_url(_, namespace, base_template, url=url)
    _.original_func = func

    return _

@contextmanager
def no_base_template(*args, **kwargs):
    yield

# TODO: Start. Make permission_required aware of ajax.
try:
    from functools import wraps
    from django.conf import settings
    from django.contrib.auth import REDIRECT_FIELD_NAME
    from django.core.exceptions import PermissionDenied
    from django.shortcuts import resolve_url
    from django.utils import six
    from django.utils.decorators import available_attrs
    from django.utils.six.moves.urllib.parse import urlparse

    def user_passes_test2(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
        """
        Decorator for views that checks that the user passes the given test,
        redirecting to the log-in page if necessary. The test should be a callable
        that takes the user object and returns True if the user passes.
        """
        def decorator(view_func):
            @wraps(view_func, assigned=available_attrs(view_func))
            def _wrapped_view(request, *args, **kwargs):
                if test_func(request.user):
                    return view_func(request, *args, **kwargs)
                path = request.build_absolute_uri()
                resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
                # If the login url is the same scheme and net location then just
                # use the path as the "next" url.
                login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
                current_scheme, current_netloc = urlparse(path)[:2]
                if ((not login_scheme or login_scheme == current_scheme)
                        and (not login_netloc or login_netloc == current_netloc)):
                    path = request.get_full_path()
                from django.contrib.auth.views import redirect_to_login
                return hypergen_response(redirect_to_login(path, resolved_login_url, redirect_field_name))

            return _wrapped_view

        return decorator

    def permission_required2(perm, login_url=None, raise_exception=False):
        """
        Decorator for views that checks whether a user has a particular permission
        enabled, redirecting to the log-in page if necessary.
        If the raise_exception parameter is given the PermissionDenied exception
        is raised.
        """
        def check_perms(user):
            if isinstance(perm, six.string_types):
                perms = (perm,)
            else:
                perms = perm
            # First check if the user has the permission (even anon users)
            if user.has_perms(perms):
                return True
            # In case the 403 handler should be called raise the exception
            if raise_exception:
                raise PermissionDenied
            # As the last resort, show the login form
            return False

        return user_passes_test2(check_perms, login_url=login_url)
except:
    permission_required2 = permission_required

# TODO: End.

@wrap2
def hypergen_callback(func, url=None, perm=None, namespace=None, target_id=None, login_url=None,
    raise_exception=False, base_template=None, app_name=None, appstate_init=None, view=None):
    assert perm is not None or perm == NO_PERM_REQUIRED, "perm is required"
    assert namespace is not None, "namespace is required"
    if base_template is None:
        base_template = no_base_template

    @wraps(func)
    def _(request, *fargs, **fkwargs):
        referer_resolver_match = resolve(c.request.META["HTTP_X_PATHNAME"])

        @appstate(app_name, appstate_init)
        def wrap_view_with_hypergen(func_return, args):
            func_return["value"] = func(request, *args, **fkwargs)
            if view is not None:
                view.original_func(request, *referer_resolver_match.args, **referer_resolver_match.kwargs)

        assert c.request.method == "POST", "Only POST request are supported"
        assert c.request.is_ajax()
        c.base_template = base_template

        args = list(fargs)
        args.extend(loads(request.POST["hypergen_data"])["args"])
        with c(referer_resolver_match=referer_resolver_match):
            func_return = {}
            commands = hypergen(wrap_view_with_hypergen, func_return, args, target_id=target_id)
            commands = commands if func_return["value"] is None else func_return["value"]

            return hypergen_response(commands)

    if perm != NO_PERM_REQUIRED:
        _ = permission_required2(perm, login_url=login_url, raise_exception=raise_exception)(_)

    _ = ensure_csrf_cookie(_)
    _ = register_view_for_url(_, namespace, base_template, url=url)
    _.original_func = func

    return _

def hypergen_urls(module):
    patterns = []
    for func, url_ in _URLS.get(module.__name__, []):
        patterns.append(url(url_, func, name=func.__name__))

    return patterns
