Work in progress...

Client Communication Format
===========================

Every time a client side event (onchange, onclick, etc.) triggers a callback view function on the server, the server returns a list of commands for the client to execute. Most of whom manipulates the DOM.

On the server it looks like this:

.. code-block:: python
                
    from hypergen import LiveviewResponse
    
    @permission_required("myapp.myperm")
    def my_callback(request):
        return LiveviewResponse([
            ["hypergen.morph", "id-of-element", "<div>New html for this section</div>", {}],
            ["hypergen.add_notification", "Updated the page!", {"sticky": True}],
        ])

or exactly the same using the convenience wrappers:

.. code-block:: python
                
    from hypergen import LiveviewResponse
    from hypergen["commands"] import morph, add_notification
    
    @permission_required("myapp.myperm")
    def my_callback(request):
        return LiveviewResponse([
            morph("id-of-element", "<div>New html for this section</div>"),
            add_notification("Updated the page!", sticky=True),
        ])

This generates json that can be read by the client:
     
.. code-block:: javascript

    {
        "status": 200,
        "commands": [
            ["hypergen.morph", "id-of-element", "<div>New html for this section</div>", {}],
            ["hypergen.add_notification", "Updated the page!", {sticky: true}],
        ]
    }

Thus it is completely possible to use different frameworks and languages on the backend.
        
Commands can be executed manually on the client as well with ``execute_commands``:

.. code-block:: javascript
                
    import { execute_commands } from 'hypergen'

    execute_commands([
        ["hypergen.morph", "id-of-element", "<div>New html for this section</div>", {}],
        ["hypergen.add_notification", "Updated the page!", {sticky: true}],
    ])

Each command is an array on the form ``[NAME, ARG1, ARG2, ..., ARGN, KEYWORD_ARGUMENTS]``, where:

*NAME*
    The name of a command function in ``hypergen["commands"]``. Add your own custom ["commands"] to
    ``hypergen["commands"]``.
*ARG1, ARG2, ..., ARGN*
    Optional positional keyword arguments to the command function.
*KEYWORD_ARGUMENTS*
    A required object with optional keyword arguments. Will be given as the last argument to the
    command function.

You can also just call the command functions directly:

.. code-block:: javascript

    import { morph, add_notification } from 'hypergen/commands'

    morph("id-of-element", "<div>New html for this section</div>")
    add_notification("Updated the page!", {sticky: true})


Server Communication Format
===========================

Stub.

Concurrency Groups
==================

A callback must have a concurrency group assigned. Each concurrency group has a concurrency model and the callbacks in a group are handled accordingly. There are no dependencies across concurrency groups.   

Execution Modes
===============

Stub.

*MAIN*
    Stub.
*OFFLINE*
    Stub.
*SERVER_ERROR_500*
    Stub.

Blocking
--------

Stub.

Concurrency Models
==================

Stub.

*SERIAL*
    Stub.
*PARALLEL*
    Stub.
*RECEIVE_SERIAL*
    Stub.

Notifications
=============

Stub.

Focus
=====

Stub.

Client State
============

The client maintains a thin state to handle going offline, what to do when receiving unknown server errors and configuring concurrency models. This can be set either from the server with the ``set_state`` command or directly in the frontend.

It defaults to:

.. code-block:: javascript

    export const ALL = "_ALL_"
    
    export var default_state = {
        hypergen: {
            execution_modes: {
                main: {
                    enter: [],
                    exit: [],
                },
                offline: {
                    enter: [
                        ["hypergen.add_notification", "Oh-ohh, you are offline.",
                         {sticky: true, group: "offline"}],
                        ["hypergen.block", ALL, {}],
                    ],
                    exit: [
                        ["hypergen.clear_notifications", {groups: ["offline"]}],
                        ["hypergen.add_notification", "The wheels are turning again.", {}],
                        ["hypergen.release", ALL, {}],                        
                    ],
                },
                server_error_500: {
                    enter: [
                        ["hypergen.add_notification", "Unknown server error.",
                         {sticky: true, group: "e500"}],
                        ["hypergen.block", ALL, {}],
                    ],
                    exit: [
                        ["hypergen.clear_notifications", {groups: ["e500"]}],
                        ["hypergen.release", ALL, {}]                        
                    ],
                },
            },
            events: {
                blocked: [
                    ["hypergen.flash", "Input is blocked. Please try later.", {throttle: 0.25}],
                ]
                released: [
                    ["hypergen.flash", "I can accept input again. Go Go Go!"],
                ]
            },
            concurrency_groups: {
                main: {
                    concurrency_model: RECEIVE_SERIAL,
                },
                save: {
                    concurrency_model: SERIAL,
                    block: ["main"],
                }
            }
        }
    }

Supported Client Commands
=========================

hypergen.morph(id_of_element, new_html)
---------------------------------------

Updates the given element with new html. Uses morphdom for efficency.

hypergen.add_callback(id_of_element, events, url, concurrency_group)
------------------------------------------------------------------------------------

Creates an eventlistener on ``id_of_element`` for an array of events that performs a callback to the server. The server responds with client commands that will be executed.

hypergen.add_notification(message, sticky=False, group=None, throttle=None)
---------------------------------------------------------------------------

Display a notification message. Set ``sticky`` to true to persist the message. Optionally mark it as part of a group or throttle similar messages in seconds.

hypergen.clear_notifications(groups=None)
------------------------------------------

Unless a list of groups is given, removes all notifications.

hypergen.focus(id_of_element)
------------------------------

Changes the focus to the given element.

hypergen.blur()
---------------

Removes the focus from the focused element, if any.

hypergen.block(execution_groups)
--------------------------------

Blocks execution of events for the given concurrency groups. Use ``ALL`` to block all concurrency groups.

hypergen.release(execution_groups)
--------------------------------

Resumes execution of events for the given concurrency groups. Use ``ALL`` to resume all concurrency groups.

hypergen.set_state(path, data, merge=False)
-------------------------------------------

Set or merges the client state at the given path.

hypergen.switch_mode(mode_name)
-------------------------------

Changes to another execution mode. Hypergen supports out of the box: "MAIN", "OFFLINE" and "SERVER_ERROR_500".

