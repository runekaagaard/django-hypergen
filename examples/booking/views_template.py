from contextlib import contextmanager

from hypergen.imports import *
from hypergen.plugins.alertify import AlertifyPlugin

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.templatetags.static import static

from booking.models import Timeslot

### Templates ###

@contextmanager
def base_template():
    yield

base_template.target_id = "target"

def free_template(timeslots_by_date):
    pass

### Liveviews ###

@liveview(perm="booking.view_booking", base_template=base_template)
def free(request):
    pass

@liveview(perm="booking.view_booking", base_template=base_template)
def booked(request):
    pass

### Actions ###

@action(perm="booking.view_booking", target_id="target")
def search(request, query):
    pass

@action(perm="booking.add_booking", target_id="target")
def book(request, pk):
    pass

@action(perm="booking.delete_booking", target_id="target")
def cancel(request, pk):
    pass
