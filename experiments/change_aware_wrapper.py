class ChangeAware(object):
    def __init__(self, data):
        self.in_init = True
        self.data = data
        self.path = [data]
        self.in_init = False

    def __setattr__(self, k, v):
        if k == "in_init" or self.in_init is True:
            object.__setattr__(self, k, v)
        else:
            setattr(self.path[-1], k, v)

    def __setitem__(self, k, v):
        print("Setting", k, v)
        self.path[-1][k] = v

    def __getattr__(self, k):
        return self.path[-1][k]


class X(object):
    y = 1


data = ChangeAware(dict(x=X()))
data.x.y = 1234
print(data.x.y)

#data.foo = 42
#data[3] = 91
#setattr(data, 3, 91)
#print data.foo.changed()


class CA2(object):
    def __init__(self, data):
        self.data = data

    def __getattribute__(self, k):
        print "__getattribute__", k
        if k == "data":
            return self.__dict__["data"]
        else:
            v = object.__getattribute__(self, k)
            if type(v) in (str, int, float, long):
                return v
            else:
                return CA2(v)

    def __getitem__(self, k):
        print "__getitem__", k
        return self.data[k]

    def __setitem__(self, k, v):
        print "__setitem__", k, v
        self.data[k] = v


ca = CA2({1: {2: 3}})
ca[1][2] = 42
print ca.data
