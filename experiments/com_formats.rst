Server to Client
================

::

    REPLACE = 1
    DELETE = 2
    APPEND = 3
    INSERT_AFTER = 4
    INSERT_BEFORE = 5
    [
        [1, "element_id", "<div id=a>The HTML</div>"],
        [2, "element_id"],
        [3, "element_id", "<div id=b>The HTML</div>"],
        [4, "element_id", "<div id=c>The HTML</div>"],
        [5, "element_id", "<div id=d>The HTML</div>"],
    ]

Client to Server
================

::

    ["id_series", "callback", arg1, arg2, arg3, arg4]

How to handle server side ids with async requests?
==================================================

The client keeps track of how many requests it has made and requests a specific series that gets prefixed to each element id. So if the series is 42 the ids will look like "h42.1", "h42.2", etc.

The ids could be base66 encoded. Valid id chars are "a-zA-Z0-9._:-". Must start with a letter. Series use "." as a separator. They could be base65 encoded. 
