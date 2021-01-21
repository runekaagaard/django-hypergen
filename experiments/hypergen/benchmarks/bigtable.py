"""
"""

import sys

try:
    from wheezy.html.utils import escape_html as escape
except ImportError:
    import cgi
    escape = cgi.escape

PY3 = sys.version_info[0] >= 3
s = PY3 and str or unicode

ctx = {
    'table': [
        dict(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)
        for x in range(10000)
    ]
}

# region: python list append

if PY3:

    def test_list_append():
        b = []
        w = b.append
        table = ctx['table']
        w('<table>\n')
        for row in table:
            w('<tr>\n')
            for key, value in row.items():
                w('<td>')
                w(escape(key))
                w('</td><td>')
                w(str(value))
                w('</td>\n')
            w('</tr>\n')
        w('</table>')
        return ''.join(b)
else:

    def test_list_append():  # noqa
        b = []
        w = b.append
        table = ctx['table']
        w(u'<table>\n')
        for row in table:
            w(u'<tr>\n')
            for key, value in row.items():
                w(u'<td>')
                w(escape(key))
                w(u'</td><td>')
                w(unicode(value))
                w(u'</td>\n')
            w(u'</tr>\n')
        w(u'</table>')
        return ''.join(b)


# region: python list extend

if PY3:

    def test_list_extend():
        b = []
        e = b.extend
        table = ctx['table']
        e(('<table>\n', ))
        for row in table:
            e(('<tr>\n', ))
            for key, value in row.items():
                e(('<td>', escape(key), '</td><td>', str(value), '</td>\n'))
            e(('</tr>\n', ))
        e(('</table>', ))
        return ''.join(b)
else:

    def test_list_extend():  # noqa
        b = []
        e = b.extend
        table = ctx['table']
        e((u'<table>\n', ))
        for row in table:
            e((u'<tr>\n', ))
            for key, value in row.items():
                e((u'<td>', escape(key), u'</td><td>', unicode(value),
                   u'</td>\n'))
            e((u'</tr>\n', ))
        e((u'</table>', ))
        return ''.join(b)


# region: wheezy.template

try:
    from wheezy.template.engine import Engine
    from wheezy.template.loader import DictLoader
    from wheezy.template.ext.core import CoreExtension
except ImportError:
    test_wheezy_template = None
else:
    engine = Engine(
        loader=DictLoader({
            'x':
                s("""\
@require(table)
<table>
    @for row in table:
    <tr>
        @for key, value in row.items():
        <td>@key!h</td><td>@value!s</td>
        @end
    </tr>
    @end
</table>
""")
        }),
        extensions=[CoreExtension()])
    engine.global_vars.update({'h': escape})
    wheezy_template = engine.get_template('x')

    def test_wheezy_template():
        return wheezy_template.render(ctx)


# region: Jinja2

try:
    from jinja2 import Environment
except ImportError:
    test_jinja2 = None
else:
    jinja2_template = Environment().from_string(
        s("""\
<table>
    {% for row in table: %}
    <tr>
        {% for key, value in row.items(): %}
        <td>{{ key | e }}</td><td>{{ value }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
</table>
"""))

    def test_jinja2():
        return jinja2_template.render(ctx)


# region: tornado

try:
    from tornado.template import Template
except ImportError:
    test_tornado = None
else:
    tornado_template = Template(
        s("""\
<table>
    {% for row in table %}
    <tr>
        {% for key, value in row.items() %}
        <td>{{ key }}</td><td>{{ value }}</td>
        {% end %}
    </tr>
    {% end %}
</table>
"""))

    def test_tornado():
        return tornado_template.generate(**ctx).decode('utf8')


# region: mako

try:
    from mako.template import Template
except ImportError:
    test_mako = None
else:
    mako_template = Template(
        s("""\
<table>
    % for row in table:
    <tr>
        % for key, value in row.items():
        <td>${ key | h }</td><td>${ value }</td>
        % endfor
    </tr>
    % endfor
</table>
"""))

    def test_mako():
        return mako_template.render(**ctx)


# region: tenjin

try:
    import tenjin
except ImportError:
    test_tenjin = None
else:
    try:
        import webext
        helpers = {'to_str': webext.to_str, 'escape': webext.escape_html}
    except ImportError:
        helpers = {
            'to_str': tenjin.helpers.to_str,
            'escape': tenjin.helpers.escape
        }
    tenjin_template = tenjin.Template(encoding='utf8')
    tenjin_template.convert(
        s("""\
<table>
    <?py for row in table: ?>
    <tr>
        <?py for key, value in row.items(): ?>
        <td>${ key }</td><td>#{ value }</td>
        <?py #end ?>
    </tr>
    <?py #end ?>
</table>
"""))

    def test_tenjin():
        return tenjin_template.render(ctx, helpers)


# region: web2py

try:
    import cStringIO
    from gluon.html import xmlescape
    from gluon.template import get_parsed
except ImportError:
    test_web2py = None
else:
    # see gluon.globals.Response
    class DummyResponse(object):
        def __init__(self):
            self.body = cStringIO.StringIO()

        def write(self, data, escape=True):
            if not escape:
                self.body.write(str(data))
            else:
                self.body.write(xmlescape(data))

    web2py_template = compile(
        get_parsed(
            s("""\
<table>
    {{ for row in table: }}
    <tr>
        {{ for key, value in row.items(): }}
        <td>{{ =key }}</td><td>{{ =value }}</td>
        {{ pass }}
    </tr>
    {{ pass }}
</table>
""")), '', 'exec')

    def test_web2py():
        response = DummyResponse()
        exec (web2py_template, {}, dict(response=response, **ctx))
        return response.body.getvalue().decode('utf8')


