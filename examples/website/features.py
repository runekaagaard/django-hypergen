from contextlib import contextmanager
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
    border-right: 1px solid grey;
    height: calc(500px - 16px * 2)
}
#features .cell .inner {
    height: calc(100% - 35px);
    display: flex;
    justify-content: center;
    align-items: center;
}
#features .cell .inner-full {
    height: calc(100%);
    display: flex;
    justify-content: center;
    align-items: center;
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
    height: 35px;
    /* border-bottom: 1px solid grey; */
    /* border-right: 1px solid grey; */
}
#features .tc {
    color: #F8F8F2;
    text-align: center;
}
#features ul {
    text-align: left;
    display: inline-block;
}
.nul {
    text-decoration: none !important;
    
    font-weight: bold;
    margin-right: 8px;
    display: inline-block;
}
.nul:hover {
    text-decoration: underline !important;
}
#features code {
    -ms-overflow-style: none;  /* Internet Explorer 10+ */
    scrollbar-width: none;  /* Firefox */
}
#features code::-webkit-scrollbar { 
    display: none;  /* Safari and Chrome */
}
#features .tc *:first-child {
    margin-top: 0;
    padding-top: 0;
}
#features .tc *:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
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
        for n in range(1, 4):
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
</table>""".strip()

# pre(code(hypergen(func, settings=dict(indent=True))))

@contextmanager
def cell(title):
    with div(class_="cell"):
        div(h4(title), class_="header")
        with div(class_="inner"):
            yield

def feature(func):
    with div(class_="grid3"):
        with cell("Hypergen"):
            fcode(func)

        with div(class_="cell tc"):
            with div(class_="inner-full"), div():
                h2("Write HTML in pure python")
                p("Build templates in a turing complete language:")
                with ul():
                    li("functions")
                    li("modules & packages")
                    li("conditionals")
                    li("loops")
                    li("with statements")
                    li("djangos ORM")
                    li("...")
                # div("", style=dict(height="60px"))

        with div(class_="cell"):
            div(h4("HTML"), class_="header")
            with div(class_="inner"):
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
    with div():
        # a("⟪", href="1", class_="selected")
        # a("⟫", href="2", class_="selected")
        a("🢨", href="1", class_="selected nul")
        a("🢩", href="2", class_="selected nul")
        small("1 of 27", style=dict(float="right"))

    # with div(id="features"):
