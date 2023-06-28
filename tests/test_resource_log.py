"""Tests for the ResourceLog class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests
import requests_mock

from fabman import Fabman
from fabman.resource_log import ResourceLog
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestResourceLog(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_resource_log_by_id"]}, m)

            self.resource_log: ResourceLog = self.fabman.get_resource_log(1)

    def test_instance(self, m):
        self.assertIsInstance(self.resource_log, ResourceLog)

    def test_str(self, m):
        string = str(self.resource_log)
        self.assertEqual(string, "ResourceLog #1, Resource #1 - reboot")

    def test_delete(self, m):
        register_uris({"resource_log": ["delete"]}, m)

        resp = self.resource_log.delete()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 204)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/resource-logs/1",
            text=validate_update,
            status_code=200,
        )

        self.resource_log.update(type="reboot")
        self.assertTrue(m.called)
