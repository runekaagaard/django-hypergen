# coding=utf-8
import datetime, json, sys
from functools import partial

if sys.version_info.major > 2:
    pass
else:
    str = unicode

default_app_config = 'freedom.apps.Freedom'


def encoder(this, o):
    from freedom._hypergen import THIS, base_element
    print 2222222222222222222222222, type(o), issubclass(type(o), base_element)
    if o is THIS:
        return quote(this)
    elif issubclass(type(o), base_element):
        return [
            "_",
            "element_value",
            {
                "id": o.attrs["id_"],
                "cb_name": o.js_cb.replace("H.cbs.", ""),  # TODO: Generalize.
            }
        ]
        # return quote(o.meta["this"])
    elif isinstance(o, datetime.datetime):
        assert False, "TODO"
        return str(o)
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
