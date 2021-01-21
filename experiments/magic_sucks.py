"""
Problem
=======

It's not possible to make one magic element class that fullfils all of the
following:

- Default operation, that adds to global state
- Can be used as arguments to another element, i.e. returning html
- Works as a context manager
- Works as a decorator
- Works as an empty tag with only attributes.

or it's (almost) possible, but it's gonnna complicate the implementation, and
increase the differences to the Cython version. Making porting a template from
Python to Cython more complicated.

Solution
========

Make it explicit whats going on. The default operation should still be adding to
the global state. So, how about:

"""
Element = namedtuple("Element", "texts attrs html")


def div(*texts, **attrs):
    """
    Takes inner texts and attributes and adds html to the global state.
    
    Returns an Element named tuple.
    """
    return element("div", *texts, **attrs)


def div_ret(*texts, **attrs):
    """
    Like div, but does not add to the global state. Use this when using an
    element as argument to another element.
    """
    return element_ret("div", *texts, **attrs)


def div_dec(*texts, **attrs):
    """
    Decorates a function with a div, and wraps elements called inside the
    decorated function. Given texts is added first.
    """
    return element_dec("div", *texts, **attrs)


def div_con(*texts, **attrs):
    """
    Use a div as a context manager. Wraps elements called inside the context.
    Given texts is added first.
    """
    return element_con("div", *texts, **attrs)


"""
To avoid import hell, we make shortcuts of div_ret, div_dec and dic_con on the
div function, like:
"""

div.r = div_ret
div.d = div_dec
div.c = div_con
