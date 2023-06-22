#!/usr/bin/python3
"""Main file for the Fabman API library.
"""

import warnings

from fabman.util import combine_kwargs
from fabman.requester import Requester
from fabman.member import Member


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
            base_url (str, optional): The base url of the API. Defaults to "https://api.fabman.io/v1".
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

    def create_member(self, **kwargs):
        raise NotImplementedError("create_member not implemented yet")

    def get_members(self, **kwargs):
        raise NotImplementedError("get_members not implemented yet")

    def get_member(self, member_id: int, **kwargs):
        """Retrieves a member from the API give their id
        calls "GET /members/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersId

        Args:
            member_id (int): ID of the member to be called
        """
        uri = f"/members/{member_id}"
        
        response = self.__requester.request(
            "GET", uri, _kwargs=combine_kwargs(**kwargs)
        )

        return Member(self.__requester, response.json())

    def get_user(self, **kwargs):
        raise NotImplementedError("get_user not implemented yet")
