def hypergen_context(data=None):
    if data is None:
        data = {}

    c_ = m(into=[], event_handler_callbacks={}, event_handler_callback_strs=[],
        target_id=data.pop("target_id",
        "__main__"), commands=[], ids=set(), wrap_elements=data.pop("wrap_elements",
        default_wrap_elements), matched_perms=set(), translate=data.pop("translate", False))

    assert callable(c_.wrap_elements), "wrap_elements must be a callable, is: {}".format(repr(c_.wrap_elements))
    return c_

### Not translation ###

TRANSLATIONS = {}

def translate(s, translatable=True):
    if translatable and c["hypergen"]["translate"]:
        if s in TRANSLATIONS:
            return TRANSLATIONS[s]
        else:
            if c.user.has_perm("hypergen.kv_hypergen_translations"):
                save_translation(s, s)

            return s
    else:
        return s

def load_translations():
    from hypergen.models import KV
    if not TRANSLATIONS:
        try:
            kv, _ = KV.objects.get_or_create(key="hypergen_translations", defaults=d(value='{}'))
            set_translations(kv)
        except Exception:
            logger.exception("Can't load translations")

def set_translations(kv):
    global TRANSLATIONS
    TRANSLATIONS = json.loads(kv.value)

def save_translation(a, b):
    from hypergen.models import KV
    kv, _ = KV.objects.get_or_create(key="hypergen_translations", defaults=d(value='{}'))
    t = json.loads(kv.value)

    t[a] = b
    if b == "RESET":
        del t[a]

    kv.value = json.dumps(t)
    kv.save()
    set_translations(kv)

def non_translatable_elements():
    from hypergen.template import (applet, audio, canvas, head, iframe, link, map_, meter, noframes, object_, picture,
        script, svg, template, textarea, title, video)
    return {
        applet, audio, canvas, head, iframe, link, map_, meter, noframes, object_, picture, script, svg, template,
        textarea, title, video}

config_attrs = {"t", "sep", "coerce_to", "js_coerce_func", "js_value_func"}
translatable = True
translatable_attributes = ["placeholder", "title"]
