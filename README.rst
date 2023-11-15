.. raw:: html

    <p align="center">
      <a href="https://github.com/runekaagaard/django-hypergen">
        <img src="https://raw.githubusercontent.com/runekaagaard/django-hypergen/main/examples/website/static/website/hypergen-logo.png" alt="Welcome to Django Hypergen" width="75px" height="100px" />
      </a>
    </p>

    <h1 align="center"><a href="https://hypergen.it">Hypergen</a></h1>

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

**Hypergen: A Hypertext Generator**:
Craft templates using pure Python. Instead of declaring ``<p>hi</p>`` in an HTML file, simply invoke ``p("hi")`` within your view. Composing Python functions keeps templates DRY and streamlined. If you've ever written JSX, Hypergen's syntax will feel familiar.

**Reactive Liveviews**:
Effortlessly bridge frontend and backend. Connect browser events like `onclick` straight to backend actions. With these actions, Django views can instantly refresh the frontend with new HTML, send notifications, and more, all while natively working with Python data types.

**Websockets**:
Hypergen brings realtime to the forefront with Django Channels. Set up is a breeze - quickly establish consumers and instantly react to live events. It's realtime made simple and friendly, just the way we like it.

**Production Ready**:
We've deployed Hypergen in projects spanning tens of thousands of lines, serving over 100,000 unique users more than 10 million requests.

**Quickstart**:
Kickstart your Hypergen journey in minutes. Execute ``pip install django-hypergen``, append ``'hypergen'`` to ``INSTALLED_APPS``, include ``'hypergen.context.context_middleware'`` in ``MIDDLEWARE``, and you're all set to dive in.
    
How does it look?
=================

Using Hypergens most high-level constructs, a simple counter looks like this:

.. code-block:: python

    @liveview(perm=NO_PERM_REQUIRED)
    def counter(request):
        with html(), body(), div(id="content"):
            template(0)

    @action(perm=NO_PERM_REQUIRED, target_id="content")
    def increment(request, n):
        template(n + 1)

    def template(n):
        label("Current value: ")
        input_el = input_(id="n", type_="number", value=n)
        button("Increment", id="increment", onclick=callback(increment, input_el))



You can `see it in action <https://hypergen.it/hellohypergen/counter/>`_.
        
The ``callback(func, arg1, arg2, ..., **settings)`` function connects the onclick event to the ``increment(request, n)`` action. The ``n`` argument is the value of the input field.

DOM elements are nested with the ``with`` statement.

It's python all the way down. 🔥🔥🔥

Features
========

- 🧩 **Composable** - structure your app with ... TADAAA ... python functions
- 🌐 **Less infrastructure** - take a break from npm, npx, yarn, webpack, parcel, react, redux, gulp, angular, vue and friends
- 🚀 **Build truly singlepage apps** - avoid abstraction gaps to a template language and javascript
- ⏳ **Async not needed** - uses the vanilla Django Request-Response cycle by default
- 🔀 **Automatic (de)serialization** - use python builtin types and move on
- 🎯 **No magic strings** - reactivity is defined by referencing python functions
- 📦 **Free partial loading** - no special setup required, includes back/forward history support
- 🔒 **Control over client side events** - inbuilt confirmation dialogs, blocking and debouncing
- 📤 **Easy uploading of files** - with progress bar
- 💛 **Still loves javascript** - trivially call client functions from the server
- ⚡ **Realtime** - Create websocket consumers trivially
- 📜 **History buff?** - don't worry, Hypergen supports from Django 1.11, Python 3.6 and up to as of this writing Django 4.2.6 and python 3.12.
- 🛠️ **Hyperfy** - the command line app that converts html to hypergen python code

Running the examples
====================

.. code-block:: bash

    git clone git@github.com:runekaagaard/django-hypergen.git
    cd django-hypergen/
    virtualenv -p python3.9 venv
    source venv/bin/activate
    pip install -r requirements-dev.txt
    cd examples
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

- Every frontend event calls the server. Not good for e.g. games.
- Python templating might not be for everyone. We found it works great in practice.

Developing
==========

Backend
-------

Hypergen is located in ``src/hypergen``. Format all python code with yapf, a .yapf config file is present in the repository.

Frontend
--------

Compile the javascript files:

.. code-block:: bash

    cd hypergen/static/hypergen
    npm install # use node 18 lts
    # watch hypergen.js to dist/hypergen.js
    npm start
    # build hypergen.js to dist/hypergen.js
    npm run build
    
Profiling
---------

How fast are we?:

.. code-block:: bash

    rm -f /tmp/hypergen.profile && python -m cProfile -o /tmp/hypergen.profile manage.py runserver 127.0.0.1:8002
    echo -e 'sort tottime\nstats' | python3 -m pstats /tmp/hypergen.profile | less
    
    # or
    pyprof2calltree -i /tmp/hypergen.profile -k

    # or
    rm -f /tmp/hypergen.profile && python -m cProfile -o /tmp/hypergen.profile manage.py inputs_profile && \
        echo -e 'sort tottime\nstats' | python3 -m pstats /tmp/hypergen.profile | less

Testing
=======

We have a `Github Action <https://github.com/runekaagaard/django-hypergen/blob/main/.github/workflows/pytest.yml>`_ that automatically tests a matrix of Django and Python versions. You can run the pytest tests locally like so:

.. code-block:: bash

    pip install -r requirements-dev.txt
    make pytest-run

And the testcafe end-to-end_ tests:

.. code-block:: bash
    
    npm i -g testcafe
    make testcafe-run
    # or
    make testcafe-run-headless

Requires that the examples are running on ``127.0.0.1:8002``.

Thanks
======

- `Django <https://www.djangoproject.com/>`_ - for making work fun
- `Morphdom <https://github.com/patrick-steele-idem/morphdom>`_ - for fast updating of the DOM tree
- `Pyrsistent <https://pyrsistent.readthedocs.io/en/latest/intro.html>`_ - for providing an immutable dict
- `sockette <https://github.com/lukeed/sockette>`_ - The cutest little WebSocket wrapper! 🧦
- `Simple.css <https://simplecss.org/>`_ - for the no-class styling on the homepage
- `DALL-E mini <https://huggingface.co/spaces/dalle-mini/dalle-mini>`_ - for the logo generated with the query "a vibrant logo of the letter H"
