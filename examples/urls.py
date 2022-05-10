from django.contrib import admin

try:
    from django.conf.urls import url, include
except ImportError:
    from django.urls import re_path as url, include
import hypergen.urls

import website.urls
import todomvc.urls
import inputs.urls
import gameofcython.urls
import djangotemplates.urls
import hellohypergen.urls
import hellocoreonly.urls
import hellocoreonly2.urls
import hellomagic.urls
import t9n.urls
import notifications.urls
import partialload.urls
import commands.urls
import gettingstarted.urls

import globalcontext.urls
import djangolander.urls
import motherofall.urls

urlpatterns = [
    url('^admin/', admin.site.urls),
    url('', include(website.urls, namespace="site")),
    url('^hypergen/', include(hypergen.urls, namespace="hypergen")),
    url('^todomvc/', include(todomvc.urls, namespace="todomvc")),
    url('^inputs/', include(inputs.urls, namespace="inputs")),
    url('^gameofcython/', include(gameofcython.urls, namespace="gameofcython")),
    url('^djangotemplates/', include(djangotemplates.urls, namespace="djangotemplates")),
    url('^hellohypergen/', include(hellohypergen.urls, namespace="hellohypergen")),
    url('^hellocoreonly/', include(hellocoreonly.urls, namespace="hellocoreonly")),
    url('^hellocoreonly2/', include(hellocoreonly2.urls, namespace="hellocoreonly2")),
    url('^gettingstarted/', include(gettingstarted.urls, namespace="gettingstarted")),
    url('^djangolander/', include(djangolander.urls, namespace="djangolander")),
    url('^motherofall/', include(motherofall.urls, namespace="motherofall")),
    url('^hellomagic/', include(hellomagic.urls, namespace="hellomagic")),
    url('^t9n/', include(t9n.urls, namespace="t9n")),
    url('^notifications/', include(notifications.urls, namespace="notifications")),
    url('^partialload/', include(partialload.urls, namespace="partialload")),
    url('^commands/', include(commands.urls, namespace="commands")),
    url('^globalcontext/', include(globalcontext.urls, namespace="globalcontext")),]
