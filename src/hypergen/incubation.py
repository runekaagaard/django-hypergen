# DONT USE THESE, might go away at anytime!
from contextlib import contextmanager
import pickle
from hypergen.template import *
from hypergen.context import context as c
from hypergen.liveview import callback

def pickle_dumps(data):
    return pickle.dumps(data, pickle.HIGHEST_PROTOCOL).decode('latin1')

def pickle_loads(string):
    return pickle.loads(string.encode('latin1'))

class SessionVar:
    def __init__(self, name, default):
        self.name = "hypergen_request_var__" + name
        self.default = default

    def get(self):
        if self.name not in c.request.session:
            return self.default
        else:
            return pickle_loads(c.request.session[self.name])

    def set(self, value):
        c.request.session[self.name] = pickle_dumps(value)
        return value

    def append(self, value):
        tmp = self.get()
        tmp.append(value)
        self.set(tmp)

        return tmp

    def pop(self):
        tmp = self.get()
        tmp2 = tmp.pop()
        self.set(tmp)

        return tmp2

    def __len__(self):
        return len(self.get())

class LiveformPlugin:
    def __init__(self, action_oninput, action_onsubmit, state):
        self.action_oninput = action_oninput
        self.action_onsubmit = action_onsubmit
        self.state = state

    @contextmanager
    def wrap_element_init(self, element, children, attrs):
        if type(element) is input_ and attrs.get("type", None) in ("button", "image", "reset", "submit"):
            assert "name" in attrs
            attrs["onclick"] = callback(self.action_onsubmit, attrs["name"], self.state)
        elif type(element) is button:
            assert "name" in attrs
            attrs["onclick"] = callback(self.action_onsubmit, attrs["name"], self.state)
        elif type(element) in (select, input_, textarea):
            assert "name" in attrs
            attrs["oninput"] = callback(self.action_oninput, self.state)
            self.state[attrs["name"]] = element
        yield

@contextmanager
def liveform(action_oninput, action_onsubmit, init_state=dict):
    state = init_state()
    plugins = [x for x in c.hypergen.plugins]
    plugins.append(LiveformPlugin(action_oninput, action_onsubmit, state))
    with c(at="hypergen", plugins=plugins):
        yield state
