from threading import local
try:
    from html import escape
except:
    from cgi import escape

data = local()


def hypergen(func, *args, **kwargs):
    try:
        data.html = []
        func(*args, **kwargs)
        html = "".join(data.html)
    except:
        data.html = []
        raise
    finally:
        data.html = []
    return html


def element(tag, inner, **attrs):
    cdef:
        str k
        str v
        
    e = data.html.extend
    e(("<", tag))
    e([
        escape(k, quote=True) + '=' + escape(v, quote=True)
        for k, v in attrs.iteritems()
    ])
    e(('>', inner, "</", tag, ">"))


def tag_open(str tag, **attrs):
    cdef:
        str k
        str v
        
    e = data.html.extend
    e(("<", tag))
    e([
        escape(k, quote=True) + '=' + escape(v, quote=True)
        for k, v in attrs.iteritems()
    ])

    e(('>', ))


cdef void tag_close(str tag):
    data.html.extend(("</", tag, ">"))


cdef write(str html):
    data.html.extend(escape(html, quote=False))


def _bigtable_benchmark_real_py(ctx):
    tag_open("table")
    for row in ctx['table']:
        tag_open("tr")
        for key, value in row.items():
            element("td", key)
            element("td", str(value))
        tag_close("tr")
    tag_close("table")


def bigtable_benchmark_real_py(ctx):
    return hypergen(_bigtable_benchmark_real_py, ctx)
