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
    exc.detail = convert_details_to_string(exc.detail)
    response = exception_handler(exc, context)
    return response

def convert_details_to_string(input_data):
    if isinstance(input_data, str):
        return input_data
    if isinstance(input_data, list):
        return '\n'.join(map(str, input_data))
    if isinstance(input_data, dict):
        return '\n'.join(map(str, input_data.values()))
    return None