import json

from django.http.response import HttpResponse
from django.utils.module_loading import import_string
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # FTODO Remove. Add perms.
def callback(request, func):
    in_ = json.loads(request.body)
    func = import_string(func)
    out = func(*in_["args"])
    if func.callback_output is not None:
        out = func.callback_output()

    return HttpResponse(
        json.dumps(out), status=200, content_type='application/json')
