from typing import Callable, Iterator, Union, Optional

# Manipulation of classes.

def add_class(id: str, class_name: Union[str, Iterator[str]], queue: Optional[str] = None,
    send: bool = False) -> list:
    """
    Adds one or more class names to the DOM element with the given id.

    Args:
        id: The id of the DOM element to add the classname to.
        class_name: Names or iterable of names to add.
        queue: Optional serial FILO queue to perform this command in.
        send: When False, don't send the command to the server.

    Returns:
        The raw command format on the form ["my_command_name", "arg1", "arg2"].
    """

def remove_class(id: str, class_name: Union[str, Iterator[str]], queue: Optional[str] = None,
    send: bool = False) -> list:
    """
    Removes one or more class names to the DOM element with the given id.
    """

def toggle_class(id: str, class_name: Union[str, Iterator[str]], queue: Optional[str] = None,
    send: bool = False) -> list:
    """
    Toggles one or more class names to the DOM element with the given id.
    """

# Modify HTML

def morph(id: str, html: str):
    """
    Updates the HTML inside the DOM element with the given id.
    """

def prepend(id: str, html: str):
    pass

def append(id: str, html: str):
    pass

def before(id: str, html: str):
    pass

def after(id: str, html: str):
    pass

def remove(id: str):
    """
    Removes the DOM element with the given id from the DOM. 
    """

def empty(id: str):
    """
    Removes all children of the DOM element with the given id. 
    """
    pass

def prop(id: str, name: str, value: Optional[str, int, bool]):
    """
    Changes a property on the DOM element of the given ID. Use None, False or OMIT to remove the property.
    """
    pass

def css(id, values):
    pass

def offset(id, top, left):
    pass

def width(id, value):
    pass

def height(id, value):
    pass

# Positioning
def scroll_left(value):
    pass

def scroll_top(value):
    pass
