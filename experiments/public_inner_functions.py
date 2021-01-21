from functools import wraps

def ipub(outer):
    """
    Decorate an inner function to make it public to the outside.
    """
    @wraps(outer)
    def _(inner):
        setattr(outer, inner.__name__, inner)
        return inner

    return _

def a(x):
    @ipub(a)
    def b(x):
        @ipub(b)
        def c(x):
            return x ** x

        return x * x
    
    return x + x 
    
print a(4)
print a.b(4)
print a.b.c(4)
