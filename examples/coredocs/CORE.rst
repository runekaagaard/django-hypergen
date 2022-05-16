Hypergen template engine
========================

Hypergen features a react-like templating engine in pure python. Import everything like this::

    from hypergen.core import *

The function that makes everything works is ``hypergen()``. It constructs a global context that collects invocations of html5 elements like ``div("hi")``. If you are using the ``@hypergen_view`` and ``@hypergen_callback`` from contrib you might not use it directly, but it's still called under the hood.

*hypergen(template_function, *args, **kwargs)*
    Calls the template_function with ``args`` and ``kwargs`` as arguments. Collects html and returns either:
*normal http requests*
    Returns html as a string.
*ajax requests*
    Returns a list of commands for the frontend to execute that re-renders to the correct ``target_id``.

So the most basic Django view using hypergen would look like this::

    def my_view(request):
        return HttpResponse(hypergen(my_template, "hypergen"))

    def my_template(name):
        doctype()
        with html():
            with body():
                p("Hello ", name)

Html elements
-------------

All html5 tags can be called like functions::

    p("Hello Hypergen", class_="foo") # <p class="foo">Hello Hypergen</p>

They all inherit the ``base_element`` class.

*base_element(*children, sep=None, coerce_to=None, js_value=None, js_coerce_func=None, **attributes)*
    Arguments becomes children inside the tag. Keyword arguments becomes attributes.
sep
    Joins arguments by this separator. ``div("a", "b", sep=", ")`` becomes ``<div>a, b</div>``.
end
    Insert this string at the end.
coerce_to, js_values, js_coerce_func
    See `Form Input elements </inputs/>`_

Html elements can take other elements as input and can be nested with the ``with`` statement. These two examples will produce the same html::

    ul(li(1), li(2), li(3))

and::

    with ul():
        li(1)
        li(2)
        li(3)

Though it can be written more elegantly::

    ul(li(x) for x in range(1, 4))

Children
~~~~~~~~

Arguments to html elements becomes children to the html tag. They have several convinience features, consider::

    section(
        [1, 2, 3],
        (x for x in [4, 5, 6]),
        7,
        lambda: 8,
        b(9),
        sep=" ",
        end=".",
    )

Which will yield the following html::

    <section>1 2 3 4 5 6 7 <b>9</b>.</section>

We can see that arguments can be:

iterables
    Things that look like an iterable will be extended into the html.
non-strings
    Hypergen will try to convert stuff to strings.
callables
    The return of a callable will be appended to the html.
other elements
    html elements are nestable.

Attributes
~~~~~~~~~~

Keyword arguments to html elements becomes attributes in the html tag.

.. raw:: html
         
    <p>
        Html attributes that clashes with python keywords or builtins can be set by postfixing the name with an underscore.
        <mark>The names <tt>type_</tt> and <tt>id_</tt> MUST be postfixed with an underscore for hypergen to work
            correctly!
        </mark>This will soon change.
    </p>

Likewise, attributes have several quality of life improvements::

    div(
        a=OMIT,
        b=True,
        c=False,
        d=None,
        style={"background_color": "green"},
        class_=["p1", "p2", "p3"],
        id_=("mymodel", "42")
    )

Which gives this html::

    <div
         b
         style="background-color: green;"
         class="p1 p2 p3"
         id="mymodel-42">
    </div>

We understand that:

a value of OMIT, False, None
    Will not create an attribute
style
    Takes a string or a dict. Underscores in the dicts keys are converted to dashes.
class
    Takes a string or an iterable. Items of an iterable will be joined by a space. Tip: Use sets.
id\_
    Takes a string or an iterable. Items of an iterable will be joined by a dash.
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
