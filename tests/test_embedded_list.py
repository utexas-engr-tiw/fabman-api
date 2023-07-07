"""Tests for the EmbeddedList class"""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman.embedded_list import EmbeddedList
from fabman.member import Member
from fabman.paginated_list import PaginatedList
from fabman.requester import Requester
from tests import settings


@requests_mock.Mocker()
class TestEmbeddedList(unittest.TestCase):
    def setUp(self):
        members = [
            {"id": 1, "firstName": "Julian", "lastName": "Bashear"},
            {"id": 2, "firstName": "Kira", "lastName": "Nerys"},
            {"id": 3, "firstName": "Benjamin", "lastName": "Sisko"},
            {"id": 4, "firstName": "Jadzia", "lastName": "Dax"},
            {"id": 5, "firstName": "Miles", "lastName": "O'Brien"},
            {"id": 6, "firstName": "Odo", "lastName": "Odo"},
            {"id": 7, "firstName": "Quark", "lastName": "Quark"},
            {"id": 8, "firstName": "Worf", "lastName": "Worf"},
            {"id": 9, "firstName": "Jake", "lastName": "Sisko"},
            {"id": 10, "firstName": "Nog", "lastName": "Nog"},
            {"id": 11, "firstName": "Rom", "lastName": "Rom"},
            {"id": 12, "firstName": "Leeta", "lastName": "Leeta"},
            {"id": 13, "firstName": "Elim", "lastName": "Garak"},
            {"id": 14, "firstName": "Martok", "lastName": "Martok"},
            {"id": 15, "firstName": "Kasidy", "lastName": "Yates"},
            {"id": 16, "firstName": "Ezri", "lastName": "Dax"},
            {"id": 17, "firstName": "Weyoun", "lastName": "Weyoun"},
            {"id": 18, "firstName": "Damar", "lastName": "Damar"},
            {"id": 19, "firstName": "Luaran", "lastName": "Luaran"},
        ]

        self._requester = Requester("https://fabman.io/api/v1", settings.API_KEY)
        extra_attribs = {"spaceId": 1, "account": 1}

        self.embedded_list = EmbeddedList(
            Member,
            members,
            self._requester,
            "GET",
            "/members",
            extra_attribs=extra_attribs,
        )

    def test_instance(self, m):
        self.assertIsInstance(self.embedded_list, EmbeddedList)

    def test_repr(self, m):
        self.assertEqual(
            repr(self.embedded_list), "<EmbeddedList of type Member with 19 elements>"
        )

    def test_iteration(self, m):
        for i, element in enumerate(self.embedded_list):
            self.assertIsInstance(element, Member)
            self.assertEqual(element.id, i + 1)

    def test_refresh(self, m):
        members = self.embedded_list.get_live_data()
        self.assertIsInstance(members, PaginatedList)

    def test_refresh_no_method(self, m):
        self.embedded_list._request_method = None
        with self.assertRaises(ValueError):
            self.embedded_list.get_live_data()
        self.embedded_list._request_method = ""
        with self.assertRaises(ValueError):
            self.embedded_list.get_live_data()

    def test_refresh_no_endpoint(self, m):
        self.embedded_list._refresh_endpoint = None
        with self.assertRaises(ValueError):
            self.embedded_list.get_live_data()
        self.embedded_list._refresh_endpoint = ""
        with self.assertRaises(ValueError):
            self.embedded_list.get_live_data()
