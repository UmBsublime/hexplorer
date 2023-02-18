from typing import Any, Dict, List, Union

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
        self.base_log = f"<cyan>{self.__class__.__name__:18}</cyan><white>|</white>"

    @staticmethod
    def __create_object(response: Union[Dict, List], obj: Any) -> Any:

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
        
        try:
            if response.ok:
                return response
            elif response.status_code == 400:
                raise ApiBadRequestError(msg)
            elif response.status_code in [401, 403]:
                raise ApiUnauthorizedError(msg)
            elif response.status_code == 404:
                raise ApiResourceNotFoundError(msg)
            elif response.status_code == 429:
                raise ApiRateLimitExceededError(msg)
            else:
                raise ApiFailledToGetResponse(msg)
        except Exception as e:
            logger.opt(colors=True).warning(f"{msg} <magenta>{response.json()['status']['message']}</magenta>")
            raise e
        finally:
            logger.trace(response.json())

    def _request_object(self, api_url: str, method: HTTP_method, endpoint: str, obj: Any, data: Dict = None) -> Any:
        response = self.__make_request(api_url, method, endpoint, data)
        logger.opt(colors=True).debug(
            f"{self.base_log} {response.status_code} {method.name} {self.__gen_url(api_url, endpoint)} <green>{obj.__name__}</green>"
        )
        return self.__create_object(
            response.json(),
            obj,
        )
