# Simple


@route("page/section/<yyyy:year>")
def section(arg1):
    h1("Velcome to section for the year ", context.url.year)


@route("page/overview")
def overview(arg1):
    h1("Velcome to the overview")


def page():
    with div.c():
        a("Go to subsection", href=(section, 1998))
        a("Go to overview", href=overview)
        context.get("route", section)(92)


@permission_required("app:perm")
def app(request):
    return hypergen(page, routes)


# Nested
"""
packages, modules and functions are the building blocks of an url. Consider the folder structure:

    mypackage1
        __init__.py
            hypergen_route = "prettyname/<yyyy:year>/<float>"
            hypergen_route_params = dict(page=0, sorted=True, q="") 
        mymodule1.py
            CONTENT BELOW
        ...
    mypackage2
"""
from freedom.hypergen import route

hypergen_route = "modulename/<myapp.MyModel:obj>"
hypergen_route_params = dict(q="Custom Q")


@route("<float:percent>")
def myfunc():
    @route("pathname1", parent=myfunc)
    def innerfunc1():
        pass

    @route("funky/<int:boo>", parent=myfunc)
    def innerfunc2(boo=72):
        pass

    myfunc.route_children()


def my_content_template():
    a("Funky guy!",
      href=("mypackage1.mymodule1.myfunc.innerfunc2", 1992, 5.3,
            MyModel.objects.get(pk=10), 900))


@permssion_required("foo.bar")
def myapp(request):
    return hypergen()
