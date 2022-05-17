class LiveviewFeature:
    @classmethod
    def context(cls):
        pass

    @classmethod
    def before(cls):
        pass

    @classmethod
    def after(cls):
        pass

def liveview(func, *args, **kwargs):
    with c(hypergen_context=liveview_context(kwargs)):
        hypergen(func, *args, **kwargs)
