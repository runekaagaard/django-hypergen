Client Commands
==============

In Hypergen, client commands provide a mechanism to directly manipulate the DOM and control client-side behavior from the server. These commands allow you to modify elements, update visibility, redirect the browser, and more without writing any JavaScript yourself.

Using Client Commands
--------------------

All commands follow the same pattern::

    from hypergen.imports import *

    command("hypergen.commandName", *args)

Commands can be used in both liveviews and actions. They are sent to the client and executed in the order they are defined.

Available Commands
-----------------

DOM Manipulation
~~~~~~~~~~~~~~~

hypergen.morph
^^^^^^^^^^^^^

Updates an element's content using morphdom for efficient DOM updating::

    command("hypergen.morph", "element-id", "<p>New content</p>")

hypergen.remove
^^^^^^^^^^^^^

Removes an element from the DOM::

    command("hypergen.remove", "element-id")

hypergen.append
^^^^^^^^^^^^^

Appends HTML content to an element::

    command("hypergen.append", "element-id", "<p>Appended content</p>")

hypergen.prepend
^^^^^^^^^^^^^^

Prepends HTML content to an element::

    command("hypergen.prepend", "element-id", "<p>Prepended content</p>")

Visibility Control
~~~~~~~~~~~~~~~~

hypergen.hide
^^^^^^^^^^^

Hides an element by setting its display property to "none"::

    command("hypergen.hide", "element-id")

hypergen.display
^^^^^^^^^^^^^^

Sets an element's display property. By default, it sets it to "block"::

    command("hypergen.display", "element-id")  # Sets to "block"
    command("hypergen.display", "element-id", "flex")  # Sets to "flex"

hypergen.visible
^^^^^^^^^^^^^^

Makes an element visible by setting its visibility property to "visible"::

    command("hypergen.visible", "element-id")

hypergen.hidden
^^^^^^^^^^^^^

Hides an element by setting its visibility property to "hidden". This preserves the element's space in the layout::

    command("hypergen.hidden", "element-id")

Navigation
~~~~~~~~~

hypergen.redirect
^^^^^^^^^^^^^^^

Redirects the browser to a new URL::

    command("hypergen.redirect", "/some/path/")
    # Or to an external URL
    command("hypergen.redirect", "https://example.com")

State Management
~~~~~~~~~~~~~~

hypergen.setClientState
^^^^^^^^^^^^^^^^^^^^^

Sets a value in the client-side state that persists between requests::

    command("hypergen.setClientState", "my.custom.state", {"key": "value"})

To access this state in your JavaScript, you can read it from ``hypergen.clientState``::

    // In your custom JS
    console.log(hypergen.clientState.my.custom.state.key)  // "value"

Examples
--------

Show/Hide a Form Dynamically
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    @liveview(perm=NO_PERM_REQUIRED)
    def toggle_form(request):
        with html(), body():
            button("Show Form", id="show-btn", onclick=callback(show_form))
            button("Hide Form", id="hide-btn", onclick=callback(hide_form))
            
            with div(id="my-form", style={"display": "none"}):
                h3("Contact Form")
                input_(type="text", placeholder="Your name")
                textarea(placeholder="Your message")
                button("Submit")

    @action(perm=NO_PERM_REQUIRED)
    def show_form(request):
        command("hypergen.display", "my-form")
        
    @action(perm=NO_PERM_REQUIRED)
    def hide_form(request):
        command("hypergen.hide", "my-form")

Dynamic Content Loading
~~~~~~~~~~~~~~~~~~~~~

::

    @liveview(perm=NO_PERM_REQUIRED)
    def dynamic_content(request):
        with html(), body():
            h1("Dynamic Content Loading")
            div(id="content-area")
            button("Load More", id="load-btn", onclick=callback(load_more))

    @action(perm=NO_PERM_REQUIRED)
    def load_more(request):
        command("hypergen.append", "content-area", 
                hypergen(lambda: div(p(f"New content loaded at {datetime.now().strftime('%H:%M:%S')}"))))

Managing Multiple UI States
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    @liveview(perm=NO_PERM_REQUIRED)
    def wizard_form(request):
        with html(), body():
            h1("Multi-step Form")
            
            with div(id="step-1"):
                h3("Step 1: Personal Info")
                input_(type="text", placeholder="Name")
                button("Next", id="next-1", onclick=callback(go_to_step_2))
                
            with div(id="step-2", style={"display": "none"}):
                h3("Step 2: Contact Info")
                input_(type="email", placeholder="Email")
                button("Back", id="back-2", onclick=callback(go_to_step_1))
                button("Next", id="next-2", onclick=callback(go_to_step_3))
                
            with div(id="step-3", style={"display": "none"}):
                h3("Step 3: Confirmation")
                p("Thank you for your submission!")
                button("Back", id="back-3", onclick=callback(go_to_step_2))

    @action(perm=NO_PERM_REQUIRED)
    def go_to_step_1(request):
        command("hypergen.display", "step-1")
        command("hypergen.hide", "step-2")
        command("hypergen.hide", "step-3")

    @action(perm=NO_PERM_REQUIRED)
    def go_to_step_2(request):
        command("hypergen.hide", "step-1")
        command("hypergen.display", "step-2")
        command("hypergen.hide", "step-3")

    @action(perm=NO_PERM_REQUIRED)
    def go_to_step_3(request):
        command("hypergen.hide", "step-1")
        command("hypergen.hide", "step-2")
        command("hypergen.display", "step-3")

Advanced Techniques
------------------

Custom Commands
~~~~~~~~~~~~~

You can call any function that's available in the global scope on the client::

    command("console.log", "This message will appear in the browser console")
    command("alert", "This will show an alert dialog")

Chaining Commands
~~~~~~~~~~~~~~~

Multiple commands will execute in the order they are defined::

    @action(perm=NO_PERM_REQUIRED)
    def process_form(request):
        command("hypergen.hide", "form")
        command("hypergen.display", "loading-indicator")
        # Process the form...
        command("hypergen.hide", "loading-indicator")
        command("hypergen.display", "success-message")

Persisting Client State Between Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The client state can be used to maintain information between requests without round-trips to the server::

    @liveview(perm=NO_PERM_REQUIRED)
    def stateful_ui(request):
        command("hypergen.setClientState", "preferences", {"theme": "dark", "fontSize": "large"})
        
        # In your JavaScript, you could access this as:
        # hypergen.clientState.preferences.theme  // "dark"

        # Later, you can update just parts of the state:
        command("hypergen.setClientState", "preferences.fontSize", "medium")
