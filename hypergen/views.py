from hypergen.contrib import hypergen_callback
from hypergen.core import save_translation

@hypergen_callback(perm="hypergen.kv_hypergen_translations", target_id="TODO-NOT-USED-GET_RID_OFF!")
def translate(request, a, b):
    save_translation(a, b)
