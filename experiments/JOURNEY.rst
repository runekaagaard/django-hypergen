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
