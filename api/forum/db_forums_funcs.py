from api.db import db_funcs
from api.user import db_users_func


def forum_create(name, short_name, user):
    db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=user)
    forum = forum_get(short_name)
    if not len(forum):
        db_funcs.db_insert_or_delete_or_update(
            'INSERT INTO Forums (name, short_name, user) '
            'VALUES (%s, %s, %s)',
            (name, short_name, user, )
        )
        forum = forum_get(short_name)
    return forum_describe(forum[0])


def forum_details(short_name, related):
    forum = forum_get(short_name)
    if not len(forum):
        raise ("forum: forum with short_name=" + short_name + " not found")
    forum_response = forum_describe(forum[0])
    if "user" in related:
        forum_response["user"] = db_users_func.user_details(forum_response["user"])
    return forum_response


def forum_list_users(short_name, optional):
    db_funcs.db_exist(entity="Forums", entity_attr="short_name", attr_value=short_name)
    select = "SELECT DISTINCT email" \
             " FROM Users u, Posts p, Forums f" \
             " WHERE p.user = u.email" \
             " AND f.short_name = p.forum" \
             " AND p.forum = %s"
    if "since_id" in optional:
        select += " AND u.id >= " + str(optional["since_id"])
    if "order" in optional:
        select += " ORDER BY u.id " + optional["order"]
    else:
        select += " ORDER BY u.id DESC"
    if "limit" in optional:
        select += " LIMIT " + str(optional["limit"])

    result = db_funcs.db_select(select, (short_name, ))
    list_u = []
    for record in result:
        list_u.append(db_users_func.user_details(record[0]))
    return list_u


# Helper functions

def forum_get(short_name):
    return db_funcs.db_select(
        'SELECT id, name, short_name, user '
        'FROM Forums '
        'WHERE short_name = %s',
        (short_name, )
    )

def forum_describe(forum):
    forum_response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }
    return forum_response