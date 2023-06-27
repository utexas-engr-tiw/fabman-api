"""Test for the ResourceType class"""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.resource_type import ResourceType
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestResourceType(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_resource_type_by_id"]}, m)

            self.resource_type: ResourceType = self.fabman.get_resource_type(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)
