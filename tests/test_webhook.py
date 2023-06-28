"""Tests for the Webhook Class"""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests
import requests_mock

from fabman import Fabman
from fabman.webhook import Webhook
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestWebhook(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_webhook_by_id"]}, m)

            self.webhook: Webhook = self.fabman.get_webhook(1)

    def test_instance(self, m):
        self.assertIsInstance(self.webhook, Webhook)

    def test_str(self, m):
        string = str(self.webhook)
        self.assertTrue(string == "Webhook #1: Garak's Test Webhook")

    def test_delete(self, m):
        register_uris({"webhook": ["delete"]}, m)

        response = self.webhook.delete()
        self.assertTrue(m.called)
        self.assertIsInstance(response, requests.Response)
        self.assertTrue(response.status_code == 204)

    def test_get_events(self, m):
        register_uris({"webhook": ["get_events"]}, m)

        resp = self.webhook.get_events()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 200)

    def test_send_test_event(self, m):
        register_uris({"webhook": ["send_test_event"]}, m)

        resp = self.webhook.send_test_event()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 201)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/webhooks/1",
            text=validate_update,
            status_code=200,
        )

        self.webhook.update(label="New Label")
        self.assertTrue(m.called)
