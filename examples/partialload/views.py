from hypergen.imports import *
from website.templates2 import base_example_template, show_func, show_sources

@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def page1(request):
    h2("Example: Welcome to page 1")
    p("Try out how partial loading and browser back/forward buttons works automatically between theses pages.")
    a("page2", href=page2.reverse(), id_="page2")
    a("page3", href=page3.reverse(), id_="page3")
    p("Check the js console to see which frontend commands are being executed!")

    template()

@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def page2(request):
    h2("Example: Welcome to page 2")
    p("Try out how partial loading and browser back/forward buttons works automatically between theses pages.")
    a("page1", href=page1.reverse(), id_="page1")
    a("page3", href=page3.reverse(), id_="page3")
    p("Check the js console to see which frontend commands are being executed!")

    template()

@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def page3(request):
    h2("Example: Welcome to page 3")
    p("Try out how partial loading and browser back/forward buttons works automatically between theses pages.")
    a("page1", href=page1.reverse(), id_="page1")
    a("page2", href=page2.reverse(), id_="page2")
    p("Check the js console to see which frontend commands are being executed!")

    template()

def template():
    h2("Partial loading with history support")
    p(
        "A common pattern in Hypergen is to have multiple @liveviews sharing the same base_template. ",
        "Hypergen will automatically detect <a> tags linking between views with the same base template and perform a partial load with browser history support."
    )
    p("It might look like this:")
    pre(
        code("""
@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def page1(request):
    h2("Welcome to page 1")
    a("page2", href=page2.reverse(), id_="page2")
        
@liveview(perm=NO_PERM_REQUIRED, base_template=base_example_template)
def page2(request):
    h2("Welcome to page 2")
    a("page1", href=page1.reverse(), id_="page1")
    """.strip()))

    p("It's required to use the", code("myview.reverse()"), "pattern provided by the autourls functionality.",
        "Autourls adds metadata to the string so hypergen knows if the two views have the same base template.",
        sep=" ")
    p("For partial loading to work this argument is required:")
    dl(
        dt("base_template"),
        dd("This base template is wrapped around the hypergen view. It should be a contextmanager callable",
        " and the hypergen view will be called where the base template yields."),
    )
    p("In our example the base_template looks like this:")
    show_func(base_example_template)
    pre(code("base_example_template.target_id = 'content'"))

    p("The id from", code('with div(id_="content"):'),
        "should match the target_id set as an attribute to the base template.", sep=" ")

    h2("Partial loading and custom javascript")
    p("If you are running custom javascript that must act on the html inside the content div that javascript ",
        "must be triggered manually after each partial reload. This can be done in two ways.")

    p("1. Use the", code("{partial:true}"), "setting to hypergen.ready():", sep=" ")
    pre(code("hypergen.ready(myInitFunc, {partial: true})"))
    p("Then your custom javascript code will be run both on page load and on partial loads.")

    p("2. Listen to the", code("hypergen.pushstate"), "signal:", sep=" ")
    pre(code('document.addEventListener("hypergen.pushstate", myInitFunc)'))

    show_sources(__file__)
