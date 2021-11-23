# coding=utf-8
from django.apps import AppConfig

class Hypergen(AppConfig):
    name = 'hypergen'
    verbose_name = u"Hypergen"

    def ready(self):
        from hypergen.core import load_translations
        load_translations()
