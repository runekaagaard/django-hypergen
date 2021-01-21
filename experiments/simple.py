# Local Variables:
# flymake-mode: nil
# End:
# yapf: disable

from hypergen import hypergen, dom, State
from hypergen.elements import *

from myapp import db, auth


def render_login(state):
    def submit(request, form_data):
        if request.user.is_logged_in:
            auth.logout(request.user)

        is_ok = auth.login(form_data.email, form_data.password)
        if is_ok:
            dom.redirect(list_movies.reverse())
        else:
            state.errors.append("Invalid email or password")

    with form(validators=[validators.no_duplicate_values],
              onchange=validators.validate):
        errors(state.errors)

        label("Email")
        errors(state.email.errors)
        input_(value=state.email, type_="email", validators=[
            validators.no_gmail_account])

        label("Password")
        errors(state.password.errors)
        input_(value=state.password, type_="password", required=True)

        button("Login", onclick=submit)

def errors(errors):
    with ul(when=errors, _class="errors"):
        [li(x) for x in errors]

@path("auth/login")
def login(request):
    state = State(errors=[], password="1234")
    return Response(hypergen(render_login, state))

@path("movies/list")
@hypergen
def list_movies(request):
    def update_my_rating(form_data):
        if 0 <= form_data.my_rating <= 100:
            db.update_rating(movie_id=form_data.meta["id"],
                             my_rating=form_data.my_rating)
        else:
            form_data.my_rating.errors.append("Must be between 0 and 100.")

    state = State(movies=db.get_movies())
    columns = ("Title", "Year", "My rating")
    with table():
        with thead(), tr():
            [th(x) for x in columns]
        with tbody():
            for movie in state.movies:
                with tr(), form(meta={"id": movie.id}):
                    td(movie.title)
                    td(movie.year)

                    errors(movie.my_rating.errors)
                    with td():
                        input_(value=movie.my_rating,
                               onchange=update_my_rating, type_="number")


"""
<table>
    <tr><th>Title</th><th>Year</th><th>My rating</th></tr>
    <tr>
        <td>The Matrix</t>
        <td>1999</td>
        <td>
            <form id="10">
                <input type="number" value=100
                    onchange='send("myapp.views.list_movies|update_my_rating", 10)'
                />
            </form>
        </td>
    </tr>
</table>
"""
