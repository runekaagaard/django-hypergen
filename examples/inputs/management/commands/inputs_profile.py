from django.core.management.base import BaseCommand
from inputs.views import inputs
from django.test import Client

def run(c, sort=["time"]):
    for _ in range(1000):
        c.post('/inputs/')

class Command(BaseCommand):
    help = 'inputs benchmark'

    def handle(self, *args, **options):
        c = Client()
        run(c)
