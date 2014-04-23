from api.funcs import *
from api.db import db_funcs


def clear(request):
    if request.method == "GET":
        try:
           db_funcs.db_clear()
        except Exception as e:
            return return_error(e.message)
        return return_success("db: truncate table success")
    return HttpResponse(status=400)