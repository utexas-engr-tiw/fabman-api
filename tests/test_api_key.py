"""Tests for the ApiKey class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.api_key import ApiKey
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestMembers(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_api_key_by_id"]}, m)

            self.api_key: ApiKey = self.fabman.get_api_key(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)
