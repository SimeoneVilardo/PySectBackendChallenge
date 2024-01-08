import logging
from rest_framework.views import exception_handler

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
    response = exception_handler(exc, context)
    return response
