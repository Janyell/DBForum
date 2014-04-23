import json

from django.http import HttpResponse

from api.post import db_posts_funcs
from api.funcs import params_are_right, return_response, return_optional, return_related, return_GET_params, return_error


def create(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["user", "forum", "thread", "message", "date"]
        optional_data = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
        optional = return_optional(request=request_data,
                                   optional=optional_data)
        try:
            params_are_right(request=request_data,
                            required=required_data)
            post = db_posts_funcs.post_create(date=request_data["date"],
                                              thread=request_data["thread"],
                                              message=request_data["message"],
                                              user=request_data["user"],
                                              forum=request_data["forum"],
                                              optional=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":

        request_data = return_GET_params(request)
        required_data = ["post"]
        related = return_related(request_data)
        try:
            params_are_right(request=request_data,
                            required=required_data)
            post = db_posts_funcs.post_details(request_data["post"],
                                               related=related)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def post_list(request):
    if request.method == "GET":
        request_data = return_GET_params(request)
        entity_attr = None
        try:
            entity_attr = request_data["forum"]
            entity = "forum"
        except KeyError:
            try:
                entity_attr = request_data["thread"]
                entity = "thread"
            except KeyError:
                return return_error("No thread or forum parameters in request")

        optional = return_optional(request=request_data,
                                   optional=["limit", "order", "since"])
        try:
            p_list = db_posts_funcs.post_list(entity=entity,
                                              entity_attr=entity_attr,
                                              related=[],
                                              params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(p_list)
    else:
        return HttpResponse(status=400)


def remove(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["post"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            post = db_posts_funcs.post_remove_or_restore(post_id=request_data["post"],
                                                         status=1)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def restore(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["post"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            post = db_posts_funcs.post_remove_or_restore(post_id=request_data["post"],
                                                         status=0)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def update(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["post", "message"]
        try:
            params_are_right(request=request_data,
                            required=required_data)
            post = db_posts_funcs.post_update(post_id=request_data["post"],
                                              message=request_data["message"])
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def vote(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["post", "vote"]
        try:
            params_are_right(request=request_data,
                            required=required_data)
            post = db_posts_funcs.post_vote(post_id=request_data["post"],
                                            vote=request_data["vote"])
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)