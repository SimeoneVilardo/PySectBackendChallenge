import logging
from django.core.exceptions import PermissionDenied
from django.db import connections
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    request = context["request"]
    logger.exception(
        f"""
        Exception occurred during processing request:
        Method: {request.method}
        Path: {request.get_full_path()}
        User: {request.user}
        Auth: {request.auth}
        Headers: {dict(request.headers)}
        GET Params: {dict(request.GET)}
        POST Params: {dict(request.POST)}
        Body: {str(request.data)}
        Exception: {exc}
        """
    )
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        exc.detail = convert_details_to_string(exc.detail)
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None

def set_rollback():
    for db in connections.all():
        if db.settings_dict['ATOMIC_REQUESTS'] and db.in_atomic_block:
            db.set_rollback(True)

def convert_details_to_string(details):
    if isinstance(details, str):
        return details
    if isinstance(details, list):
        return '\n'.join(map(str, details))
    if isinstance(details, dict):
        return '\n'.join(map(str, details.values()))
    return None