"""Tests for the ApiKey class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests
import requests_mock

from fabman import Fabman
from fabman.api_key import ApiKey
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestMembers(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_api_key_by_id"]}, m)

            self.api_key: ApiKey = self.fabman.get_api_key(1)

    def testInstance(self, m):
        self.assertIsInstance(self.api_key, ApiKey)

    def test_str(self, m):
        string = str(self.api_key)
        self.assertTrue(string == "ApiKey #1: New API Key")

    def test_delete(self, m):
        register_uris({"api_key": ["delete"]}, m)

        resp = self.api_key.delete()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 204)

    def test_get_token(self, m):
        register_uris({"api_key": ["get_token"]}, m)

        tok = self.api_key.get_token()
        self.assertIsInstance(tok, dict)
        self.assertTrue(tok["token"] == "123")

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/api-keys/1",
            text=validate_update,
            status_code=200,
        )

        self.api_key.update(label="New Label")
        self.assertTrue(m.called)
