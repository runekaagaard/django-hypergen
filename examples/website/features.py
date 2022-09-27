import inspect

from hypergen.imports import *

STYLE = """
#features pre, #features code {
    padding: 0;
    margin: 0;
    background-color: transparent;
}

#features .cell {
    background-color: #272822;
    padding: 8px 16px;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    border-right: 1px solid grey;
}
#features .nc {
    background-color: transparent;
}
#features table {
   width: 100%;
   table-layout: fixed;
   overflow-wrap: break-word;
   display: table;
   padding: 0;
   margin: 0;
}
#features h4 {
    margin: 0;
    padding: 0;
    margin-top: 4px;
}
#features .header {
    background-color: #272822;
    color: #fd971f;
    color: #F8F8F2;
    text-align: center;
    /* border-bottom: 1px solid grey; */
    border-right: 1px solid grey;
}
#features .tc {
    color: #F8F8F2;
    text-align: center;
}
#features ul {
    text-align: left;
    display: inline-block;
}

"""

def fcode(func):
    s = inspect.getsource(func)
    s = s.replace("\n    ", "\n")
    s = "\n".join(s.splitlines()[1:])
    pre(code(s))

def f1():
    with table(class_="striped"):
        tr(th("n"), th("squared"))
        for n in range(1, 6):
            with tr():
                td(n)
                td(n * n)

f1.html = """
<table class="striped">
    <tr>
        <th>n</th>
        <th>squared</th>
    </tr>
    <tr>
        <td>1</td>
        <td>1</td>
    </tr>
    <tr>
        <td>2</td>
        <td>4</td>
    </tr>
    <tr>
        <td>3</td>
        <td>9</td>
    </tr>
    ...
</table>""".strip()

# pre(code(hypergen(func, settings=dict(indent=True))))

def feature(func):
    with div(class_="grid3"):
        div(h4("Hypergen"), class_="header")
        div(h4(""), class_="header")
        div(h4("HTML"), class_="header")

    with div(class_="grid3"):
        with div(class_="cell"):
            fcode(func)

        with div(class_="cell tc"):
            with div():
                h2("Write HTML in pure python")
                p("Built your templates in a real language with:")
                with ul():
                    li("functions")
                    li("modules & packages")
                    li("conditionals")
                    li("loops")
                    li("with statements")
                    li("djangos ORM")
                    li("...")
                div("", style=dict(height="60px"))

        with div(class_="cell"):
            with pre(), code():
                write(func.html)

        # with div(class_="cell nc"):
        #     func()

def features_template():
    link("https://highlightjs.org/static/demo/styles/base16/monokai.css")
    style(STYLE)
    with div(id="features"):
        h2("Features")
        feature(f1)

    # with div(id="features"):
