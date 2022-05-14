Hypergen template engine
========================

Hypergen features a react-like templating engine in pure python. Import everything like this::

    from hypergen.core import *

HTML elements
-------------

All HTML5 tags can be called like functions::

    p("Hello Hypergen", class_="foo") # <p class="foo">Hello Hypergen</p>

They all inherit the ``base_element`` class.

*base_element(*children, sep=None, coerce_to=None, js_value=None, js_coerce_func=None, **attributes)*
    Arguments becomes children inside the tag. Keyword arguments becomes attributes.
sep
    Joins arguments by this separator. ``div("a", "b", sep=", ")`` becomes ``<div>a, b</div>``.
coerce_to, js_values, js_coerce_func
    See `Form Input elements </inputs/>`_

Children
~~~~~~~~

Arguments to HTML elements have several convinience features, consider::

    section(
        [1, 2, 3],
        (x for x in [4, 5, 6]),
        7,
        lambda: 8,
        b(9),
        sep=" ",
    )

Which will yield the following html::

    <section>1 2 3 4 5 6 7 <b>9</b></section>

We can see that arguments can be:

iterables
    Things that look like an iterable will be extended into the HTML.
non-strings
    Hypergen will try to convert stuff to strings.
callables
    The return of a callable will be appended to the HTML.
other elements
    HTML elements are nestable.

Attributes
~~~~~~~~~~

Likewise attributes have several quality of life improvements::

    div(
        a=OMIT,
        b=lambda: 1,
        c=True,
        d=False,
        e=None,
        style={"background_color": "green"},
        class_=["p1", "p2", "p3"],
        id_=("mymodel", "42")
    )

Which gives this HTML::

    <div b="1"
         c
         style="background-color: green;"
         class="p1 p2 p3"
         id="mymodel-42">
    </div>

We understand that:

a value of OMIT, False, None
    Will not create an attribute
style
    Parse a dict to generate css. Underscores in keys are converted to dashes. A string is also supported.
class
    Items of an iterable will be joined by " ". A string is also supported.
id\_
    Items of an iterable will be joined by "-". A string is also supported.
trailing underscores
     are removed to allow for python keywords like ``class``.

    
Composition
-----------

Base templates
~~~~~~~~~~~~~~

Higher order functions
~~~~~~~~~~~~~~~~~~~~~~

Helpers
-------

write
~~~~~

raw
~~~

rst
~~~

t
~

command
~~~~~~~

callback
~~~~~~~~

call_js
~~~~~~~

THIS
~~~~

OMIT
~~~~

is_ajax
~~~~~~~

@component
~~~~~~~~~~

Callbacks
=========

Value binding
=============

Serialization
=============

Life cycle
==========
