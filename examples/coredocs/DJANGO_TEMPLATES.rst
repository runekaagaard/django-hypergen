Django Template Support
=======================

Even though we enthusiastically endorse using the pure Python template engine, an important aspect of Hypergen is
to extend existing vanilla Django html templates with liveview functionality.

Check out the `demo </djangotemplates/>`_ to see an example of that.

Setup HTML templates
--------------------

In your Django base template html file you need to ``{% load hypergen %}`` and then place ``{% hypergen_media_header %}`` inside ``<head>...</head>`` and ``{% hypergen_media_footer %}`` just before ``</body>``. If you wish to
partially update the inner content of the page you also need to add a div with an id that matches the ``target_id`` keyword argument to ``@action``.

The hypergen parts of the base template will look like::

    {% load hypergen %}<!DOCTYPE html>
    <html>
        <head>
            {% hypergen_media_header %}
        </head>
        <body>
            <div id="content">
                {% block content %}
                {% endblock %}
            </div>
        </body>
        {% hypergen_media_footer %}
    </html>

Enable liveview for existing vanilla Django views
-------------------------------------------------

To enable liveview capabilities for existing vanilla Django views they should be decorated with the ``@liveview``
decorator. Prevent Hypergen from automatically adding a route by setting the ``autourl`` keyword argument to False::

    from django.shortcuts import render
    
    @liveview(perm=NO_PERM_REQUIRED, autourl=False)
    def my_vanilla_django_view(request):
        return render(request, "my_app/my_template.html")

Bind DOM events to callbacks in HTML templates
----------------------------------------------

The ``{% callback %}`` template tag takes first an reversible url and then an optional number of arguments that will be passed to the action or consumer. The ``id``, ``event`` keyword arguments are required. It automatically adds an id attribute unless ``add_id=False`` is passed.

Strings prefixed with a ``#`` are interpreted as ids and the value of those HTML elements will be passed as arguments
to the @action or @consumer function. Type coercion can be defined by adding an optional ``.[type]`` to the magic string, e.g. ``"#my_id.date"``. The following coercions are allowed: str, float, int, date, datetime, month and week.

It takes the all same keyword arguments as the regular ``callback`` function, like ``debounce``, ``confirm`` and ``blocks``.

A click event on a button can be bound to a callback like this::

    {% load hypergen %}

    {% block content %}
        <button {% callback "my_app:my_action" "#number.float" id="increment" event="onclick" %}>
            Increment
        </button>
    {% endblock %}

Partially render specific blocks in a Django html template
----------------------------------------------------------

Actions work exactly like in Hypergen. Hypergen provides the ``render_to_hypergen`` function that works exactly as Djangos render_to_string except for two things:

1. It writes the HTML directly to the page.
2. It supports a "block" keyword argument so that only the content of that block is rendered.

To have an action partially render the ``content`` block inside the ``content`` id one would write::

    from hypergen.templatetags.hypergen import render_to_hypergen

    @action(perm=NO_PERM_REQUIRED, target_id="content")
    def my_action(request):
        # do what you want here...
        render_to_hypergen("my_app/my_template.html", block="content")
