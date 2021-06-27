Why Hypergen?
=============

The journey leading up to building hypergen has been 15 years of experimenting with all the different methodologies of building websites for advanced business applications. It went something like this:

- Custom non-frameworky PHP: Totally great cowboy style. Everything is a already a template.
- Drupal obession: Why am I programming an UI for us programmers to build the site when we could just program the site? Try to think about the problem on your own before following current "best practices". Use a framework that is actually a framework.
- Switch to Django. Wow there is actually all the features I need, and great docs too. Ahh python makes sense. Django forms and the request/response cycle is great. Python is not a template language, hmm i guess djangos templates are ok.
- Frontend level1: We need dynamic features, use the jQuery language to sprinkle behaviour where needed. State management is hard. Disconnect between server and client.
- Frontend level2: Oh noohs the jQuery is unmanageable. Lets use handlebars templates, a persistent state and render everything on each state change. A bit slow sometimes.
- Frontend level3: Please save me React. State management is finally kind of nice. Everything is a template. Wow building duplicate functionality on the server and the client is annoying. A lot of the code is just about shuffling data between the server and the client. I miss python and all the great stuff in Django.
- No frontend, no javascript, no serialization, no templates, no webpack, no NPM, no data mangling: Why can't I just write my html in python and make frontend events call python functions. Actually I can, enter Hypergen :)

Why not Hypergen?
=================

- Every frontend change on the frontend requires a call to the server.
- Python templating is not for everyone. Using Django templates is possible but not as polished yet.

Value Proposition
=================

The basic form that makes Hypergen great (for me) is exemplified in this simple counter::

    from hypergen.core import *
    from hypergen.core import callback as cb
    from hypergen.contrib import hypergen_view, hypergen_callback
    
    @hypergen_view
    def counter():
        template(1)
    
    @hypergen_callback
    def increment(n):
        template(n+1)

    def template(n):
        doctype()
        with html():
            with body():
                label("Current value: ")
                input(id_="n", type_="number", value=n)
                button("Increment", onclick=cb(hypergen_callback, n))
        
