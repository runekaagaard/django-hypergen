from datetime.datetime import now
d = dict

from hypergen.core import context as c, namespace as ns
from hypergen.core import *


@route(
    # Auto namespace various concerns.
    namespace=d(params="mini", id_="mini", class_="", route="mini"),
    # Default query parameters. Can be a dict or a callable.
    params=lambda: d(year=now().year))
def minidash(year=None):
    """
    Mini dashboard overlayed on all pages.

    Parameters will display namedspaced in the url, the route as "mini_route":

        /main/app/page/mini/?mini_page=1&mini_status=new&mini_year=2020&mini_route=pretty

    """

    @route("pretty", parent=minidash)
    def graphs():
        div(id_="graph")
        # Runs a javascript command with graph data.
        command([
            "graphlib",
            "render",
            [ns("graph"), someapi.get_graph_data()],
        ])

    # Params are still namedspaced in the "mini_" namespace.
    @route(parent=minidash, params=dict(status="completed", page=0))
    def log(status=None):
        items = Item.objects.filter(status=c.params.status)
        # The "ul.e" function is short for enumerate.
        ul(
            li.r(a.r("Show completed", href=(log, "completed"))),
            li.r(a.r("Show done", href=(log, "done"))), )
        for item in ul.e(Paginate(items, page=c.params.page)):
            li(item.date, item.text)

    # Magic function that makes innner functions decorated with e.g. @route, available from the outside.
    # It must be called after the last inner function and before the body of the function. It works by raising
    # a custom exception when a custom context variable is set.
    make_nestable()

    # Id's are prefixed with "mini-" from the namespace. In this instance classes are not prefixed.
    with div.c(id_="content", class_="card"):
        # Urls uses pushstate and have backbutton support.
        a("graphs", href=graphs)
        a("log", href=log)
        minidash.route_children(default=graphs)
        a("-", href=(minidash, c.params.year - 1))
        a("+", href=(minidash, c.params.year + 1))

    timeout((minidash, year), 500)


@permission_required("dashboard.fulldash")
def fulldash():
    """Master dashboard on a single page"""
    div(id_="graph")
    update_client_state("graph", someapi.get_all_graph_data())
    command(["graphlib", "render", ["graph", client_state("graph")]])
