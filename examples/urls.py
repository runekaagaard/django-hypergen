from django.contrib import admin
from django.urls import path, include

from . import hypergen.urls

from . import todomvc.urls
from . import inputs.urls
from . import gameofcython.urls
from . import djangotemplates.urls
from . import hellohypergen.urls
from . import t9n.urls

from .home import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hypergen/', include(hypergen.urls, namespace="hypergen")),
    path('', home),
    path('todomvc/', include(todomvc.urls, namespace="todomvc")),
    path('inputs/', include(inputs.urls, namespace="inputs")),
    path('gameofcython/', include(gameofcython.urls, namespace="gameofcython")),
    path('djangotemplates/', include(djangotemplates.urls, namespace="djangotemplates")),
    path('hellohypergen/', include(hellohypergen.urls, namespace="hellohypergen")),
    path('t9n/', include(t9n.urls, namespace="t9n")),]
