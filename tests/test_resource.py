"""Tests for the Resources class."""
# pylint: disable=missing-function-docstring, missing-class-docstring, invalid-name, unused-argument

import unittest

import requests
import requests_mock

from fabman import Fabman
from fabman.resource import Resource, ResourceBridge
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestResource(unittest.TestCase):
    """Test Cases for the Resource class."""

    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_resource_by_id"]}, m)

            self.resource: Resource = self.fabman.get_resource(1)

    def test_instance(self, m):
        self.assertIsInstance(self.resource, Resource)

    def test_str(self, m):
        string = str(self.resource)
        self.assertTrue(string == "Resource #1: USS Defiant")

    def test_delete(self, m):
        register_uris({"resource": ["delete"]}, m)

        resp = self.resource.delete()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 204)

    def test_delete_bridge(self, m):
        register_uris({"resource": ["delete_bridge"]}, m)

        resp = self.resource.delete_bridge()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 204)

    def test_get_bridge(self, m):
        register_uris({"resource": ["get_bridge"]}, m)
        bridge = self.resource.get_bridge()

        self.assertIsInstance(bridge, ResourceBridge)
        self.assertTrue(hasattr(bridge, "serialNumber"))

    def test_get_bridge_api_key(self, m):
        register_uris({"resource": ["get_bridge_api_key"]}, m)
        api_key = self.resource.get_bridge_api_key()

        self.assertIsInstance(api_key, dict)


@requests_mock.Mocker()
class TestResourceBridge(unittest.TestCase):
    """Tests the ResourceBridge class"""

    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {"fabman": ["get_resource_by_id"], "resource": ["get_bridge"]}, m
            )

            self.resource = self.fabman.get_resource(1)
            self.bridge = self.resource.get_bridge()

    def test_instance(self, m):
        self.assertIsInstance(self.bridge, ResourceBridge)

    def test_str(self, m):
        string = str(self.bridge)
        self.assertTrue(string == "Resource #1: abcdef123456")

    def test_update(self, m):
        """This update does not require a lockVersion for whatever reason"""

        register_uris({"resource": ["update_bridge"]}, m)

        self.bridge.update()
        self.assertTrue(m.called)
