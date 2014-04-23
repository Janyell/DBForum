from api.db import db_funcs
from api.forum import db_forums_funcs
from api.user import db_users_func


def thread_close_or_open(thread_id, is_closed):
    db_funcs.db_exist(entity="Threads", entity_attr="id", attr_value=thread_id)
    db_funcs.db_insert_or_delete_or_update(
        "UPDATE Threads"
        " SET isClosed = %s"
        " WHERE id = %s",
        (is_closed, thread_id, )
    )
    thread_response = {
        "thread": thread_id
    }
    return thread_response


def thread_create(forum, title, is_closed, user, date, message, slug, optional):
    db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=user)
    db_funcs.db_exist(entity="Forums", entity_attr="short_name", attr_value=forum)
    is_deleted = 0
    if "isDeleted" in optional:
        is_deleted = optional["isDeleted"]
    thread = thread_select(slug)
    if not len(thread):
        db_funcs.db_insert_or_delete_or_update(
            'INSERT INTO Threads (forum, title, isClosed, user, date, message, slug, isDeleted)'
            ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (forum, title, is_closed, user, date, message, slug, is_deleted, )
        )
        thread = thread_select(slug)
    thread_response = thread_describe(thread[0])
    del thread_response["dislikes"]
    del thread_response["likes"]
    del thread_response["points"]
    del thread_response["posts"]
    return thread_response


def thread_details(thread_id, related):
    thread = db_funcs.db_select(
        'SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts'
        ' FROM Threads'
        ' WHERE id = %s',
        (thread_id, )
    )
    if not len(thread):
        raise Exception('thread: thread with id=' + str(thread_id) + " not found")
    thread_response = thread_describe(thread[0])
    if "user" in related:
        thread_response["user"] = db_users_func.user_details(thread_response["user"])
    if "forum" in related:
        thread_response["forum"] = db_forums_funcs.forum_details(short_name=thread_response["forum"], related=[])
    return thread_response


def thread_list(entity, entity_attr, related, params):
    if entity == "forum":
        db_funcs.db_exist(entity="Forums", entity_attr="short_name", attr_value=entity_attr)
    else:
    # if entity == "user":
        db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=entity_attr)
    select = "SELECT id" \
             " FROM Threads" \
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

    threads = db_funcs.db_select(query=select, query_params=select_params)
    list_t = []
    for thread in threads:
        list_t.append(thread_details(thread_id=thread[0], related=related))
    return list_t


def thread_remove_or_restore(thread_id, is_deleted):
    db_funcs.db_exist(entity="Threads", entity_attr="id", attr_value=thread_id)
    db_funcs.db_insert_or_delete_or_update(
        "UPDATE Threads"
        " SET isDeleted = %s"
        " WHERE id = %s",
        (is_deleted, thread_id, )
    )
    thread_response = {
        "thread": thread_id
    }
    return thread_response


def thread_update(thread_id, slug, message):
    db_funcs.db_exist(entity="Threads", entity_attr="id", attr_value=thread_id)
    db_funcs.db_insert_or_delete_or_update(
        'UPDATE Threads'
        ' SET slug = %s, message = %s'
        ' WHERE id = %s',
        (slug, message, thread_id, )
    )
    return thread_details(thread_id=thread_id, related=[])


def thread_vote(thread_id, vote):
    db_funcs.db_exist(entity="Threads", entity_attr="id", attr_value=thread_id)
    if vote == -1:
        db_funcs.db_insert_or_delete_or_update(
            "UPDATE Threads"
            " SET dislikes = dislikes + 1, points = points - 1"
            " WHERE id = %s",
            (thread_id, )
        )
    else:
    # if vote == 1:
        db_funcs.db_insert_or_delete_or_update(
            "UPDATE Threads"
            " SET likes = likes + 1, points = points + 1"
            " WHERE id = %s",
            (thread_id, )
        )
    return thread_details(thread_id=thread_id, related=[])


# Helper functions

def thread_select(slug):
    return db_funcs.db_select(
        'SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts'
        ' FROM Threads'
        ' WHERE slug = %s',
        (slug, )
    )


def thread_describe(thread):
    return {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
        'dislikes': thread[9],
        'likes': thread[10],
        'points': thread[11],
        'posts': thread[12],
    }