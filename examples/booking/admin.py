from django.contrib import admin
from booking.models import Timeslot

@admin.register(Timeslot)
class TimeslotAdmin(admin.ModelAdmin):
    list_display = ("pk", "start", "end", "doctor", "booked_to")
    pass
