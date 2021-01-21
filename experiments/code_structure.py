Callback = namedtuple("Callback", "args debounce")


def callback(path, args=None, debounce=100):
    return Callback(path, args if args is not None else [], debounde)


def input_(**attrs):
    if state.auto_id is True and "id_" not in attrs:
        attrs["id_"] = next(state.iterid)
    if state.liveview is True:
        for k, v in attrs.iteritems():
            if k.startswith("on") and type(v) in (list, tuple, Callback):
                cb = callback(v[0], v[1:]) if type(v) in (list, tuple) else v

def get_liveview_arg(x, attrs):
        if x == THIS:
            return json.dumps(attrs["liveview_arg"])
        else:
            arg = getattr(x, "liveview_arg", None)
            if arg:
                if arg.startswith("H."):
                    return arg
                else:
                    return json.dumps(arg)
            else:
                return json.dumps(x)

            v = "H.cb({})".format(",".join(
                get_liveview_arg(x, attrs)
                for x in [v[0].hypergen_url] + list(v[1:])))

    def form_element(liveview, attrs):
        if liveview:
            type_ = 

            attrs["liveview_arg"] = 

        return attrs
