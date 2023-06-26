#!/usr/bin/python3
"""Main file for the Fabman API library.
"""

import warnings

from fabman.member import Member
from fabman.paginated_list import PaginatedList
from fabman.requester import Requester
from fabman.resources import Resource


class Fabman(object):
    """
    The main class to be instantiated to provide access to the Fabman api.
    """

    def __init__(self, access_token, base_url="https://fabman.io/api/v1"):
        """Initializes the Fabman class with the given access token and base url.
        All methods take kwargs as their arguments, please refer to the Fabman API
        for more information

        Args:
            access_token (str): The access token to access the API
            base_url (str, optional): The base url of the API. Defaults to
            "https://api.fabman.io/v1".
        """

        if "https://" not in base_url:
            warnings.warn(
                "Please use HTTPS when possible. Fabman API may not respond as intended and user"
                "data will not be secure",
                UserWarning
            )

        if "://" not in base_url:
            warnings.warn(
                "An invalid `bad_url` provided. Will likely not work as intended.",
                UserWarning
            )
        if not access_token or access_token == "":
            raise ValueError("No access token provided")

        # sanitize access token and base url
        access_token = access_token.strip()
        if base_url[-1] == "/":
            base_url = base_url[:-1]

        self.__requester = Requester(base_url, access_token)

    def create_member(self, member_data, **kwargs) -> Member:
        """Creates a new member in the Fabman database.
        Calls "POST /members"
        Documentation: https://fabman.io/api/v1/documentation#/members/postMembers

        Returns:

        """
        uri = f"/members"
        
        response = self.__requester.request(
            "POST", uri, _kwargs=member_data
        )
        
        return Member(self.__requester, response.json())
        

    def get_members(self, **kwargs):
        """Get all of the members in the Fabman database. Can specify filters,
        search string, result limits, offsets, and sorting. Refer to the Fabman API
        documentation.

        calls "GET /members"
        documentation https://fabman.io/api/v1/documentation#/members/getMembers
        """
        
        return PaginatedList(
            Member,
            self.__requester,
            "GET",
            "/members",
        )

    def get_member(self, member_id: int, **kwargs):
        """Retrieves a member from the API give their id
        calls "GET /members/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersId

        Args:
            member_id (int): ID of the member to be called
        """
        uri = f"/members/{member_id}"

        response = self.__requester.request(
            "GET", uri, _kwargs=kwargs
        )

        return Member(self.__requester, response.json())

    def get_resources(self, **kwargs):
        """
        Get list of available resources (e.g. doors, printers, etc.) Limit, offset,
        and a number of filters are available. Refer to the appropriate documentation.
        calls "GET /resources"
        Documentation: https://fabman.io/api/v1/documentation#/resources/getResources
        """
        raise NotImplementedError("get_resources not implemented yet. Awaiting Pagination")

    def get_resource(self, resource_id: int, **kwargs):
        """
        Get a single resource by its ID. Embed information is also available.
        
        Calls "GET /resources/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/resources/getResourcesId
        """
        uri = f"/resources/{resource_id}"

        response = self.__requester.request(
            "GET", uri, _kwargs=kwargs
        )

        return Resource(self.__requester, response.json())

    def get_user(self, **kwargs):
        """Gets authenticated user information from the API as Member object. Does
        not returns state and superuser information.
        calls "GET /user/me"
        Documentation: https: // fabman.io/api/v1/documentation  # /user/getUserMe
        """
        uri = "/user/me"

        response = self.__requester.request(
            "GET", uri, _kwargs=kwargs
        )

        return Member(self.__requester, response.json()["members"][0])
