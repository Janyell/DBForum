from api.db import db_funcs


def user_create(email, username, about, name, optional):
    is_anonymous = 0
    if "isAnonymous" in optional:
        is_anonymous = optional["isAnonymous"]
    try:
        user = user_select(email)
        if not len(user):
            db_funcs.db_insert_or_delete_or_update(
                'INSERT INTO Users (email, about, name, username, isAnonymous)'
                ' VALUES (%s, %s, %s, %s, %s)',
                (email, about, name, username, is_anonymous, )
            )
            user = user_select(email)
    except Exception as e:
        raise Exception(e.message)
    return user_describe(user[0])


def user_details(email):
    db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=email)
    user = user_select(email)
    if not len(user):
        raise Exception("user: user with email " + email + " not found")
    user_response = user_describe(user[0])
    user_response["followers"] = user_follower(email, "follower")
    user_response["following"] = user_follower(email, "followee")
    list_s = []
    subscriptions = db_funcs.db_select(
        'SELECT thread'
        ' FROM Subscriptions'
        ' WHERE user = %s',
        (email, )
    )
    for sub in subscriptions:
        list_s.append(sub[0])
    user_response["subscriptions"] = list_s
    return user_response


def user_follower(email, type):
    if type == "follower":
        where_condition = "followee"
    else:
    # if type == "followee":
        where_condition = "follower"
    followers_ees = db_funcs.db_select(
        "SELECT " + type +
        " FROM Followers f, Users u"
        " WHERE u.email = f." + type +
        " AND " + where_condition + " = %s ",
        (email, )
    )
    list_f = []
    for follower_ee in followers_ees:
        list_f.append(follower_ee[0])
    return list_f


def user_update_profile(email, about, name):
    db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=email)
    db_funcs.db_insert_or_delete_or_update(
        'UPDATE Users'
        ' SET about = %s, name = %s'
        ' WHERE email = %s',
        (about, name, email, )
    )
    return user_details(email)


# Helper functions

def user_select(email):
    return db_funcs.db_select(
        'SELECT email, about, isAnonymous, id, name, username'
        ' FROM Users'
        ' WHERE email = %s',
        (email, )
    )


def user_describe(user):
    user_response = {
        'about': user[1],
        'email': user[0],
        'id': user[3],
        'isAnonymous': bool(user[2]),
        'name': user[4],
        'username': user[5]
    }
    return user_response