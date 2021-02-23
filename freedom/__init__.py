# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)
import datetime, json, sys
from functools import partial

if sys.version_info.major > 2:
    pass
else:
    str = unicode

default_app_config = 'freedom.apps.Freedom'


def encoder(this, o):
    from freedom.hypergen import THIS, base_element
    if hasattr(o, "hypergen_callback_url"):
        return o.hypergen_callback_url
    elif issubclass(type(o), base_element):
        assert o.attrs.get("id_", False), "Missing id_"
        return ["_", "element_value", [o.js_cb, o.attrs["id_"].v]]
    elif isinstance(o, datetime.datetime):
        assert False, "TODO"
        return ["_", "datetime", o.isoformat()]
    elif isinstance(o, datetime.date):
        assert False, "TODO"
        return ["_", "date", o.isoformat()]
    elif hasattr(o, "__weakref__"):
        # Lazy strings and urls.
        return str(o)
    else:
        raise TypeError(repr(o) + " is not JSON serializable")


def dumps(data, default=encoder, unquote=False, escape=False, this=None):
    from freedom.hypergen import t
    result = json.dumps(
        data, default=partial(encoder, this), separators=(',', ':'))
    if unquote:
        result = _unquote(result)
    if escape:
        result = t(result)

    return result


def loads(data, default=encoder):
    return json.loads(data)


quote = lambda x: "H_" + x + "_H"

_unquote = lambda x: x.replace('"H_', "").replace('_H"', "")[1:-1]
