# In hypergen.
def hypergen(func, *args, **kwargs):
    get_callback = kwargs.pop("get_callback")
    if get_callback is not None:
        callback = get_callback(func, *args, **kwargs)
        if callback is not None:
            response = callback()
            if response is not None:
                return response

    func(*args, **kwargs)

    return  # the html.


# In app.


def get_callback(func, request, *args, **kwargs):
    if not request.method == "POST" and request.is_xhr():
        return None
    else:
        """
        E.g. ["todos.views.todos|update", 91, {"title": "Milk",
            "description": "Just buy it!"}]
        """
        return request.POST.get("hypergen_callback")
