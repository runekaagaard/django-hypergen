"""
Yes it really _is_ possible to differentiate between html element called as:
    - decorator
    - context manager
    - function
    - argument to other html element
"""
from contextlib2 import ContextDecorator

html = []
i = -1


def open_tag(tag, **kwargs):
    s = "<" + tag
    if kwargs:
        s += " " + " ".join("=".join((k.rstrip("_"), v))
                            for k, v in list(kwargs.items()))
    return s + ">"


DELETED = None


class div(ContextDecorator):
    def __init__(self, s, **kwargs):
        global i
        i += 1
        self.i = i
        self.s = s
        self.kwargs = kwargs
        if not issubclass(type(s), ContextDecorator):
            self.html = lambda: open_tag("div", **kwargs) + s + "</div>"
        else:
            html[s.i] = DELETED
            self.html = lambda: open_tag("div", **kwargs) + (s.html() if callable(s.html) else s.html) + "</div>"

        html.append(self.html)
        super(div, self).__init__()

    def __enter__(self):
        global i
        i += 1
        html.append(open_tag("div", **self.kwargs) + self.s)
        html[self.i] = DELETED
        return self

    def __exit__(self, *exc):
        global i
        i += 1
        html.append("</div>")
        return False


html = []
i = -1


@div("A", id_="aid", class_="a-cls")
def function(s):
    div("inner A", id_="innerida")


function("a-a")
print("+++++++++++++++++")
print("\n".join(x() if callable(x) else x for x in html
                if x != DELETED).strip())
print("-----------------")

# ------------------------------------------------- #

html = []
i = -1

with div("B", id_="bid", class_="b-cls"):
    div("inner B", id_="inneridb")

print("+++++++++++++++++")
print("\n".join(x() if callable(x) else x for x in html
                if x != DELETED).strip())
print("-----------------")

# ------------------------------------------------- #

html = []
i = -1

div("C", id_="cid", class_="c-cls")

print("+++++++++++++++++")
print("\n".join(x() if callable(x) else x for x in html
                if x != DELETED).strip())
print("-----------------")

# ------------------------------------------------- #

html = []
i = -1

div(div(div("D", id_="did1"), id_="did2"), id_="did3")
div(div(div("D", id_="did1"), id_="did2"), id_="did3")

print("+++++++++++++++++")
print("\n".join(x() if callable(x) else x for x in html
                if x != DELETED).strip())
print("-----------------")
