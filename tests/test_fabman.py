"""Tests for the fabman module."""
# pylint: disable=missing-function-docstring, missing-class-docstring, invalid-name, unused-argument
import unittest
import warnings

import requests_mock

from fabman import Fabman
from fabman.member import Member
from fabman.resources import Resource
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestFabman(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

    # Test initializing the Fabman instance
    def test_init_no_api_key(self, m):
        with self.assertRaises(
            ValueError,
            msg="No access token provided"
        ):
            Fabman(None)

    def test_init_empty_api_key(self, m):
        with self.assertRaises(
            ValueError,
            msg="No access token provided"
        ):
            Fabman("")

    def test_init_warnings_for_http(self, m):
        with warnings.catch_warnings(record=True):
            Fabman(settings.API_KEY, settings.BASE_URL_AS_HTTP)
            self.assertRaises(
                UserWarning,
                msg=(
                    "Please use HTTPS when possible. Fabman API may not respond as intended and"
                    "user data will not be secure",
                )
            )

    def test_init_warnings_for_bad_url(self, m):
        with warnings.catch_warnings(record=True):
            Fabman(settings.API_KEY, settings.BASE_URL_AS_INVALID)
            self.assertRaises(
                UserWarning,
                msg=(
                    "An invalid `bad_url` provided. Will likely not work as intended."
                )
            )

    def test_get_member(self, m):
        register_uris({"fabman": ["get_member_by_id"]}, m)

        member = self.fabman.get_member(1)
        self.assertIsInstance(member, Member)
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "firstName"))

    def test_get_member_with_embed_str(self, m):
        """
        Tests the ability to embed a single resource as a string. Primarily tests 
        the functionality of the Requester child object. Embedding does not need 
        to be checked for other resources, as they all use the same Requester.
        """
        register_uris({"fabman": ["get_member_by_id_with_embed_str"]}, m)

        member = self.fabman.get_member(1, embed="memberPackages")
        self.assertIsInstance(member, Member)
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "_embedded"))

    def test_get_member_with_embed_single_list(self, m):
        """
        Tests the ability to embed a single resource in a list. Primarily tests 
        the functionality of the Requester child object. Embedding does not need 
        to be checked for other resources, as they all use the same Requester.
        """
        register_uris({"fabman": ["get_member_by_id_with_embed_str"]}, m)

        member = self.fabman.get_member(1, embed=["memberPackages"])
        self.assertIsInstance(member, Member)
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "_embedded"))

        self.assertTrue(
            "memberPackages" in member._embedded)  # pylint: disable=protected-access

    def test_get_member_with_embed_multi_list(self, m):
        """
        Tests the ability to embed multiple resource in a list. Primarily tests 
        the functionality of the Requester child object. Embedding does not need 
        to be checked for other resources, as they all use the same Requester.
        """
        register_uris({"fabman": ["get_member_by_id_with_embed_list_multi"]}, m)

        member = self.fabman.get_member(
            1, embed=["memberPackages", "trainings"])
        self.assertIsInstance(member, Member)
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "_embedded"))

        embeds = member._embedded  # pylint: disable=protected-access
        self.assertTrue("memberPackages" in embeds)
        self.assertTrue("trainings" in embeds)

    def test_get_user_me(self, m):
        register_uris({"fabman": ["get_user_me"]}, m)

        member = self.fabman.get_user()
        self.assertIsInstance(member, Member)
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "firstName"))
        self.assertTrue(hasattr(member, "account"))

    def test_get_resource(self, m):
        register_uris({"fabman": ["get_resource_by_id"]}, m)

        resource = self.fabman.get_resource(1)
        self.assertIsInstance(resource, Resource)
        self.assertTrue(hasattr(resource, "id"))
        self.assertTrue(hasattr(resource, "name"))


if __name__ == "__main__":
    unittest.main()
