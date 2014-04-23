from api.db import db_funcs
from api.forum import db_forums_funcs
from api.thread import db_threads_funcs
from api.user import db_users_func


def post_create(date, thread, message, user, forum, optional):
    db_funcs.db_exist(entity="Threads", entity_attr="id", attr_value=thread)
    db_funcs.db_exist(entity="Forums", entity_attr="short_name", attr_value=forum)
    db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=user)
    thread_counter = db_funcs.db_select(
        "SELECT COUNT(t.id)"
        " FROM Threads t, Forums f"
        " WHERE t.forum = f.short_name"
        " AND t.forum = %s"
        " AND t.id = %s",
        (forum, thread, )
    )
    if not thread_counter[0][0]:
        raise Exception("post: thread with id = " + thread + " in forum " + forum + " not found")
    if "parent" in optional:
        parent_counter = db_funcs.db_select(
            "SELECT COUNT(p.id)"
            " FROM Posts p, Threads t"
            " WHERE t.id = p.thread"
            " AND p.id = %s"
            " AND t.id = %s",
            (optional["parent"], thread, )
        )
        if not parent_counter[0][0]:
            raise Exception("post: post with id = " + optional["parent"] + " not found")
    insert = "INSERT INTO Posts (message, user, forum, thread, date"
    values = "(%s, %s, %s, %s, %s"
    params = [message, user, forum, thread, date]
    for is_attr in optional:
        insert += ", " + is_attr
        values += ", %s"
        params.append(optional[is_attr])
    insert += ") VALUES " + values + ")"
    update_threads_posts = "UPDATE Threads SET posts = posts + 1 WHERE id = %s"
    conn = db_funcs.db_connect()
    conn.autocommit(False)
    with conn:
        cursor = conn.cursor()
        try:
            cursor.execute(update_threads_posts, (thread, ))
            cursor.execute(insert, params)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception("Database error: " + e.message)
        post_id = cursor.lastrowid
        cursor.close()
    conn.close()
    post_response = post_select(post_id)
    del post_response["dislikes"]
    del post_response["likes"]
    del post_response["parent"]
    del post_response["points"]
    return post_response


def post_details(post_id, related):
    post_response = post_select(post_id)
    if post_response is None:
        raise Exception("post: post with id = " + post_id + " not found")
    if "user" in related:
        post_response["user"] = db_users_func.user_details(post_response["user"])
    if "thread" in related:
        post_response["thread"] = db_threads_funcs.thread_details(thread_id=post_response["thread"], related=[])
    if "forum" in related:
        post_response["forum"] = db_forums_funcs.forum_details(short_name=post_response["forum"], related=[])
    return post_response


def post_list(entity, entity_attr, related, params):
    if entity == "user":
        db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=entity_attr)
    else:
        if entity == "forum":
            db_funcs.db_exist(entity="Forums", entity_attr="short_name", attr_value=entity_attr)
        else:
        # if entity == "thread":
            db_funcs.db_exist(entity="Threads", entity_attr="id", attr_value=entity_attr)
    select = "SELECT id" \
             " FROM Posts" \
             " WHERE " + entity + " = %s "
    select_params = [entity_attr]
    if "since" in params:
        select += " AND date >= %s"
        select_params.append(params["since"])
    if "order" in params:
        select += " ORDER BY date " + params["order"]
    else:
        select += " ORDER BY date DESC "
    if "limit" in params:
        select += " LIMIT " + str(params["limit"])
    posts = db_funcs.db_select(query=select, query_params=select_params)
    list_p = []
    for post in posts:
        list_p.append(post_details(post_id=post[0], related=related))
    return list_p


def post_remove_or_restore(post_id, status):
    db_funcs.db_exist(entity="Posts", entity_attr="id", attr_value=post_id)
    db_funcs.db_insert_or_delete_or_update(
        "UPDATE Posts "
        "SET isDeleted = %s "
        "WHERE id = %s",
        (status, post_id, )
    )
    post_response = {"post": post_id}
    return post_response


def post_update(post_id, message):
    db_funcs.db_exist(entity="Posts", entity_attr="id", attr_value=post_id)
    db_funcs.db_insert_or_delete_or_update(
        'UPDATE Posts'
        ' SET message = %s'
        ' WHERE id = %s',
        (message, post_id, )
    )
    return post_details(post_id=post_id, related=[])


def post_vote(post_id, vote):
    db_funcs.db_exist(entity="Posts", entity_attr="id", attr_value=post_id)
    if vote == -1:
        db_funcs.db_insert_or_delete_or_update(
            "UPDATE Posts"
            " SET dislikes=dislikes+1, points=points-1"
            " WHERE id = %s",
            (post_id, )
        )
    else:
    # if vote == 1:
        db_funcs.db_insert_or_delete_or_update(
            "UPDATE Posts"
            " SET likes=likes+1, points=points+1"
            " WHERE id = %s",
            (post_id, )
        )
    return post_details(post_id=post_id, related=[])


# Helper functions

def post_select(post_id):
    post = db_funcs.db_select(
        'SELECT date, dislikes, forum, id, isApproved, isDeleted, isEdited, '
        'isHighlighted, isSpam, likes, message, parent, points, thread, user '
        'FROM Posts '
        'WHERE id = %s', (post_id, )
    )
    if not len(post):
        return None
    return post_describe(post[0])


def post_describe(post):
    post_response = {
        'date': str(post[0]),
        'dislikes': post[1],
        'forum': post[2],
        'id': post[3],
        'isApproved': bool(post[4]),
        'isDeleted': bool(post[5]),
        'isEdited': bool(post[6]),
        'isHighlighted': bool(post[7]),
        'isSpam': bool(post[8]),
        'likes': post[9],
        'message': post[10],
        'parent': post[11],
        'points': post[12],
        'thread': post[13],
        'user': post[14],
    }
    return post_response
