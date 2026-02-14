import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


SUCCESS_MESSAGES = {
    200: "Request successful.",
    201: "Resource created successfully.",
    202: "Request accepted for processing.",
    204: "Request completed successfully. No content returned.",
}


ERROR_MESSAGES = {
    400: "Invalid request data.",
    401: "Authentication required or failed.",
    403: "Permission denied.",
    404: "Resource not found.",
    405: "HTTP method not allowed.",
    409: "Resource conflict.",
    422: "Unprocessable entity.",
    429: "Too many requests. Please try again later.",
    500: "Internal server error.",
    502: "Bad gateway.",
    503: "Service temporarily unavailable.",
    504: "Gateway timeout.",
}



def _extract_error_message(data, status_code):
    if isinstance(data, dict):
        detail = data.get("detail")
        if isinstance(detail, str) and detail:
            return detail
        non_field = data.get("non_field_errors")
        if isinstance(non_field, list) and non_field:
            return str(non_field[0])
    return ERROR_MESSAGES.get(status_code, "Erro.")


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        message = _extract_error_message(response.data, response.status_code)
        return Response(
            {
                "success": False,
                "status_code": response.status_code,
                "message": ERROR_MESSAGES.get(response.status_code, "Erro."),
                "errors": response.data,
            },
            status=response.status_code,
        )

    logger.exception("Unhandled exception", exc_info=exc)
    return Response(
        {
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": ERROR_MESSAGES[500],
            "errors": {"detail": "Internal Server Error"},
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None
        status_code = getattr(response, "status_code", None)

        if status_code == status.HTTP_204_NO_CONTENT:
            return super().render(None, accepted_media_type, renderer_context)

        if isinstance(data, dict) and {"success", "status_code", "message"}.issubset(data.keys()):
            return super().render(data, accepted_media_type, renderer_context)

        if status_code is not None and 200 <= status_code < 300:
            envelope = {
                "success": True,
                "status_code": status_code,
                "message": SUCCESS_MESSAGES.get(status_code, "OK"),
                "data": data,
            }
            return super().render(envelope, accepted_media_type, renderer_context)

        return super().render(data, accepted_media_type, renderer_context)
