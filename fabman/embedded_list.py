"""Interface for handling embedded lists of FabmanObjects"""

from typing import List, Optional, Type

from fabman.fabman_object import FabmanObject
from fabman.paginated_list import PaginatedList
from fabman.requester import Requester


class EmbeddedList(object):
    """Mimics the functionality of :code:`fabman.paginated_list.PaginatedList` for embedded objects."""

    def __getitem__(self, index):
        assert isinstance(
            index, int
        ), "Index must be an integer. slicing and keys are not supported"
        if index < 0:
            raise IndexError("Cannot use negative indexing on EmbeddedList")
        return self._elements[index]

    def __init__(  # pylint: disable=too-many-arguments
        self,
        content_class: Type[FabmanObject],
        initial_data: List[dict],
        requester: Requester,
        request_method: Optional[str] = None,
        refresh_endpoint: Optional[str] = None,
        extra_attribs: Optional[dict] = None,
        **kwargs,
    ) -> None:
        """Initializes the EmbeddedList object with sub element and acts as a simple list.
        Has a refresh method to retrieve a PaginatedList from the API.

        :param content_class: Class of the stored objects.
        :type content_class: Type[FabmanObject]
        :param requester: Requester for refreshing the API
        :type requester: fabman.requester.Requester
        :param request_method: One of "GET", "POST", "PUT", "DELETE"
        :type request_method: str
        :param refresh_endpoint: Endpoint for retrieving a Paginated List
        :type refresh_endpoint: str
        :param initial_data: list of Initial data in JSON format
        :type initial_data: List[dict]
        :param extra_attribs: Extra attributes to add to each object, defaults to None
        :type extra_attribs: Optional[dict], optional
        """
        self._elements = []

        for element in initial_data:
            obj = content_class(requester, element)
            if extra_attribs:
                obj.update(extra_attribs)
            self._elements.append(obj)

        self._content_class = content_class
        self._requester = requester
        self._first_params = kwargs or {}
        self._refresh_endpoint = refresh_endpoint
        self._extra_attribs = extra_attribs or {}
        self._request_method = request_method

    def __iter__(self):
        for element in self._elements:
            yield element

    def __repr__(self):
        return f"<EmbeddedList of type {self._content_class.__name__} with {len(self._elements)} elements>"

    def get_live_data(self) -> PaginatedList:
        """Convert the EmbeddedList into a PaginatedList by passing arguments to the
        PaginatedList. The Paginated list will hold no data but will retrieve live
        data as needed.

        :return: PaginatedList to work on current objects
        :rtype: PaginatedList
        """
        if self._refresh_endpoint is None or self._refresh_endpoint == "":
            raise ValueError("Cannot refresh an EmbeddedList without a refresh URL")
        if self._request_method is None or self._request_method == "":
            raise ValueError("Cannot refresh an EmbeddedList without a request method")

        return PaginatedList(
            self._content_class,
            self._requester,
            self._request_method,
            self._refresh_endpoint,
            extra_attribs=self._extra_attribs,
            **self._first_params,
        )
