import json
from django.http import HttpResponse


# response
def return_response(obj):
    response = {"code": 0, "response": obj}
    return HttpResponse(json.dumps(response), content_type='application/json')


def return_error(msg):
    response = {"code": 1, "response": msg}
    return HttpResponse(json.dumps(response), content_type='application/json')


def return_success(msg):
    response = {"code": 0, "response": msg}
    return HttpResponse(json.dumps(response), content_type='application/json')


# request
def return_related(request):
    try:
        related = request["related"]
    except KeyError:
        related = []
    return related


def return_optional(request, optional):
    opt = {}
    for attr in optional:
        try:
            opt[attr] = request[attr]
        except KeyError:
            continue
    return opt


def return_GET_params(request):
    GET_params = {}
    for attr in request.GET:
        GET_params[attr] = request.GET.get(attr)
    return GET_params


def params_are_right(request, required):
    for param in required:
        if param not in request:
            raise Exception("http: required element " + param + " not found")
        if request[param] is not None:
            try:
                request[param] = request[param].encode('utf-8')
            except Exception:
                continue
    return
