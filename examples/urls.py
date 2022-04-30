from django.contrib import admin
from django.urls import path, include

import hypergen.urls

import website.urls
import todomvc.urls
import inputs.urls
import gameofcython.urls
import djangotemplates.urls
import hellohypergen.urls
import hellocoreonly.urls
import hellocoreonly2.urls
import t9n.urls
import notifications.urls
import commands.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(website.urls, namespace="site")),
    path('hypergen/', include(hypergen.urls, namespace="hypergen")),
    path('todomvc/', include(todomvc.urls, namespace="todomvc")),
    path('inputs/', include(inputs.urls, namespace="inputs")),
    path('gameofcython/', include(gameofcython.urls, namespace="gameofcython")),
    path('djangotemplates/', include(djangotemplates.urls, namespace="djangotemplates")),
    path('hellohypergen/', include(hellohypergen.urls, namespace="hellohypergen")),
    path('hellocoreonly/', include(hellocoreonly.urls, namespace="hellocoreonly")),
    path('hellocoreonly2/', include(hellocoreonly2.urls, namespace="hellocoreonly2")),
    path('t9n/', include(t9n.urls, namespace="t9n")),
    path('notifications/', include(notifications.urls, namespace="notifications")),
    path('commands/', include(commands.urls, namespace="commands")),]
