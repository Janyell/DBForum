from api.post import db_posts_funcs
from api.thread import db_threads_funcs
from api.funcs import *
from api.forum import db_forums_funcs

def create(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["name", "short_name", "user"]
        try:
            params_are_right(request=request_data,
                            required=required_data)
            forum = db_forums_funcs.forum_create(name=request_data["name"],
                                                 short_name=request_data["short_name"],
                                                 user=request_data["user"])
        except Exception as e:
            return return_error(e.message)
        return return_response(forum)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":
        request_data = return_GET_params(request)
        required_data = ["forum"]
        related = return_related(request_data)
        try:
            params_are_right(request=request_data,
                            required=required_data)
            forum = db_forums_funcs.forum_details(short_name=request_data["forum"],
                                                  related=related)
        except Exception as e:
            return return_error(e.message)
        return return_response(forum)
    else:
        return HttpResponse(status=400)


def list_threads(request):
    if request.method == "GET":
        request_data = return_GET_params(request)
        required_data = ["forum"]
        related = return_related(request_data)
        optional = return_optional(request=request_data, optional=["limit", "order", "since"])
        try:
            params_are_right(request=request_data,
                            required=required_data)
            threads_l = db_threads_funcs.thread_list(entity="forum",
                                                     entity_attr=request_data["forum"],
                                                     related=related,
                                                     params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(threads_l)
    else:
        return HttpResponse(status=400)


def list_posts(request):
    if request.method == "GET":
        request_data = return_GET_params(request)
        required_data = ["forum"]
        related = return_related(request_data)

        optional = return_optional(request=request_data,
                                optional=["limit", "order", "since"])
        try:
            params_are_right(request=request_data,
                            required=required_data)
            posts_l = db_posts_funcs.post_list(entity="forum",
                                               entity_attr=request_data["forum"],
                                               related=related,
                                               params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(posts_l)
    else:
        return HttpResponse(status=400)


def list_users(request):
    if request.method == "GET":
        request_data = return_GET_params(request)
        required_data = ["forum"]
        optional = return_optional(request=request_data,
                                optional=["limit", "order", "since_id"])
        try:
            params_are_right(request=request_data,
                             required=required_data)
            users_l = db_forums_funcs.forum_list_users(request_data["forum"],
                                                       optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(users_l)
    else:
        return HttpResponse(status=400)