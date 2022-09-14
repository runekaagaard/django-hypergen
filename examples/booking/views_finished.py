from contextlib import contextmanager

from django.http.response import HttpResponse

from hypergen.imports import *
from hypergen.plugins.alertify import AlertifyPlugin

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.templatetags.static import static

from booking.models import Timeslot

### Templates ###

@contextmanager
def base_template():
    doctype()
    with html():
        with head():
            link(href=static("chota.css"))
            title("Doctor booking")
        with body():
            with div(class_="container"):
                h1("Doctor booking")
                with div(id_="target"):
                    yield

base_template.target_id = "target"

def free_template(timeslots_by_date):
    menu()
    with p():
        input_(placeholder="Search here", id_="search", oninput=callback(search, THIS, debounce=50))
    with table():
        thead(tr(th(x) for x in ["Date", "Time", "Doctor", "Action"]))
        for date, timeslots in timeslots_by_date:
            tr(th(date, colspan=4))
            for timeslot in timeslots:
                with tr():
                    td()
                    td(timeslot.fmt_time)
                    td(timeslot.doctor)
                    with td():
                        button("Book", id_=["timeslot", timeslot.pk], class_="button primary",
                               onclick=callback(book, timeslot.pk))

def menu():
    with nav(class_="tabs nav-center"):
        a("Book timeslot", href=free.reverse(), class_active="active")
        a("My bookings", href=booked.reverse(), class_active="active")

@contextmanager
def row():
    with div(class_="row"):
        yield

@contextmanager
def col(n):
    with div(class_=f"col-{n}"):
        yield

@contextmanager
def card(title, description):
    with div(class_="card"):
        header(h4(title))
        p(description)
        with footer(class_="is-right"):
            yield

### Liveviews ###

@liveview(perm="booking.view_booking", base_template=base_template, user_plugins=[AlertifyPlugin()])
def free(request):
    timeslots_by_date = Timeslot.free_by_date()
    free_template(timeslots_by_date)

@liveview(perm="booking.view_booking", base_template=base_template, user_plugins=[AlertifyPlugin()])
def booked(request):
    menu()
    with row():
        for timeslot in Timeslot.objects.filter(booked_to=request.user):
            with col(4), card(timeslot, timeslot.doctor):
                button("Cancel", class_="button error", id_=["timeslot", timeslot.pk],
                       onclick=callback(cancel, timeslot.pk, confirm="Are you sure?"))

### Actions ###

@action(perm="booking.view_booking", target_id="target", user_plugins=[AlertifyPlugin()])
def search(request, query):
    timeslots_by_date = Timeslot.free_by_date(query)
    free_template(timeslots_by_date)

@action(perm="booking.add_booking", target_id="target", user_plugins=[AlertifyPlugin()])
def book(request, pk):
    Timeslot.book(request, pk)
    messages.add_message(request, messages.SUCCESS, "You got it!")

    return HttpResponseRedirect(booked.reverse())

@action(perm="booking.delete_booking", target_id="target", base_view=booked, user_plugins=[AlertifyPlugin()])
def cancel(request, pk):
    Timeslot.cancel(request, pk)
    messages.add_message(request, messages.WARNING, "Your booking is gone forever!")
