"""Tests for the PaginatedList class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.member import Member
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

    def test_iteration(self, m):
        register_uris(
            {
                "paginated_list": ["get_members_first", "get_members_second"],
            },
            m,
        )

        members = self.fabman.get_members(limit=5)
        self.assertIsInstance(members, PaginatedList)
        items = [m for m in members]
        self.assertEqual(len(items), 10)
        for i, item in enumerate(items):
            self.assertIsInstance(item, Member)
            self.assertEqual(item.id, i + 1)

    def test_negative_index(self, m):
        register_uris({"paginated_list": ["get_members_first"]}, m)

        members = self.fabman.get_members(limit=5)
        self.assertIsInstance(members, PaginatedList)

        with self.assertRaises(IndexError):
            member = members[-1]

    def test_index(self, m):
        register_uris({"paginated_list": ["get_members_first"]}, m)

        members = self.fabman.get_members(limit=5)
        self.assertIsInstance(members, PaginatedList)
        member = members[2]
        self.assertIsInstance(member, Member)
        self.assertTrue(member.id == 3)

    def test_grow_index(self, m):
        register_uris(
            {"paginated_list": ["get_members_first", "get_members_second"]}, m
        )

        members = self.fabman.get_members(limit=5)
        self.assertIsInstance(members, PaginatedList)
        member = members[7]
        self.assertIsInstance(member, Member)
        self.assertTrue(member.id == 8)

    def test_index_out_of_range(self, m):
        register_uris(
            {"paginated_list": ["get_members_first", "get_members_second"]}, m
        )

        members = self.fabman.get_members(limit=5)
        self.assertIsInstance(members, PaginatedList)

        with self.assertRaises(IndexError):
            member = members[11]
