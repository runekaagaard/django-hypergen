Django Template Support
=======================

Even though we enthusiastically endorse using the pure Python template engine, an important aspect of Hypergen is
also to extend existing vanilla Django html templates with liveview functionality. This can be done either by passing liveview data from the views to the templates or inside the templates themselves.

To enable hypergen context collector views must be decorated with the ``@vanilla_template`` decorator. 

Extending Django templates with liveview functionality
------------------------------------------------------

base_template.html::

    <html>
        <body>
            <div id="content">
                {% block content %}
                {% endblock %}
            </div>
        </body>
    </html>

content.html::

    {% load "hypergen" %}
    {% hypergen_extend "base_template.html" %}
    {% block content %}
        <input id="number" type="number" value="{{n}}" disabled />
        <button {% callback "#number" event="onclick" url="counter:increment" %}>
            Increment
        </button>
    {% endblock %}

The ``callback`` template takes an optional number of arguments. Strings prefixed with a ``#`` is interpreted as ids
and the value of those HTML elements will be passed as arguments to the @action or @consumer function. The ``event`` and ``url`` are required. It automatically adds an id attribute unless ``add_id=False`` is passed.

Use ``{% hypergen_extend %}`` instead of ``{% extend %}`` to make partially updating the page work.



views.py::

    from hypergen.imports import *

    N = 0

    @vanilla_template
    def counter(request):
        return render(request, "content.html", {"n": N})
        
    @callback(perm=NO_PERM_REQUIRED, base_view=counter, target_id="content")
    def increment(request, n):
        global N
        N += 1

Passing callbacks from views to templates
-----------------------------------------

The ``callback_to_string`` function works similarly to ``callback`` but returns a string that can be passed to django
templates and provide liveview capabilities.

views.py::

    from hypergen.imports import *

    def render_counter(n):
        increment_callback = callback_to_string(increment, element_value("number"), id="submit", event="onclick")

        return render(request, "content.html", {"n": 1, "increment_callback": increment_callback})
        
    @vanilla_template
    def counter(request):
        render_counter(1)
        
    @callback(perm=NO_PERM_REQUIRED, target_id="content")
    def increment(request, n):
        render_counter(n+1)

base_template.html::

    <html>
        <body>
            <div id="content">
                {% block content %}
                {% endblock %}
            </div>
        </body>
    </html>

content.html::

    {% hypergen_extend "base_template.html" %}
    {% block content %}
        <input id="number" type="number" disabled />
        <button {{increment_callback}}>Increment</button>
    {% endblock %}

    
