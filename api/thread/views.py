import json

from django.http import HttpResponse

from api.post import db_posts_funcs
from api.thread import db_threads_funcs, db_subscriptions_funcs
from api.funcs import return_response, return_related, params_are_right, return_optional, return_GET_params, return_error


def create(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
        optional = return_optional(request=request_data,
                                   optional=["isDeleted"])
        try:
            params_are_right(request=request_data,
                             required=required_data)
            thread = db_threads_funcs.thread_create(forum=request_data["forum"],
                                                    title=request_data["title"],
                                                    is_closed=request_data["isClosed"],
                                                    user=request_data["user"],
                                                    date=request_data["date"],
                                                    message=request_data["message"],
                                                    slug=request_data["slug"], optional=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":
        request_data = return_GET_params(request)
        required_data = ["thread"]
        related = return_related(request_data)
        try:
            params_are_right(request=request_data,
                             required=required_data)
            thread = db_threads_funcs.thread_details(thread_id=request_data["thread"],
                                                     related=related)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def vote(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread", "vote"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            thread = db_threads_funcs.thread_vote(thread_id=request_data["thread"],
                                                  vote=request_data["vote"])
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def subscribe(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread", "user"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            subscription = db_subscriptions_funcs.thread_subscribe(sub_email=request_data["user"],
                                                                   thread_id=request_data["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(subscription)
    else:
        return HttpResponse(status=400)


def unsubscribe(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread", "user"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            subscription = db_subscriptions_funcs.thread_unsubscribe(sub_email=request_data["user"],
                                                                     thread_id=request_data["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(subscription)
    else:
        return HttpResponse(status=400)


def open(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            thread = db_threads_funcs.thread_close_or_open(thread_id=request_data["thread"],
                                                           is_closed=0)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def close(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            thread = db_threads_funcs.thread_close_or_open(thread_id=request_data["thread"],
                                                           is_closed=1)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def update(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread", "slug", "message"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            thread = db_threads_funcs.thread_update(thread_id=request_data["thread"],
                                                    slug=request_data["slug"],
                                                    message=request_data["message"])
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def remove(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            thread = db_threads_funcs.thread_remove_or_restore(thread_id=request_data["thread"],
                                                               is_deleted=1)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def restore(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            thread = db_threads_funcs.thread_remove_or_restore(thread_id=request_data["thread"],
                                                               is_deleted=0)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def thread_list(request):
    if request.method == "GET":
        request_data = return_GET_params(request)
        entity_attr = None
        try:
            entity_attr = request_data["forum"]
            entity = "forum"
        except KeyError:
            try:
                entity_attr = request_data["user"]
                entity = "user"
            except KeyError:
                return return_error("http: user or forum parameters not setted")
        optional = return_optional(request=request_data, optional=["limit", "order", "since"])
        try:
            t_list = db_threads_funcs.thread_list(entity=entity, entity_attr=entity_attr, related=[], params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(t_list)
    else:
        return HttpResponse(status=400)


def list_posts(request):
    if request.method == "GET":
        request_data = return_GET_params(request)
        required_data = ["thread"]
        entity = "thread"
        optional = return_optional(request=request_data, optional=["limit", "order", "since"])
        try:
            params_are_right(request=request_data, required=required_data)
            p_list = db_posts_funcs.post_list(entity=entity, entity_attr=request_data["thread"], related=[], params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(p_list)
    else:
        return HttpResponse(status=400)