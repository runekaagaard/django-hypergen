.. figure:: https://raw.githubusercontent.com/runekaagaard/django-hypergen/main/examples/website/static/website/hypergen-logo2.png
    :align: center
    :target: https://github.com/runekaagaard/django-hypergen
    :alt: Welcome to Django Hypergen

.. image :: https://github.com/runekaagaard/django-hypergen/actions/workflows/pytest.yml/badge.svg

Features
========

- Wonderful composability - structure your app by arranging python functions
- Less infrastructure - take a break from npm, npx, yarn, webpack, parcel, react, redux, gulp, template tags, angular, vue and friends
- Build truly singlepage apps - avoid abstraction gaps to a template language and javascript
- Async not needed - uses the vanilla Django Request-Response cycle
- Automatic (de)serialization - use python builtin types and move on
- No magic strings - reactivity is defined by referencing python functions
- Free partial loading and back/forward history support - no special setup needed
- Inbuilt confirmation dialogs, blocking and debouncing of client side events
- Easy uploading of files - with progress bar

Value Proposition
=================

The basic form that makes Hypergen great (for us) is exemplified in this simple counter:

.. code-block:: python

    from hypergen.core import *
    from hypergen.core import callback as cb
    from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED

    from django.templatetags.static import static

    @hypergen_view(perm=NO_PERM_REQUIRED)
    def counter(request):
        doctype()
        with html():
            with head():
                script(src=static("hypergen/hypergen.min.js"))
            with body(id_="body"):
                template(1)

    @hypergen_callback(perm=NO_PERM_REQUIRED, target_id="body")
    def increment(request, n):
        template(n + 1)

    def template(n):
        label("Current value: ")
        input_(id_="n", type_="number", value=n)
        button("Increment", id_="increment", onclick=cb(increment, n))

Running the examples
====================

.. code-block:: bash

    git clone git@github.com:runekaagaard/django-hypergen.git
    cd django-hypergen/
    virtualenv -p python3.9 venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -r examples/requirements.txt
    cd examples
    python manage.py migrate
    python manage.py runserver

Then browse to http://127.0.0.1:8000.
    
Contributing
============

Bug reports and feature requests are `very welcome <https://github.com/runekaagaard/django-hypergen/issues/new>`_. So are pull requests or diffs.

Authors
=======

Hypergen is written by `Jeppe Tuxen <https://github.com/jeppetuxen>`_ and `Rune Kaagaard <https://github.com/runekaagaard>`_. While we are unfortunately not working fulltime on Hypergen we are using it pretty extensively at work, so it's a big focus of ours.

Why not Hypergen?
=================

- Every frontend change on the frontend requires a call to the server
- Python templating is not for everyone. Using Django templates is possible but not as polished yet

Developing
==========

Backend
-------

Hypergen is located in ``src/hypergen``. Format all python code with yapf, a .yapf config file is present in the repository.

Frontend
--------

Compile the javascript files:

.. code-block:: bash

    yarn global add parcel-bundler
    # or
    npm install -g parcel-bundler
    cd hypergen/static/hypergen
    parcel watch -o hypergen.min.js -d . hypergen.js
    
Profiling
---------

How fast are we?:

.. code-block:: bash

    rm -f /tmp/hypergen.profile && python -m cProfile -o /tmp/hypergen.profile manage.py runserver 127.0.0.1:8002
    echo -e 'sort tottime\nstats' | python3 -m pstats /tmp/hypergen.profile | less
    # or
    pyprof2calltree -i /tmp/hypergen.profile -k

    #
    rm -f /tmp/hypergen.profile && python -m cProfile -o /tmp/hypergen.profile manage.py inputs_profile && \
        echo -e 'sort tottime\nstats' | python3 -m pstats /tmp/hypergen.profile | less

Testing
=======

We have a Github Action that automatically tests a matrix of Django and Python versions. You can run the pytest tests locally like so:

.. code-block:: bash

    pip install requirements.txt
    make pytest-run

And the testcafe end-to-end tests:

.. code-block:: bash
    
    npm i -g testcafe
    make testcafe-run
    # or
    make testcafe-run-headless

Requires that the examples are running on ``127.0.0.1:8002``.
