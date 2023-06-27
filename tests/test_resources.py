"""Tests for the Resources class."""
# pylint: disable=missing-function-docstring, missing-class-docstring, invalid-name, unused-argument

import unittest
import requests_mock

from fabman import Fabman
from fabman.resource import Resource
from fabman.resource import ResourceBridge

from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestResources(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_resource_by_id"]}, m)

            self.resource: Resource = self.fabman.get_resource(1)

    def test_get_bridge(self, m):
        register_uris({"resources": ["get_bridge"]}, m)
        bridge = self.resource.get_bridge()

        self.assertIsInstance(bridge, ResourceBridge)
        self.assertTrue(hasattr(bridge, 'serialNumber'))

    def test_get_bridge_api_key(self, m):
        register_uris({"resources": ["get_bridge_api_key"]}, m)
        api_key = self.resource.get_bridge_api_key()

        self.assertIsInstance(api_key, dict)
