"""Tests for the PaginatedList class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.paginated_list import PaginatedList
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestPaginatedList(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_members"]}, m)

            self.paginated_list: PaginatedList = self.fabman.get_members(limit=1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)

    def test_repr(self, m):
        self.assertEqual("<PaginatedList of type Member>", repr(self.paginated_list))

    def test_format_link(self, m):
        headers = {
            "link": '<https://fabman.io/api/v1/members?limit=1&offset=1>; rel="next", <https://fabman.io/api/v1/members?limit=1&offset=2>; rel="last"'
        }
        link = self.paginated_list._PaginatedList__format_link(headers)
        self.assertEqual(link, "/members?limit=1&offset=1")
