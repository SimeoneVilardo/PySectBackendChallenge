from typing import Type

from django.http import HttpResponseNotAllowed
from django.views import View
from django.views.decorators.csrf import csrf_exempt


def create_dispatcher_view(views_by_method: dict[str, Type[View]]):
    """
    This creates a dispatcher view which is used to dispatch the requests to the appropriate views
    considering http verb used. Use this if you have an url shared between multiple verbs, and you want to match on view
    for each tuple (verb, url) where verb it's GET, PUT, etc.

    One view per (verb, url) makes the code more readable and maintainable, 'cause in the views the listed attributes
    and methods are those required ONLY for a specific action.

    Example:
        path('foo/bar', create_dispatcher_view({
                    'DELETE': ResourceManageDeleteView,
                    'GET': ResourceManageListView,
                    'PUT': ResourceManageUpdateView,
                })

    Args:
        views_by_method: dict mapping http methods (POST, GTE, etc.) to a specific view

    Returns:
        the dispatcher to use in a django path

    """

    @csrf_exempt
    def dispatcher(request, *args, **kwargs):
        if request.method not in views_by_method:
            return HttpResponseNotAllowed(views_by_method.keys())
        return views_by_method[request.method].as_view()(request, *args, **kwargs)

    return dispatcher
