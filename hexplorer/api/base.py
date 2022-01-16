from typing import Any, Dict, List, Tuple, Union

import requests
from loguru import logger

from hexplorer.api.exceptions import (ApiBadRequestError,
                                      ApiFailledToGetResponse,
                                      ApiRateLimitExceededError,
                                      ApiResourceNotFoundError,
                                      ApiUnauthorizedError)
from hexplorer.constants import HTTP_method


class Api:
    base_url: str = "http://example.com"
    base_endpoint: str = ""
    session: requests.Session = requests.session()

    def __init__(self) -> None:
        self.base_log = f"{self.__class__.__module__}.{self.__class__.__name__}"

    @staticmethod
    def __create_object(response: Union[Dict, List], obj: Any) -> Union[Dict, List]:

        logger.trace(response)
        if obj == type(response):
            # If obj is already the right type simply return it
            return response
        elif isinstance(response, list):
            # If the response is a list, but we requested obj, return a list of obj
            return [obj(**r) for r in response]
        else:
            # Default to returning an obj of the result
            return obj(**response)

    def __gen_url(self, api_url: str, path: str) -> str:
        return f"{api_url}/{self.base_endpoint}/{path}"

    def __make_request(self, api_url: str, method: HTTP_method, endpoint: str, data: Dict = None) -> requests.Response:
        url = self.__gen_url(api_url, endpoint)
        req = requests.Request(method.name, url, data=data)
        prepped = self.session.prepare_request(req)
        response = self.session.send(prepped)
        msg = f"{self.base_log} {response.status_code} {method.name} {url}"
        logger.trace(response)
        if response.ok:
            return response
        elif response.status_code == 400:
            logger.warning(f"{msg}{response.json()['status']['message']}")
            raise ApiBadRequestError(msg)
        elif response.status_code in [401, 403]:
            logger.warning(f"{msg}")
            raise ApiUnauthorizedError(msg)
        elif response.status_code == 404:
            logger.warning(f"{msg}")
            raise ApiResourceNotFoundError(msg)
        elif response.status_code == 429:
            logger.warning(msg)
            raise ApiRateLimitExceededError(msg)
        else:
            logger.warning(msg)
            raise ApiFailledToGetResponse(msg)

    def _request_object(self, api_url: str, method: HTTP_method, endpoint: str, obj: Any, data: Dict = None) -> Any:
        response = self.__make_request(api_url, method, endpoint, data)
        logger.debug(
            f"{self.base_log} {response.status_code} {method.name} {self.__gen_url(api_url, endpoint)} {obj.__name__}"
        )
        return self.__create_object(
            response.json(),
            obj,
        )
