#coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)
from functools import wraps

from django.urls.base import reverse_lazy, resolve, reverse
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from django.http.response import HttpResponse

from freedom.core import context as c, wrap2
from freedom.hypergen import loads, command, hypergen, hypergen_as_response, hypergen_response, dumps

d = dict
_URLS = {}
NO_PERM_REQUIRED = "__NO_PERM_REQUIRED__"

def register_view_for_url(func, namespace, url=None):
    def _reverse(*view_args, **view_kwargs):
        return reverse("{}:{}".format(namespace, func.__name__),
                       args=view_args, kwargs=view_kwargs)

    func.reverse = _reverse

    module = func.__module__
    if module not in _URLS:
        _URLS[module] = set()

    if url is None:
        url = r"^{}/$".format(func.__name__)

    _URLS[module].add((func, url))

    return func

@wrap2
def hypergen_view(func, url=None, perm=None, base_template=None,
                  base_template_args=None, base_template_kwargs=None,
                  namespace=None, login_url=None, raise_exception=False,
                  target_id=None):

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

        def wrap_base_template(request, *fargs, **fkwargs):
            with base_template(*base_template_args, **base_template_kwargs):
                func(request, *fargs, **fkwargs)
                command("history.replaceState", d(callback_url=path), "", path)

        if not c.request.is_ajax():
            return hypergen_as_response(wrap_base_template, request, *fargs,
                                        **fkwargs)
        else:
            fkwargs["target_id"] = target_id
            commands = hypergen(func, request, *fargs, **fkwargs)
            data = loads(c.request.POST["hypergen_data"])
            if not ("meta" in data and "is_popstate" in data["meta"]
                    and data["meta"]["is_popstate"]):
                commands.append(
                    command("history.pushState", d(callback_url=path), "",
                            path, return_=True))
            return hypergen_response(commands)

    if perm != NO_PERM_REQUIRED:
        _ = permission_required(perm, login_url=login_url,
                                raise_exception=raise_exception)(_)

    return register_view_for_url(_, namespace, url=url)

@wrap2
def hypergen_callback(func, url=None, perm=None, namespace=None,
                      target_id=None, login_url=None, raise_exception=False):
    assert perm is not None or perm == NO_PERM_REQUIRED, "perm is required"
    assert namespace is not None, "namespace is required"
    assert target_id is not None, "target_id is required"

    @wraps(func)
    def _(request, *fargs, **fkwargs):
        def wrap_view_with_hypergen(func_return):
            func_return["value"] = func(request, *args, **fkwargs)

        assert c.request.is_ajax()
        args = list(fargs)
        args.extend(loads(request.POST["hypergen_data"])["args"])
        with c(referer_resolver_match=resolve(
                c.request.META["HTTP_X_PATHNAME"])):
            func_return = {}
            commands = hypergen(wrap_view_with_hypergen, func_return,
                                target_id=target_id)
            commands = commands if func_return[
                "value"] is None else func_return["value"]

            return hypergen_response(commands)

    if perm != NO_PERM_REQUIRED:
        _ = permission_required(perm, login_url=login_url,
                                raise_exception=raise_exception)(_)

    return register_view_for_url(_, namespace, url=url)

def hypergen_urls(module):
    patterns = []
    for func, url_ in _URLS.get(module.__name__, []):
        patterns.append(url(url_, func, name=func.__name__))

    return patterns
