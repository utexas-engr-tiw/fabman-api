"""The Requester module handles all requests to the API. This should not be used 
or called directly as it is meant to be used internally. All accesses should be
made directly through the Fabman class found in fabman/fabman.py
"""
import logging
import warnings
from pprint import pformat
from time import sleep
from typing import Optional

import requests

from fabman.exceptions import (
    BadRequest,
    Conflict,
    FabmanException,
    ForbiddenError,
    InvalidAccessToken,
    RateLimitExceeded,
    ResourceDoesNotExist,
    Unauthorized,
    UnprocessableEntity,
)
from fabman.util import clean_headers

logger = logging.getLogger(__name__)

CACHE_SIZE = 4


class Requester(object):
    """Main class responsible for handling all http requests to the API.
    Based on canvasapi.requester.Requester found at
    https://github.com/ucfopen/canvasapi/blob/develop/canvasapi/requester.py
    """

    def __init__(self, base_url: str, access_token: str) -> None:
        """
        :param base_url: The base URL of the Fabman instance's API.
        :type base_url: str
        :param access_token: The API key to authenticate requests with.
        :type access_token: str
        """

        self.base_url = base_url
        self.__access_token = access_token
        self.__session = requests.Session()
        self.__cache = []

    def _delete_request(
        self, url: str, headers: dict, data: Optional[dict] = None, **kwargs
    ) -> requests.Response:
        """
        Handles a delete request to the API. Should never be called directly
        """

        return self.__session.delete(url, headers=headers, data=data, **kwargs)

    def _get_request(
        self, url: str, headers: dict, params: Optional[dict] = None, **kwargs
    ) -> requests.Response:
        """
        Handles a get request to the API. Should never be called directly
        """

        return self.__session.get(url, headers=headers, params=params, **kwargs)

    def _post_request(
        self, url: str, headers: dict, data: Optional[dict] = None, **kwargs
    ) -> requests.Response:
        """
        Handles a post request to the API. Should never be called directly
        """

        return self.__session.post(url, headers=headers, data=data, **kwargs)

    def _put_request(
        self, url: str, headers: dict, data: Optional[dict] = None, **kwargs
    ) -> requests.Response:
        """
        Handles a put request to the API. Should never be called directly
        """

        return self.__session.put(url, headers=headers, data=data, **kwargs)

    def request(
        self,
        method: str,
        endpoint: Optional[str] = None,
        headers: Optional[dict] = None,
        use_auth: Optional[bool] = True,
        _url: Optional[str] = None,
        _kwargs: Optional[dict] = None,
        json: Optional[bool] = False,
        **kwargs,
    ) -> requests.Response:
        """
        Main method for handling requests to the API. Should never be called directly except for
        testing or from the Fabman class.

        :param method: The HTTP method to use for the request.
        :type method: str
        :param endpoint: The API endpoint to call.
        :type endpoint: str
        :param headers: HTTP headers to send with the request.
        :type headers: dict
        :param use_auth: Whether or not to include the access token in the request.
        :type use_auth: bool
        :param _url: The full URL to use for the request. This overrides the base_url and endpoint.
        :type _url: str
        :param _kwargs: Keyword arguments from the calling argument. These are morphed into the params or body of the request depending on :code:`method`.
        :type _kwargs: dict
        :param json: Whether or not to send the data as JSON.
        :type json: bool

        :return: The response object if the call was successful
        :rtype: requests.Response
        """
        full_url = _url if _url else f"{self.base_url}{endpoint}"

        if not headers:
            headers = {}

        if use_auth:
            auth_header = {"Authorization": f"Bearer {self.__access_token}"}
            headers.update(auth_header)

        # Add kwargs to _kwargs
        if _kwargs is None:
            _kwargs = kwargs
        else:
            _kwargs.update(kwargs)

        # Determine the appropriate request method.
        if method == "GET":
            req_method = self._get_request
        elif method == "POST":
            req_method = self._post_request
        elif method == "DELETE":
            req_method = self._delete_request
        elif method == "PUT":
            req_method = self._put_request
        else:
            raise ValueError(f"Invalid method {method}")

        logger.info("Request: %s %s", method, full_url)
        logger.debug(
            "Headers %s",
            pformat(clean_headers(headers), indent=2, width=80, compact=True),
        )

        response = req_method(full_url, headers, _kwargs, json=json)
        logger.info("Response: %s %s %s", method, full_url, response.status_code)
        logger.debug("Headers: %s", pformat(clean_headers(response.headers)))

        try:
            logger.debug("Data: %s", pformat(response.content.decode("utf-8")))
        except UnicodeDecodeError:
            logger.debug("Data: %s", pformat(response.content))
        except AttributeError:
            # Response has no content
            logger.debug("No data")

        # add response to cache
        if len(self.__cache) >= CACHE_SIZE:
            self.__cache.pop()
        self.__cache.insert(0, response)

        # Raise for status codes
        if response.status_code == 400:
            raise BadRequest(response.text)
        if response.status_code == 204:
            if method != "DELETE":
                warnings.warn(
                    "204 No Content returned. This likely means there is no information"
                    "at the resource.",
                    UserWarning,
                )
            return response
        if response.status_code == 401:
            if "WWW-Authenticate" in response.headers:
                raise InvalidAccessToken(response.json())
            raise Unauthorized(response.json())
        if response.status_code == 403:
            raise ForbiddenError(response.json())
        if response.status_code == 404:
            raise ResourceDoesNotExist("Not found")
        if response.status_code == 409:
            raise Conflict(response.text)
        if response.status_code == 422:
            raise UnprocessableEntity(response.text)
        # rate limit is number of request/second at time of writing. Unable to hit the
        # rate limit on home connection to verify this handling works. May break in the future.
        if response.status_code == 429:
            raise RateLimitExceeded(
                "Rate Limit Exceeded. Too many requests in a short amount of time. Retry in at least 2 seconds."
                "https://github.com/FabmanHQ/fabman-api#rate-limiting"
            )

        if response.status_code > 400:
            # catch all for other (bad)codes
            raise FabmanException(
                f"Encountered an error: status code {response.status_code}"
            )

        return response
