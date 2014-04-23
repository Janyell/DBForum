from api.db import db_funcs


def thread_subscribe(sub_email, thread_id):
    db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=sub_email)
    db_funcs.db_exist(entity="Threads", entity_attr="id", attr_value=thread_id)
    subscription = subscription_select(sub_email, thread_id)
    if not len(subscription):
        db_funcs.db_insert_or_delete_or_update(
            'INSERT INTO Subscriptions (thread, user)'
            ' VALUES (%s, %s)',
            (thread_id, sub_email, )
        )
        subscription = subscription_select(sub_email, thread_id)
    subscription_response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return subscription_response


def thread_unsubscribe(sub_email, thread_id):
    #db_funcs.db_exist(entity="Users", entity_attr="email", attr_value=sub_email)
    #db_funcs.db_exist(entity="Threads", entity_attr="id", attr_value=thread_id)
    subscription = subscription_select(sub_email, thread_id)
    if not len(subscription):
        raise Exception("thread: user " + sub_email + " don't subscribe thread #" + str(thread_id))
    db_funcs.db_insert_or_delete_or_update(
        'DELETE'
        ' FROM Subscriptions'
        ' WHERE user = %s'
        ' AND thread = %s',
        (sub_email, thread_id, )
    )
    subscription_response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return subscription_response


# Helper functions

def subscription_select(sub_email, thread_id):
    return db_funcs.db_select(
        'SELECT thread, user'
        ' FROM Subscriptions'
        ' WHERE user = %s'
        ' AND thread = %s',
        (sub_email, thread_id, )
    )