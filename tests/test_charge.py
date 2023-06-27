"""Tests for the Charge class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.charge import Charge
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestMembers(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_charge_by_id"]}, m)

            self.charge: Charge = self.fabman.get_charge(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)
