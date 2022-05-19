from hypergen.utils import *

from html import escape

__all__ = ["OMIT", "t"]

### Constants ####

OMIT = "__OMIT__"

def t(s, quote=True):
    return escape(make_string(s), quote=quote)
