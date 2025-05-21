.. _js_commands:

========================
Client-Side Commands
========================

Hypergen allows you to trigger common JavaScript actions on the client directly from your Python code using the ``command()`` function. This is useful for dynamic updates to the page that don't require a full re-render of a component or for utility actions like redirects.

These commands are invoked from your Python ``@action`` or ``@liveview`` methods by returning a list containing the ``command`` call:

.. code-block:: python

    from hypergen import command, action

    @action
    def do_something_on_client(request):
        return [
            command("hypergen.remove", "#temporary-message"),
            command("hypergen.redirect", "/new-page", delay=1000) # delay is optional
        ]

Below is a reference for the available ``hypergen.*`` commands that can be called this way.

---------------------
``hypergen.remove``
---------------------

Removes DOM element(s) from the page.

* **Purpose**: Deletes elements matching the CSS selector from the DOM.
* **Python Example**:

    .. code-block:: python

        command("hypergen.remove", "#my-element-to-delete")

* **Arguments**:
    * ``selector`` (string): A CSS selector for the element(s) to remove. All matching elements will be removed.
* **JavaScript Action**: Iterates through all elements matching the ``selector`` and calls ``element.remove()`` on each.

-------------------
``hypergen.hide``
-------------------

Hides DOM element(s) by setting their ``style.display`` CSS property to ``none``.

* **Purpose**: Makes elements invisible and removes them from the layout flow.
* **Python Example**:

    .. code-block:: python

        command("hypergen.hide", ".elements-to-hide")

* **Arguments**:
    * ``selector`` (string): A CSS selector for the element(s) to hide.
* **JavaScript Action**: Iterates through all elements matching the ``selector`` and sets ``element.style.display = 'none'``.

-------------------
``hypergen.show``
-------------------

Makes DOM element(s) visible by setting their ``style.display`` CSS property.

* **Purpose**: Makes elements visible, causing them to reflow according to their display type.
* **Python Example**:

    .. code-block:: python

        # Show with default display: 'block'
        command("hypergen.show", "#hidden-section")

        # Show with a specific display type
        command("hypergen.show", ".flex-container", "flex")

* **Arguments**:
    * ``selector`` (string): A CSS selector for the element(s) to show.
    * ``display_value`` (string, optional): The value for the ``display`` CSS property (e.g., "block", "flex", "inline-block"). Defaults to ``"block"``.
* **JavaScript Action**: Iterates through all elements matching the ``selector`` and sets ``element.style.display = display_value``.

---------------------
``hypergen.visible``
---------------------

Makes a DOM element visible by setting its ``style.visibility`` CSS property to ``visible``.

* **Purpose**: Makes an element visible. Unlike ``hypergen.show`` (which uses ``display``), setting ``visibility`` to ``visible`` will make the element appear, but it always retains its space in the layout.
* **Python Example**:

    .. code-block:: python

        command("hypergen.visible", "#my-specific-element")

* **Arguments**:
    * ``selector`` (string): A CSS selector for the element to affect.
* **JavaScript Action**: Sets ``element.style.visibility = 'visible'`` for the **first** element matching the ``selector``.
* **Note**: This command targets only the first element found by the selector, unlike ``hypergen.show`` or ``hypergen.hide``.

--------------------
``hypergen.hidden``
--------------------

Hides a DOM element by setting its ``style.visibility`` CSS property to ``hidden``.

* **Purpose**: Makes an element invisible but retains its space in the layout.
* **Python Example**:

    .. code-block:: python

        command("hypergen.hidden", "#another-specific-element")

* **Arguments**:
    * ``selector`` (string): A CSS selector for the element to affect.
* **JavaScript Action**: Sets ``element.style.visibility = 'hidden'`` for the **first** element matching the ``selector``.
* **Note**: This command targets only the first element found by the selector.

----------------------
``hypergen.redirect``
----------------------

Redirects the browser to a new URL.

* **Purpose**: Navigates the user to a different web page.
* **Python Example**:

    .. code-block:: python

        # Immediate redirect
        command("hypergen.redirect", "/new-page")

        # Redirect after a delay (e.g., 500ms)
        command("hypergen.redirect", "https://example.com", 500)

