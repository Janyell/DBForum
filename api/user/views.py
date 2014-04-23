import json

from django.http import HttpResponse

from api.post import db_posts_funcs
from api.user import db_users_func, db_followers_funcs
from api.funcs import return_response, params_are_right, return_optional, return_GET_params, return_error


def create(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["email", "username", "name", "about"]
        optional = return_optional(request=request_data,
                                   optional=["isAnonymous"])
        try:
            params_are_right(request=request_data,
                             required=required_data)
            user = db_users_func.user_create(email=request_data["email"],
                                             username=request_data["username"],
                                             about=request_data["about"],
                                             name=request_data["name"],
                                             optional=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(user)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":
        request_data = return_GET_params(request)
        required_data = ["user"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            user_details = db_users_func.user_details(email=request_data["user"])
        except Exception as e:
            return return_error(e.message)
        return return_response(user_details)
    else:
        return HttpResponse(status=400)


def follow(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["follower", "followee"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            following = db_followers_funcs.user_follow(follower_email=request_data["follower"],
                                                       followee_email=request_data["followee"])
        except Exception as e:
            return return_error(e.message)
        return return_response(following)
    else:
        return HttpResponse(status=400)


def unfollow(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["follower", "followee"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            following = db_followers_funcs.user_unfollow(follower_email=request_data["follower"],
                                                         followee_email=request_data["followee"])
        except Exception as e:
            return return_error(e.message)
        return return_response(following)
    else:
        return HttpResponse(status=400)


def list_followers(request):
    if request.method == "GET":
        request_data = return_GET_params(request)
        required_data = ["user"]
        followers_param = return_optional(request=request_data,
                                          optional=["limit", "order", "since_id"])
        try:
            params_are_right(request=request_data, required=required_data)
            follower_l = db_followers_funcs.user_list_followers_or_following(type_email=request_data["user"],
                                                                             type="follower", params=followers_param)
        except Exception as e:
            return return_error(e.message)
        return return_response(follower_l)
    else:
        return HttpResponse(status=400)


def list_following(request):
    if request.method == "GET":
        request_data = return_GET_params(request)
        required_data = ["user"]
        followers_param = return_optional(request=request_data,
                                          optional=["limit", "order", "since_id"])
        try:
            params_are_right(request=request_data,
                             required=required_data)
            followings = db_followers_funcs.user_list_followers_or_following(type_email=request_data["user"],
                                                                             type="followee", params=followers_param)
        except Exception as e:
            return return_error(e.message)
        return return_response(followings)
    else:
        return HttpResponse(status=400)


def list_posts(request):
    if request.method == "GET":
        request_data = return_GET_params(request)
        required_data = ["user"]
        optional = return_optional(request=request_data,
                                   optional=["limit", "order", "since"])
        try:
            params_are_right(request=request_data,
                             required=required_data)
            posts_l = db_posts_funcs.post_list(entity="user",
                                               entity_attr=request_data["user"],
                                               related=[],
                                               params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(posts_l)
    else:
        return HttpResponse(status=400)


def update(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["user", "name", "about"]
        try:
            params_are_right(request=request_data,
                             required=required_data)
            user = db_users_func.user_update_profile(email=request_data["user"],
                                                     name=request_data["name"],
                                                     about=request_data["about"])
        except Exception as e:
            return return_error(e.message)
        return return_response(user)
    else:
        return HttpResponse(status=400)