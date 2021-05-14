from django.contrib import admin
from django.urls import path, include

import todomvc.urls
import inputs.urls
import gameofcython.urls
import djangotemplates.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todomvc/', include(todomvc.urls, namespace="todomvc")),
    path('inputs/', include(inputs.urls, namespace="inputs")),
    path('gameofcython/', include(gameofcython.urls, namespace="gameofcython")),
    path('djangotemplates/', include(djangotemplates.urls, namespace="djangotemplates")),]
