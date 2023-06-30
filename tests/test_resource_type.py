"""Test for the ResourceType class"""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests
import requests_mock

from fabman import Fabman
from fabman.resource_type import ResourceType
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestResourceType(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_resource_types"]}, m)

            self.resource_type: ResourceType = self.fabman.get_resource_types()[0]

    def test_instance(self, m):
        self.assertIsInstance(self.resource_type, ResourceType)

    def test_str(self, m):
        string = str(self.resource_type)
        self.assertTrue(string == "ResourceType #1: Starship")

    def test_delete(self, m):
        register_uris({"resource_type": ["delete"]}, m)

        resp = self.resource_type.delete()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 204)

    def test_update(self, m):
        register_uris({"resource_type": ["update"]}, m)

        self.resource_type.update(name="Victory Class Starship")
        self.assertTrue(m.called)
        self.assertTrue(self.resource_type.name == "Victory Class Starship")
