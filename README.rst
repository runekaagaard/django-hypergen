.. raw:: html

    <p align="center">
      <a href="https://github.com/runekaagaard/django-hypergen">
        <img src="https://raw.githubusercontent.com/runekaagaard/django-hypergen/main/examples/website/static/website/hypergen-logo.png" alt="Welcome to Django Hypergen" width="75px" height="100px" />
      </a>
    </p>

    <h1 align="center"><a href="https://hypergen.it">Django Hypergen</a></h1>

    <p align="center">
        <b>Take a break from javascript</b>
    </p>
    <p align="center">
        Write server-rendered reactive HTML liveviews for Django in pure python 💫
    </p>
    <p align="center">
        <img src="https://github.com/runekaagaard/django-hypergen/actions/workflows/pytest.yml/badge.svg" />
        <a href="https://pypi.org/project/django-hypergen/">
            <img src="https://badge.fury.io/py/django-hypergen.svg" />
        </a>
    </p>

    <p align="center" dir="auto">
        <a href="https://hypergen.it" rel="nofollow">Homepage</a> &nbsp;&nbsp;•&nbsp;&nbsp;
      <a href="https://hypergen.it/documentation/" rel="nofollow">Documentation</a> &nbsp;&nbsp;•&nbsp;&nbsp;
      <a href="https://github.com/runekaagaard/django-hypergen/issues/" rel="nofollow">Support</a>
    </p>

**Hypergen is short for Hypertext Generator**: Templates are pure python. Instead of writing ``<p>hi</p>`` in a html file, call ``p("hi")`` inside a view. It's simple to keep templates DRY by composing python functions. Hypergen feels a lot like writing jsx.

**Liveview included**: Still in pure python, connect browser events like ``onclick`` to callback functions. Mix frontend input html elements and python datatypes as arguments to callbacks and everything works round-trip. Callbacks are Django views that sends updated html to the frontend as well as other commands.

**1 minute to set up**: Do ``pip install django-hypergen``, add ``'hypergen'`` to ``INSTALLED_APPS``, ``'hypergen.core.context_middleware'`` to ``MIDDLEWARE`` and you're good to go.

How does it look?
=================

Using Hypergens most high-level constructs, a simple counter looks like this:

.. code-block:: python

    from hypergen.core import *
    from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED, base_template

    HYPER = dict(perm=NO_PERM_REQUIRED, base_template=base_template(title="Hello Hypergen"))

    @hypergen_view(**HYPER)
    def counter(request):
        template(0)

    @hypergen_callback(**HYPER)
    def increment(request, n):
        template(n + 1)

    def template(n):
        with p():
            label("Current value: ")
            input_el = input_(id_="n", type_="number", value=n)
            button("Increment", id_="increment", onclick=callback(increment, input_el))

You can `see it in action <https://hypergen.it/hellohypergen/counter/>`_.
        
The ``callback(func, arg1, arg2, ..., **settings)`` function connects the onclick event to the ``increment(request, n)`` callback. The ``n`` argument is the value of the input field.

The ``base_template(title=None)`` function returns a function with html5 boilerplate.

It's python functions all the way down. 🔥🔥🔥

Features
========

- **Composable** - structure your app with ... TADAAA ... python functions
- **Less infrastructure** - take a break from npm, npx, yarn, webpack, parcel, react, redux, gulp, angular, vue and friends
- **Build truly singlepage apps** - avoid abstraction gaps to a template language and javascript
- **Async not needed** - uses the vanilla Django Request-Response cycle
- **Automatic (de)serialization** - use python builtin types and move on
- **No magic strings** - reactivity is defined by referencing python functions
- **Free partial loading** - no special setup required, includes back/forward history support
- **Control over client side events** - inbuilt confirmation dialogs, blocking and debouncing
- **Easy uploading of files** - with progress bar
- **Still loves javascript** - trivially call client functions from the server
- **History buff?** - don't worry, Hypergen supports from Django 1.11, Python 3.5 and up
- **Hyperfy** - the command line app that converts html to hypergen python code

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

Hypergen is written by `Jeppe Tuxen <https://github.com/jeppetuxen>`_ and `Rune Kaagaard <https://github.com/runekaagaard>`_, both located around Copenhagen, Denmark.

We are using Hypergen extensively at work so it's a big focus of ours. 

Why not Hypergen?
=================

- Every frontend event calls to the server
- Python templating is not for everyone. Using Django templates is possible but still in alpha
- No realtime capabilities yet, so the server can only push data back when it receives a request

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

We have a `Github Action <https://github.com/runekaagaard/django-hypergen/blob/main/.github/workflows/pytest.yml>`_ that automatically tests a matrix of Django and Python versions. You can run the pytest tests locally like so:

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
