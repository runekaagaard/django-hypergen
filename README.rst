.. image :: https://github.com/runekaagaard/django-hypergen/actions/workflows/pytest.yml/badge.svg

Why hypergen?
=============

Say bye bye to:

- frontend
- javascript
- mangling making data ready for serialization
- serialization/deserialization
- template language
- webpack/NPM/parcel/gulp/redux/react/etc/etc/etc

And hello to:

- automatic liveview features
- composable pure python templates
- easy dataformat to perform custom frontend actions
- automatic serialization/deserialization from backend->frontend and frontend->backend
  
Why not Hypergen?
=================

- every frontend change on the frontend requires a call to the server
- python templating is not for everyone. Using Django templates is possible but not as polished yet

Value Proposition
=================

The basic form that makes Hypergen great (for us) is exemplified in this simple counter::

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

Our journal to Hypergen
=======================

The journey leading up to building hypergen has been 15 years of experimenting with all the different methodologies of building websites for advanced business applications. It went something like this:

- Custom non-frameworky PHP: Totally great cowboy style. Everything is a already a template.
- Drupal obession: Why are we programming an UI for us programmers to build the site when we could just program the site? Try to think about the problem on your own before following current "best practices". Use a framework that is actually a framework.
- Switch to Django. Wow there is actually all the features we need, and great docs too. Ahh python makes sense. Django forms and the request/response cycle is great. Djangos templates works fine for most stuff.
- Frontend level1: We need dynamic features, use the jQuery language to sprinkle behaviour where needed. State management is hard. Disconnect between server and client.
- Frontend level2: Oh noohs the jQuery is unmanageable. Lets use handlebars templates, a persistent state and render everything on each state change. Rerendering is sluggish for large pages.
- Frontend level3: Please save us React. State management is finally kind of nice. Everything is a template. Wow building duplicate functionality on the server and the client is annoying. A lot of the code is just about shuffling data between the server and the client. We miss python and all the great stuff in Django.
- Why can't we just write html in python and have frontend events call python functions? Actually we can, enter Hypergen :)

Running the examples
====================

::

    git clone git@github.com:runekaagaard/django-hypergen.git
    cd django-hypergen/
    virtualenv -p python3.9 venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -r examples/requirements.txt
    cd examples
    python manage.py migrate
    python manage.py runserver
    # open http://127.0.0.1:8000 in your browser
    
Contributing
============

Bug reports and feature requests are `very welcome <https://github.com/runekaagaard/django-hypergen/issues/new>`_. So are pull requests or diffs.

Authors
=======

Hypergen is written by `Jeppe Tuxen <https://github.com/jeppetuxen>`_ and `Rune Kaagaard <https://github.com/runekaagaard>`_. While we are unfortunately not working fulltime on Hypergen we are using it pretty extensively at work, so it's a big focus of ours.

Developing
==========

Backend
-------

Format all python code with yapf.

Frontend
--------

::
    
    sudo yarn global add parcel-bundler
    # or
    sudo npm install -g parcel-bundler
    cd hypergen/static/hypergen
    parcel watch -o hypergen.min.js -d . hypergen.js
    
Profiling
---------

::

    rm -f /tmp/hypergen.profile && python -m cProfile -o /tmp/hypergen.profile manage.py runserver 127.0.0.1:8002
    echo -e 'sort tottime\nstats' | python3 -m pstats /tmp/hypergen.profile | less
    # or
    pyprof2calltree -i /tmp/hypergen.profile -k

    #
    rm -f /tmp/hypergen.profile && python -m cProfile -o /tmp/hypergen.profile manage.py inputs_profile && \
        echo -e 'sort tottime\nstats' | python3 -m pstats /tmp/hypergen.profile | less

