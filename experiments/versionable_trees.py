# Local Variables:
# flymake-check: nil
# End:

from django.db import models
from versiontrees.models import VersionTreeField

class Instructor(models.Model):
    version = VersionTreeField()

    name = models.TextField()

class Actor(models.Model):
    version = VersionTreeField()

    name = models.TextField()

class Movie(models.Model):
    version = VersionTreeField()

    title = models.TextField()
    instructor = models.ForeignKey(Instructor)
    actors = models.Many2ManyField(Actor)

class Release(models.Model):
    version = VersionTreeField()

    movie = models.ForeignKey(Movie)

class TvShow(models.Model):
    version = VersionTreeField(include=["instructor"], exclude=["actors"])

    title = models.TextField()
    instructor = models.ForeignKey(Instructor)
    actors = models.Many2ManyField(Actor)
