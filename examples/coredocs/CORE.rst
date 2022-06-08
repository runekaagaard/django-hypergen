Hypergen template engine
========================

Hypergen features a react-like templating engine in pure python. All liveview functionality is located in the ``hypergen.template`` module.

Import everything like this::

    from hypergen.template import *

Or TRULY everything::

    from hypergen.imports import *

hypergen()
==========
    
The function that makes everything works is aptly named ``hypergen()``. It constructs a global context that collects invocations of html5 elements like ``div("hi")``. If you are using the ``@liveview`` and ``@action`` decorators from liveview you might not use it directly, but it's still called under the hood.

The most basic Django view using hypergen would look like::

    from hypergen.template import *
    from django.http.response import HttpResponse
    
    def my_view(request):
        return HttpResponse(hypergen(my_template, "hypergen"))

    def my_template(name):
        doctype()
        with html():
            with body():
                p("Hello ", name)

And the full definition reads:
                
*hypergen(func, *args, settings={}, **kwargs)*
    Calls the given template function as ``func(*args, **kwargs)``. Returns the collected HTML as a string.
    Takes a ``settings`` dict.
*settings:*
    - **base_template** (None): Wrap the function with a ``base_template`` contextmanager function. ``func`` runs
      where the base_template yields.
    - **indent** (False): Indent HTML by 4 spaces. Requires ``pip install yattag``.
    - **liveview** (False): Enables the liveview plugin.
    - **action** (False): Enables the action plugin.
    - **target_id** (None): A string passed to the action plugin that makes hypergen render to a specific div on
      the the frontend.
    - **returns** (HTML): One of the ``HTML``, ``COMMANDS`` or ``FULL`` constants defined in the template module.
    - **plugins** ([TemplatePlugin()]): Use your own custom list of plugins.

For normal use you would be interested in the ``base_template`` argument, the rest is mostly for liveview functionality. Different inner templates can share the same base template::

    from contextlib import contextmanager

    @contextmanager
    def my_base_template():
        doctype()
        with html():
            with body():
                yield
                
    def my_view(request):
        return HttpResponse(hypergen(my_template, "hypergen", settings={"base_template": my_base_template}))
    
    def my_template(name):
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

Clashes with python builtins and keywords are mitigated by postfixing a single underscore::

    input_(type_="number", id_="my-input", class_="my-class", value=92)

If you prefer, keyword arguments that matches builtins like ``type``, ``id`` and can of course be used without the postfix.

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

Keyword arguments to html elements becomes attributes in the html tag. Html attributes that clashes with python keywords or builtins can be set by postfixing the name with an underscore.

Likewise, attributes have several quality of life improvements::

    from hypergen.template import OMIT
    
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

Security
~~~~~~~~~~

All children given to elements have html entities escaped, so for instance it's safe to do::

    div(my_obj.my_field_with_user_input)

Composition
-----------

Since everything is pure python, composition is trivial. The following describes some useful patterns.

Context managers
~~~~~~~~~~~~~~~~

Wrap the specific stuff with common functionality by using context managers::

    from contextlib import contextmanager

    @contextmanager
    def form_field(label_name):
        with div(class_="form-field"):
            label(label_name)
            yield

    def my_view(request):
        with form_field("What's your name"):
            input_(type="text")

Components
~~~~~~~~~~

Structure common functionality into functions. If you want to use the output of a function as the input to a
hypergen element, eg. ``div()``, implementation details forces you to decorate it as::

    from hypergen.template import component

    @component
    def my_popup(title, text):
        with div(class_="popup"):
            h1(title)
            p(text)

    div("Monday", my_popup("Tuesday", "Go, go go"), "Thursday")  

Helpers
-------

Some additional functions are available in the template module:

*write(string)*
    Writes the given html. Entities are escaped.
*raw(string)*
    Writes the given html. **Entities are NOT escaped**.

*rst(string)*
    Converts given restructured text string to html and writes it. Needs ``pip install docutils``.
