"""The Requester module handles all requests to the API. This should not be used 
or called directly as it is meant to be used internally. All accesses should be
made directly through the Fabman class found in fabman/fabman.py
"""
import logging
from datetime import datetime
from pprint import pformat
from typing import Optional, List

import requests

from fabman.util import clean_headers
from fabman.exceptions import (
    BadRequest,
    InvalidAccessToken,
    Unauthorized,
    ResourceDoesNotExist,
    FabmanException,
    ForbiddenError,
    Conflict,
    UnprocessableEntity,
    RateLimitExceeded,
)


logger = logging.getLogger(__name__)


class Requester(object):
    """Main class responsible for handling all http requests to the API.
    Based on canvasapi.requester.Requester found at 
    https://github.com/ucfopen/canvasapi/blob/develop/canvasapi/requester.py
    """

    def __init__(self, base_url: str, access_token: str) -> None:
        """_summary_

        Args:
            base_url (str): The base url of Fabman API. Should simply https://api.fabman.io/v1
            access_token (_type_): Access token to access the API
        """

        self.base_url = base_url
        self.__access_token = access_token
        self.__session = requests.Session()
        self.__cache = []

    def _delete_request(self, url: str, headers: dict,
                        data: Optional[List] = None, **kwargs) -> requests.Response:
        """Handles a delete request to the API. Should never be called directly

        Args:
            url (str): url for the request
            headers (dict): dictionary of headers
            data (_type_, optional): data as part of the delete requests. Defaults to None.

        Returns:
            requests.Response
        """

        return self.__session.delete(url, headers=headers, data=data, **kwargs)

    def _get_request(self, url: str, headers: dict,
                     params: Optional[List] = None, **kwargs) -> requests.Response:
        """Handles a get request to the API. Should never be called directly

        Args:
            url (str): url for the request
            headers (dict): dictionary of headers
            params (List, optional): dictionary of parameters. Defaults to None.
        Returns:

            requests.Response
        """

        return self.__session.get(url, headers=headers, params=params, **kwargs)

    def _patch_request(self, url: str, headers: dict,
                       data: Optional[List] = None, **kwargs) -> requests.Response:
        """Handles a patch request to the API. Should never be called directly

        Args:
            url (str): url for the request
            headers (dict): dictionary of headers
            data (dict, optional): dictionary of data. Defaults to None.

        Returns:
            requests.Response
        """

        return self.__session.patch(url, headers=headers, data=data, **kwargs)

    def _post_request(self, url: str, headers: dict,
                      data: Optional[List] = None, **kwargs) -> requests.Response:
        """Handles a post request to the API. Should never be called directly

        Args:
            url (str): url for the request
            headers (dict): dictionary of headers
            data (dict, optional): dictionary of data. Defaults to None.

        Returns:
            requests.Response
        """

        return self.__session.post(url, headers=headers, data=data, **kwargs)

    def _put_request(self, url: str, headers: dict,
                     data: Optional[List] = None, **kwargs) -> requests.Response:
        """Handles a put request to the API. Should never be called directly

        Args:
            url (str): url for the request
            headers (dict): dictionary of headers
            data (dict, optional): dictionary of data. Defaults to None.
        """

        return self.__session.put(url, headers=headers, data=data, **kwargs)

    def request(self, method: str, endpoint: Optional[str] = None,
                headers: Optional[dict] = None, use_auth: Optional[bool] = True,
                _url: Optional[str] = None, _kwargs: Optional[dict] = None,
                json: Optional[bool] = False, **kwargs
                ):
        """Main method for handling requests to the API. Should never be called directly except for 
        testing or from the Fabman class.

        Args:
            method (str): Method to be declared. Should be one of GET, POST, PUT, PATCH, DELETE
            endpoint (Optional[str], optional): Endpoint of the api to call. Defaults to None.
            headers (Optional[dict], optional): Any special headers to be added to the request. 
            Authorization headers are automatically handled. Defaults to None.
            use_auth (Optional[bool], optional): Should the api call use authorization? Should be 
            true in almost any case. Defaults to True.
            _url (Optional[str], optional): URL to call, should be None in most cases. Defaults 
            to None.
            _kwargs (Optional[List], optional): Any special kwargs to use inside of the call. 
            Defaults to None.
            json (Optional[bool], optional): Sending dict or json? Defaults to False.

        Raises:
            ValueError
            BadRequest
            InvalidAccessToken
            Unauthorized
            ForbiddenError
            ResourceDoesNotExist
            Conflict
            UnprocessableEntity
            FabmanException

        Returns:
            _type_: _description_
        """
        full_url = _url if _url else f"{self.base_url}/{endpoint}"

        if not headers:
            headers = {}

        if use_auth:
            auth_header = {"Authorization": f"Bearer {self.__access_token}"}
            headers.update(auth_header)

        # Determine the appropriate request method.
        if method == "GET":
            req_method = self._get_request
        elif method == "POST":
            req_method = self._post_request
        elif method == "DELETE":
            req_method = self._delete_request
        elif method == "PUT":
            req_method = self._put_request
        elif method == "PATCH":
            req_method = self._patch_request
        else:
            raise ValueError(f"Invalid method {method}")

        logger.info("Request: %s %s", method, full_url)
        logger.debug(
            "Headers %s", pformat(clean_headers(headers),
                                  indent=2, width=80, compact=True)
        )

        response = req_method(full_url, headers, _kwargs, json=json)
        logger.info(
            "Response: %s %s %s", method, full_url, response.status_code
        )
        logger.debug(
            "Headers: %s",
            pformat(clean_headers(response.headers))
        )

        try:
            logger.debug(
                "Data: %s", pformat(response.content.decode("utf-8"))
            )
        except UnicodeDecodeError:
            logger.debug("Data: %s", pformat(response.content))
        except AttributeError:
            # Response has no content
            logger.debug("No data")

        # add response to cache
        if len(self.__cache) > 4:
            self.__cache.pop()
        self.__cache.insert(0, response)

        # Raise for status codes
        if response.status_code == 400:
            raise BadRequest(response.text)
        elif response.status_code == 401:
            if "WWW-Authenticate" in response.headers:
                raise InvalidAccessToken(response.json())
            else:
                raise Unauthorized(response.json())
        elif response.status_code == 403:
            raise ForbiddenError(response.json())
        elif response.status_code == 404:
            raise ResourceDoesNotExist("Not found")
        elif response.status_code == 409:
            raise Conflict(response.text)
        elif response.status_code == 422:
            raise UnprocessableEntity(response.text)
        elif response.status_code == 429:
            raise RateLimitExceeded(response.text)
        elif response.status_code > 400:
            # catch all for other codes
            raise FabmanException(
                f"Encountered an error: status code {response.status_code}"
            )

        return response
