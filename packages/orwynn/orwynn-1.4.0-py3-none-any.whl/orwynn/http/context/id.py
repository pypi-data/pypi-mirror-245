from pykit import validation
from pykit.rnd import RandomUtils

from orwynn.context import ContextStorage
from orwynn.context.errors import RequestIdAlreadySavedError


class HttpRequestContextId:
    def __init__(self) -> None:
        self.__storage: ContextStorage = ContextStorage.ie()

    def get(
        self
    ) -> str:
        return validation.apply(self.__storage.get("request_id"), str)

    def save(self) -> str:
        """Generates an id for the request and saves it into the context.

        Returns:
            Request id generated.

        Raises:
            RequestIdAlreadySavedError:
                If the request id has been set previously.
        """
        request_id: str = RandomUtils.makeid()
        try:
            self.__storage.get("request_id")
        except KeyError:
            self.__storage.save("request_id", request_id)
            return request_id
        else:
            raise RequestIdAlreadySavedError()
