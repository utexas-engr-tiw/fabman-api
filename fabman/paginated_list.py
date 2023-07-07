"""Handles pagination of the api"""
from typing import List, Optional, Type

from requests.structures import CaseInsensitiveDict

from fabman.fabman_object import FabmanObject
from fabman.requester import Requester


# TODO: kwargs are not coming through correctly, so commands for pagination are not working
class PaginatedList(object):  # pylint: disable=too-many-instance-attributes
    """
    Abstracts pagination and rate limiting of the Fabman API.
    Documentation: https://github.com/FabmanHQ/fabman-api#pagination
    """

    def __getitem__(self, index):
        assert isinstance(
            index, int
        ), "Index must be an integer, slicing and keys are \
            not supported"
        if index < 0:
            raise IndexError("Cannot use negative indexing on PaginatedList")
        self._get_up_to_index(index)
        return self._elements[index]

    def __init__(  # pylint: disable=too-many-arguments
        self,
        content_class: Type[FabmanObject],
        requester: Requester,
        request_method: str,
        first_url: str,
        extra_attribs: Optional[dict] = None,
        _root: Optional[str] = None,
        url_override: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Abstracts pagination of the Fabman API. Provides a simple interface to work with
        objects and requests new objects from the API as needed.

        :param content_class: Class of the stored objects. Must inherit from FabmanObject
        :type content_class: Type[fabman.fabman_object.FabmanObject]
        :param requester: Requester for refreshing the API
        :type requester: fabman.requester.Requester
        :param request_method: One of "GET", "POST", "PUT", "DELETE"
        :type request_method: str
        :param first_url: endpoint to be called for the first page
        :type first_url: str
        :param extra_attribs: Extra attributes to be added to :code:`content_class`, defaults to None
        :type extra_attribs: Optional[dict], optional
        :param _root: Root endpoint without parameters, defaults to None
        :type _root: str, optional
        :param url_override: Override the base_url, defaults to None
        :type url_override: str, optional
        """

        self._elements = []

        self._content_class = content_class
        self._requester = requester
        self._first_url = first_url
        self._first_params = kwargs or {}
        self._next_url = first_url
        self._next_params = self._first_params
        self._extra_attribs = extra_attribs or {}
        self._root = _root
        self._request_method = request_method
        self._url_override = url_override

    def __iter__(self):
        for element in self._elements:
            yield element
        while self._has_next():
            new_elements = self._grow()
            for element in new_elements:
                yield element

    def __repr__(self):
        return f"<PaginatedList of type {self._content_class.__name__}>"

    @staticmethod
    def __format_link(headers: CaseInsensitiveDict):
        if "link" in headers.keys():
            link = headers["link"]
            return link.split(";")[0].strip("<>").split("/api/v1")[1]

        return None

    def _get_next_page(self):
        response = self._requester.request(
            self._request_method,
            self._next_url,
            _url=self._url_override,
            _kwargs=self._next_params,
        )

        data = response.json()
        headers = response.headers
        self._next_url = self.__format_link(headers)

        content = []

        for element in data:
            if element is not None:
                element.update(self._extra_attribs)
                content.append(self._content_class(self._requester, element))

        return content

    def _get_up_to_index(self, index):
        while len(self._elements) <= index and self._has_next():
            self._grow()

    def _grow(self):
        new_elements = self._get_next_page()
        self._elements.extend(new_elements)
        return new_elements

    def _has_next(self):
        return self._next_url is not None
