Primitives
==========

- locks
- isolations
- mutual exclusions
- latch
- semaphore
- read/write barrier

Links
=====

- https://dannyyassine.github.io/operationkit/

Random
======

::

    concurrency_groups:
        chat:
            mode_send: parallel
            mode_receive: unordered
        live_validation:
            mode_send: parallel
            mode_receive: ordered
            meta:
                block_message: "Please don't change the form when we are saving the data on the server."
        submit:
            mode_send: serial
            mode_receive: ordered
            blocks:
                - live_validation
            