# region: django

try:
    from django.conf import settings
    DJANGO_TEMPLATES = [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
    }]
    settings.configure(TEMPLATES=DJANGO_TEMPLATES)
    import django
    django.setup()
    from django.template import Template
    from django.template import Context

except ImportError:
    test_django = None
else:
    django_template = Template(
        s("""\
<table>
    {% for row in table %}
    <tr>
        {% for key, value in row.items %}
        <td>{{ key }}</td><td>{{ value }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
</table>
"""))

    def test_django():
        return django_template.render(Context(ctx))


# region: chameleon

try:
    from chameleon.zpt.template import PageTemplate
except ImportError:
    test_chameleon = None
else:
    chameleon_template = PageTemplate(
        s("""\
<table>
    <tr tal:repeat="row table">
        <i tal:omit-tag="" tal:repeat="key row">
        <td>${key}</td><td>${row[key]}</td>
        </i>
    </tr>
</table>
"""))

    def test_chameleon():
        return chameleon_template.render(**ctx)


# region: cheetah

try:
    from Cheetah.Template import Template
except ImportError:
    test_cheetah = None
else:
    cheetah_ctx = {}
    cheetah_template = Template(
        s("""\
#import cgi
<table>
    #for $row in $table
    <tr>
        #for $key, $value in $row.items
        <td>$cgi.escape($key)</td><td>$value</td>
        #end for
    </tr>
    #end for
</table>
"""),
        searchList=[cheetah_ctx])

    def test_cheetah():
        cheetah_ctx.update(ctx)
        output = cheetah_template.respond()
        cheetah_ctx.clear()
        return output


# region: spitfire

try:
    import spitfire
    import spitfire.compiler.util
except ImportError:
    test_spitfire = None
else:
    spitfire_template = spitfire.compiler.util.load_template(
        s("""\
#from cgi import escape
<table>
    #for $row in $table
    <tr>
        #for $key, $value in $row.items()
        <td>${key|filter=escape}</td><td>$value</td>
        #end for
    </tr>
    #end for
</table>
"""), 'spitfire_template', spitfire.compiler.analyzer.o3_options,
        {'enable_filters': True})

    def test_spitfire():
        return spitfire_template(search_list=[ctx]).main()


# region: qpy

try:
    from qpy import join_xml
    from qpy import xml
    from qpy import xml_quote
except ImportError:
    test_qpy_list_append = None
else:
    if PY3:

        def test_qpy_list_append():
            b = []
            w = b.append
            table = ctx['table']
            w(xml('<table>\n'))
            for row in table:
                w(xml('<tr>\n'))
                for key, value in row.items():
                    w(xml('<td>'))
                    w(xml_quote(key))
                    w(xml('</td><td>'))
                    w(value)
                    w(xml('</td>\n'))
                w(xml('</tr>\n'))
            w(xml('</table>'))
            return join_xml(b)
    else:

        def test_qpy_list_append():
            b = []
            w = b.append
            table = ctx['table']
            w(xml(u'<table>\n'))
            for row in table:
                w(xml(u'<tr>\n'))
                for key, value in row.items():
                    w(xml(u'<td>'))
                    w(xml_quote(key))
                    w(xml(u'</td><td>'))
                    w(value)
                    w(xml(u'</td>\n'))
                w(xml(u'</tr>\n'))
            w(xml(u'</table>'))
            return join_xml(b)


# region: bottle

try:
    from bottle import SimpleTemplate
except ImportError:
    test_bottle = None
else:
    bottle_template = SimpleTemplate(
        s("""\
<table>
    % for row in table:
    <tr>
        % for key, value in row.items():
        <td>{{key}}</td><td>{{!value}}</td>
        % end
    </tr>
    % end
</table>
"""))

    def test_bottle():
        return bottle_template.render(**ctx)


from cython_proof_of_concept import (bigtable_benchmark,
                                     bigtable_benchmark_real)

from pure_python_proof_of_concept import bigtable_benchmark_real_py


def test_hypergen():
    return bigtable_benchmark()


def test_hypergen_real():
    return bigtable_benchmark_real(ctx)


def test_hypergen_real_py():
    return bigtable_benchmark_real_py(ctx)


def run(number=2):
    import profile
    from timeit import Timer
    from pstats import Stats
    names = globals().keys()
    names = sorted([(name, globals()[name]) for name in names
                    if name.startswith('test_')])
    print("                     msec    rps  tcalls  funcs")
    for name, test in names:
        if name not in (
                "test_hypergen",
                #"test_hypergen_real",
                "test_hypergen_real_py",
                "test_jinja2",
                "test_list_extend",
                "test_tenjin"):
            continue
        if name == "test_django":
            continue
        if test:
            #assert isinstance(test(), s)
            t = Timer(setup='from __main__ import %s as t' % name, stmt='t()')
            t = t.timeit(number=number)
            st = Stats(profile.Profile().runctx('test()', globals(), locals()))
            print('%-17s %7.2f %6.2f %7d %6d' %
                  (name[5:], 1000 * t / number, number / t, st.total_calls,
                   len(st.stats)))
        else:
            print('%-26s not installed' % name[5:])


if __name__ == '__main__':
    run()
