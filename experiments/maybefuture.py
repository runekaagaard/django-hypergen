def wrap3(dfunc):
    """
    A a decorator decorator, allowing the decorator to be used as:
        @decorator(with, arguments, and=kwargs)
    or
        @decorator

    It does not work for a wrapped function that takes a callback as the only input.

    It looks like this:

        @wrap3
        def mydecorator(func, fargs, fkwargs, *dargs, **dkwargs):
            print "Decorator args, kwargs are", dargs, dkwargs
            func(*fargs, **fkwargs)


        @mydecorator
        def myfunc(x, y=19):
            return x + y


        @mydecorator(42, foo=True)
        def myfunc2(x, y=19):
            return x + y
    """
    def _(*xargs, **xkwargs):
        if len(xargs) == 1 and len(xkwargs) == 0 and callable(xargs[0]):
            # Without decorator args, kwargs.
            func = xargs[0]

            @wraps(func)
            def __(*fargs, **fkwargs):
                dfunc(func, fargs, fkwargs)

            return __
        else:
            # With decorator args, kwargs.
            dargs, dkwargs = xargs, xkwargs

            def __(func):
                @wraps(func)
                def ___(*fargs, **fkwargs):
                    return dfunc(func, fargs, fkwargs, *dargs, **dkwargs)

                return ___

            return __

    return _

class SkipException(Exception):
    pass

@contextmanager
def skippable():
    try:
        yield
    except SkipException:
        pass

@contextmanager
def skip(when):
    if when:
        raise SkipException()
    else:
        yield

class adict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name] if type(self[name]) is not dict else adict(self[name])
        else:
            raise AttributeError("No such attribute: " + name)

    def __getitem__(self, name):
        value = super(adict, self).__getitem__(name)
        return value if value is not dict else adict(value)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