* **Arguments**:
    * ``url`` (string): The URL to redirect to.
    * ``delay`` (integer, optional): Delay in milliseconds before redirecting. Defaults to ``0`` (immediate).
* **JavaScript Action**: Changes ``window.location.href`` after the optional delay.

--------------------
``hypergen.append``
--------------------

Appends HTML content to the end of the selected DOM element(s).

* **Purpose**: Adds new HTML content inside and at the end of specified elements.
* **Python Example**:

    .. code-block:: python

        command("hypergen.append", "#my-list", "<li>New item at the end</li>")

* **Arguments**:
    * ``selector`` (string): A CSS selector for the parent element(s).
    * ``html`` (string): The HTML string to append.
* **JavaScript Action**: Iterates through all elements matching the ``selector`` and uses ``element.insertAdjacentHTML('beforeend', html)``.

---------------------
``hypergen.prepend``
---------------------

Prepends HTML content to the beginning of the selected DOM element(s).

* **Purpose**: Adds new HTML content inside and at the beginning of specified elements.
* **Python Example**:

    .. code-block:: python

        command("hypergen.prepend", "#my-list", "<li>New item at the start</li>")

* **Arguments**:
    * ``selector`` (string): A CSS selector for the parent element(s).
    * ``html`` (string): The HTML string to prepend.
* **JavaScript Action**: Iterates through all elements matching the ``selector`` and uses ``element.insertAdjacentHTML('afterbegin', html)``.

---------------------------
``hypergen.setClientState``
---------------------------

Sets a key-value pair in a client-side JavaScript object named ``hypergen.clientState``. This state is automatically sent back to the server with subsequent Hypergen requests (e.g., when an ``@action`` is triggered).

* **Purpose**: Allows you to store and retrieve simple state directly on the client, which can then be accessed by the server.
* **Python Example**:

    .. code-block:: python

        command("hypergen.setClientState", "userTheme", "dark")
        command("hypergen.setClientState", "itemSelected", 123)

* **Arguments**:
    * ``key`` (string): The key for the state variable.
    * ``value`` (any): The value to set. It should be a type that can be serialized to JSON (e.g., string, number, boolean, list, dict).
* **JavaScript Action**: Sets ``hypergen.clientState[key] = value;``.

Reading Client State
~~~~~~~~~~~~~~~~~~~~

**On the Client (JavaScript)**

You can access the client state directly in your own JavaScript code by reading properties of the ``hypergen.clientState`` object:

.. code-block:: javascript

    // Assuming setClientState("userTheme", "dark") was called
    let currentTheme = hypergen.clientState.userTheme; // "dark"
    console.log(currentTheme);

    if (hypergen.clientState.itemSelected === 123) {
        // Do something
    }

**On the Server (Python)**

The entire ``hypergen.clientState`` object is sent as a JSON string in the ``hypergen_client_state`` POST parameter with each Hypergen request (e.g., to an ``@action``). Hypergen automatically parses this and makes it available via ``context.hypergen.appstate``.

.. code-block:: python

    from hypergen import action, context

    @action
    def my_server_action(request):
        # Access the client state through context.hypergen.appstate
        user_theme = context.hypergen.appstate.get('userTheme')
        item_id = context.hypergen.appstate.get('itemSelected')

        if user_theme == 'dark':
            print(f"User prefers dark theme. Selected item: {item_id}")
        # ... your action logic

        return [] # Or other commands/updates

    # Initializing clientState from a @liveview
    from hypergen import liveview

    @liveview(appstate={'initialValue': 'hello', 'userTheme': 'light'})
    def my_live_view(request):
        # context.hypergen.appstate will initially contain {'initialValue': 'hello', 'userTheme': 'light'}
        # and will be updated if hypergen.setClientState is called on the client.
        pass

The ``appstate`` parameter in the ``@liveview`` decorator can be used to set the initial values of ``hypergen.clientState`` when the liveview is first rendered. Subsequently, ``hypergen.setClientState`` modifies this state on the client, and the updated state is available in ``context.hypergen.appstate`` on the server for following requests.
