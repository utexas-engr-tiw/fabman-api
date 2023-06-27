"""Tests for the Package class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.package import Package
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestPackage(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_package_by_id"]}, m)

            self.package: Package = self.fabman.get_package(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)
