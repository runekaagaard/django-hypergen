import json

from django.http.response import HttpResponse
from django.utils.module_loading import import_string
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # TODO Remove. Add perms. Security.
def callback(request, path):

    in_ = json.loads(request.body)
    func = import_string(path)
    assert func.hypergen_is_callback is True
    out = func(request, *in_["args"])

    return HttpResponse(
        json.dumps(out), status=200, content_type='application/json')
