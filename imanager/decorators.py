# -*- coding: utf-8 -*-
from functools import wraps

from django.shortcuts import redirect


def no_require_login(view_func):
    @wraps(view_func)
    def no_login(request, *args, **kwargs):
        if request.user.is_authenticated():
            # Permission Denied!!!
            return redirect("planning:profile_list")
        else:
            response = view_func(request, *args, **kwargs)
        return response
    return wraps(view_func)(no_login)