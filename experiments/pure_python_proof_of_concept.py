from threading import local
try:
    from html import escape
except:
    from cgi import escape

data = local()


def hypergen(func, *args, **kwargs):
    try:
        data.html = []
        data.extend = data.html.extend
        func(*args, **kwargs)
        html = "".join(data.html)
    finally:
        data.html = []
        data.extend = None

    return html


def element(tag, inner, **attrs):
    e = data.extend
    e(("<", tag))
    e([
        escape(k, quote=True) + '=' + escape(v, quote=True)
        for k, v in attrs.iteritems()
    ])
    e(('>', inner, "</", tag, ">"))


def tag_open(tag, **attrs):
    e = data.extend
    e(("<", tag))
    e([
        escape(k, quote=True) + '=' + escape(v, quote=True)
        for k, v in attrs.iteritems()
    ])

    e(('>', ))


def tag_close(tag):
    data.extend(("</", tag, ">"))


def write(html):
    data.extend(escape(html, quote=False))


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
