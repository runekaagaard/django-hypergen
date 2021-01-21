# yapf: disable
class element(object):
    # Decorator withput ().
    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and callable(args[0]) and not kwargs:
            return cls()(args[0])
        else:
            return super(element, cls).__new__(cls, *args, **kwargs)

    def __init__(self, *texts, **attributes):
        # There are texts, so we are calling as a function.
        print "INIT"
        if texts:
            print self.tag, attributes
            for text in texts:
                print text
            print self.etag
        else:
            self.attributes = attributes

    # Hello context manager "with" invocation.
    def __enter__(self):
        print self.tag, self.attributes
    def __exit__(self, type, value, traceback):
        print self.etag

    # What, as a decorator?!
    def __call__(self, func):
        def _(*args, **kwargs):
            print self.tag, self.attributes
            func(*args, **kwargs)
            print self.etag

        return _

class div(element):
    tag = "<div>"
    etag = "</div>"

print
div("A", class_="funk")

print
with div(class_="y"):
    print "B"

print
@div(class_="town")
def foo(x):
    print "C", x
foo(42)

print
@div
def bar(x):
    print "D", x

bar(91)

print
div(class_="clearfix")
