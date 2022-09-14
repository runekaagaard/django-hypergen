from itertools import groupby

from django.db import models
from django.utils.formats import date_format
from django.contrib.auth.models import User

def full_name(user):
    return f"{user.first_name} {user.last_name}"

class Doctor(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Doctor id={self.pk} name="{self.name}">'

class Timeslot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="+")
    booked_to = models.ForeignKey("auth.User", on_delete=models.CASCADE, default=None, null=True, related_name="+")

    def __str__(self):
        return self.fmt_datetime

    def __repr__(self):
        d1 = str(self.start)[:16]
        d2 = str(self.end)[:16]
        booked_to = f' booked_to="{full_name(self.booked_to)}"' if self.booked_to else " booked_to=None"

        return f'<Timeslot id={self.pk} start="{d1}" end="{d2}" doctor="{self.doctor.name}"{booked_to}>'

    @property
    def fmt_datetime(self):
        return date_format(self.start, format='Y-m-d H:i') + " – " + date_format(self.end, "H:i")

    @property
    def fmt_time(self):
        return date_format(self.start, format='H:i') + " – " + date_format(self.end, "H:i")

    @staticmethod
    def free_by_date(query=None):
        timeslots = Timeslot.objects.filter(booked_to=None).order_by("start")
        if query:
            timeslots = timeslots.filter(doctor__name__icontains=query)

        return [[k, list(v)] for k, v in groupby(timeslots, key=lambda x: x.start.date())]

    @staticmethod
    def book(request, timeslot_id):
        user = User.objects.first()  # Cheat to avoid allow anonymous access.
        Timeslot.objects.filter(pk=timeslot_id).update(booked_to=user)

    @staticmethod
    def cancel(request, timeslot_id):
        Timeslot.objects.filter(pk=timeslot_id).update(booked_to=None)
