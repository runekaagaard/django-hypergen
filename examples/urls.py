from django.contrib import admin

try:
    from django.conf.urls import url, include
except ImportError:
    from django.urls import re_path as url, include

import website.urls
import todomvc.urls
import inputs.urls
import gameofcython.urls
import djangotemplates.urls
import hellohypergen.urls
import hellocoreonly.urls
import hellomagic.urls
import notifications.urls
import partialload.urls
import commands.urls
import gettingstarted.urls
import globalcontext.urls
import apptemplate.urls
import coredocs.urls
import kitchensink.urls
import misc.urls
import booking.urls
import websockets.urls
import features.urls

urlpatterns = [
    url('^admin/', admin.site.urls),
    url('', include(website.urls, namespace="site")),
    url('^todomvc/', include(todomvc.urls, namespace="todomvc")),
    url('^inputs/', include(inputs.urls, namespace="inputs")),
    url('^gameofcython/', include(gameofcython.urls, namespace="gameofcython")),
    url('^djangotemplates/', include(djangotemplates.urls, namespace="djangotemplates")),
    url('^hellohypergen/', include(hellohypergen.urls, namespace="hellohypergen")),
    url('^hellocoreonly/', include(hellocoreonly.urls, namespace="hellocoreonly")),
    url('^gettingstarted/', include(gettingstarted.urls, namespace="gettingstarted")),
    url('^hellomagic/', include(hellomagic.urls, namespace="hellomagic")),
    url('^notifications/', include(notifications.urls, namespace="notifications")),
    url('^partialload/', include(partialload.urls, namespace="partialload")),
    url('^commands/', include(commands.urls, namespace="commands")),
    url('^globalcontext/', include(globalcontext.urls, namespace="globalcontext")),
    url('^apptemplate/', include(apptemplate.urls, namespace="apptemplate")),
    url('^coredocs/', include(coredocs.urls, namespace="coredocs")),
    url('^kitchensink/', include(kitchensink.urls, namespace="kitchensink")),
    url('^misc/', include(misc.urls, namespace="misc")),
    url('^booking/', include(booking.urls, namespace="booking")),
    url('^websockets/', include(websockets.urls, namespace="websockets")),
    url('^features/', include(features.urls, namespace="features")),]
