from hypergen.context import context
from contextlib import contextmanager
import pickle

class AppstatePlugin:
    def __init__(self, namespace, appstate):
        self.namespace = namespace
        self.appstate = appstate

    @contextmanager
    def context(self):
        k = "hypergen_appstate_{}".format(self.namespace)
        appstate = context.request.session.get(k, None)
        if appstate is not None:
            appstate = pickle.loads(appstate.encode('latin1'))
        else:
            appstate = self.appstate()
        with context(appstate=appstate):
            yield
            context.request.session[k] = pickle.dumps(context.appstate, pickle.HIGHEST_PROTOCOL).decode('latin1')
