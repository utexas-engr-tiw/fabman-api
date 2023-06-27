"""Tests for the Webhook Class"""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.webhook import Webhook
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestWebhook(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_webhook_by_id"]}, m)

            self.webhook: Webhook = self.fabman.get_webhook(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)
