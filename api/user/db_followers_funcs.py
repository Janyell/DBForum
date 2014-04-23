from api.db import db_funcs
from api.user import db_users_func


def user_follow(follower_email, followee_email):
    if follower_email == followee_email:
        raise Exception("followers: follower_email=followee_email=" + follower_email)
    db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=follower_email)
    db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=followee_email)
    follows = follower_select(follower_email, followee_email)
    if not len(follows):
        db_funcs.db_insert_or_delete_or_update(
            'INSERT INTO Followers (follower, followee)'
            ' VALUES (%s, %s)',
            (follower_email, followee_email, )
        )
    return db_users_func.user_details(follower_email)


def user_unfollow(follower_email, followee_email):
    if follower_email == followee_email:
        raise Exception("followers: follower_email=followee_email=" + follower_email)
    db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=follower_email)
    db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=followee_email)
    follows = follower_select(follower_email, followee_email)
    if len(follows):
        db_funcs.db_insert_or_delete_or_update(
            'DELETE'
            ' FROM Followers'
            ' WHERE id= %s',
            (follows[0][0], )
        )
    else:
        raise Exception("followers: following not found")
    return db_users_func.user_details(follower_email)


def user_list_followers_or_following(type_email, type, params):
    db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=type_email)
    if type == "follower":
        where_condition = "followee"
    else:
    # if type == "followee":
        where_condition = "follower"
    select = "SELECT " + type + \
             " FROM Followers f, Users u" \
             " WHERE u.email = f." + type +\
             " AND " + where_condition + " = %s "
    if "since_id" in params:
        select += " AND u.id >= " + str(params["since_id"])
    if "order" in params:
        select += " ORDER BY u.name " + params["order"]
    else:
        select += " ORDER BY u.name DESC"
    if "limit" in params:
        select += " LIMIT " + str(params["limit"])
    followers_ees = db_funcs.db_select(query=select, query_params=(type_email, ))
    list_f = []
    for follower_ee in followers_ees:
        list_f.append(db_users_func.user_details(email=follower_ee[0]))
    return list_f


# Helper functions

def follower_select(follower_email, followee_email):
    return db_funcs.db_select(
        'SELECT id'
        ' FROM Followers'
        ' WHERE follower = %s'
        ' AND followee = %s',
        (follower_email, followee_email, )
    )