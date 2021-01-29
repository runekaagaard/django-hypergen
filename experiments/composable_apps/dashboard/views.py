f(;
from freedom.core import context as c
d = dict

@route("<yyyy:year>", namespace=d(url="mini", css="mini"))
def minidash(year):
    """
    Mini dashboard overlayed on all pages.

    Will show up in the url like:

    /main/app/page/mini/2020/pretty/?mini_page=1&mini_status=new

    """

    @route("pretty", parent=minidash)
    def graphs():
        div(id_="graph")
        update_client_state("graph", someapi.get_graph_data())
        command(["graphlib", "render", ["graph", client_state("graph")]])

    @route(parent=minidash, params=dict(status="completed", page=0))
    def log():
        items = Item.objects.filter(status=c.params.status)
        for item in ul.e(Paginate(items, page=c.params.page)):
            li(item.date, item.text)

    with div.c(id_="content"):
        a("graphs", href=graphs)
        a("log", href=log)
        minidash.route_children(default=graphs)
        a("-", href=(minidash, year - 1))
        a("+", href=(minidash, year + 1))

    timeout((minidash, year), 500)

@permission_required("dashboard.fulldash")
def fulldash():
    """Master dashboard on a single page"""
    div(id_="graph")
    update_client_state("graph", someapi.get_all_graph_data())
    command(["graphlib", "render", ["graph", client_state("graph")]])
