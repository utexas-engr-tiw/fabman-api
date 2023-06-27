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

            self.paginated_list: PaginatedList = self.fabman.get_members()

    def test_sanity(self, m):
        self.assertEqual(1, 1)
