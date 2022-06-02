# DONT USE THESE, might go away at anytime!
import pickle
from hypergen.context import context as c

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
