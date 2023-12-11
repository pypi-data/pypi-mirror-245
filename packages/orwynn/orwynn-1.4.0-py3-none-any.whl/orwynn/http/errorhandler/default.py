from fastapi.exceptions import RequestValidationError

from orwynn.errorhandler import ErrorHandler
from orwynn.http.errors import HttpException
from orwynn.http.requests import HttpRequest
from orwynn.http.responses import HttpResponse, JsonHttpResponse
from orwynn.proxy.boot import BootProxy


class DefaultRequestValidationErrorHandler(ErrorHandler):
    E = RequestValidationError

    def handle(
        self,
        request: HttpRequest,
        error: RequestValidationError
    ) -> HttpResponse:
        return JsonHttpResponse(
            BootProxy.ie().api_indication.digest(error),
            422
        )


class DefaultErrorHandler(ErrorHandler):
    E = Exception

    def handle(self, request: HttpRequest, error: Exception) -> HttpResponse:
        return JsonHttpResponse(
            BootProxy.ie().api_indication.digest(error),
            400
        )


class DefaultHttpErrorHandler(ErrorHandler):
    E = HttpException

    def handle(
        self, request: HttpRequest, error: HttpException
    ) -> HttpResponse:
        return JsonHttpResponse(
            BootProxy.ie().api_indication.digest(error),
            error.status_code
        )
