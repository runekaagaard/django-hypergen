from hypergen.core import *
from hypergen.contrib import hypergen_view, NO_PERM_REQUIRED

from website.templates import base_example_template, show_func, show_sources

@hypergen_view(perm=NO_PERM_REQUIRED, base_template=base_example_template, target_id="content")
def page1(request):
    h2("Welcome to page 1")
    p("Try out how partial loading and browser back/forward buttons works automatically between theses pages.")
    a("page2", href=page2.reverse(), id_="page2")
    a("page3", href=page3.reverse(), id_="page3")
    template()

@hypergen_view(perm=NO_PERM_REQUIRED, base_template=base_example_template, target_id="content")
def page2(request):
    h2("Welcome to page 2")
    p("Try out how partial loading and browser back/forward buttons works automatically between theses pages.")
    a("page1", href=page1.reverse(), id_="page1")
    a("page3", href=page3.reverse(), id_="page3")
    template()

@hypergen_view(perm=NO_PERM_REQUIRED, base_template=base_example_template, target_id="content")
def page3(request):
    h2("Welcome to page 3")
    p("Try out how partial loading and browser back/forward buttons works automatically between theses pages.")
    a("page1", href=page1.reverse(), id_="page1")
    a("page2", href=page2.reverse(), id_="page2")
    template()

def template():
    h2("Partial loading with history support")
    p(
        "A common pattern in Hypergen is to have multiple @hypergen_views sharing the same base_template. ",
        "Hypergen will automatically detect <a> tags linking between views with the same base template and perform a partial load with browser history support."
    )
    p("It might look like this:")
    pre(
        code("""
@hypergen_view(perm=NO_PERM_REQUIRED, base_template=base_example_template, target_id="content")
def page1(request):
    h2("Welcome to page 1")
    a("page2", href=page2.reverse(), id_="page2")
        
@hypergen_view(perm=NO_PERM_REQUIRED, base_template=base_example_template, target_id="content")
def page2(request):
    h2("Welcome to page 2")
    a("page1", href=page1.reverse(), id_="page1")
    """.strip()))

    p("For partial loading to work these arguments are required:")
    dl(
        dt("base_template"),
        dd("This base template is wrapped around the hypergen view. It should be a contextmanager callable",
        " and the hypergen view will be called where the base template yields."), dt("target_id"),
        dd("Just around where the hypergen_view is yielded it must be wrapped with a div with this id.",
        " This makes hypergen understand into which html element to write the partial content."))
    p("In our example the base_template looks like this:")
    show_func(base_example_template)

    p("The id from", code('with div(id_="content"):'), "should match the target_id set in the views.", sep=" ")
    p("Check the js console to see which frontend commands are being executed!")

    show_sources(__file__)
