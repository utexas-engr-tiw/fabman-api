"""Tests for the Charge class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests
import requests_mock

from fabman import Fabman
from fabman.charge import Charge
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestMembers(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_charge_by_id"]}, m)

            self.charge: Charge = self.fabman.get_charge(1)

    def test_instance(self, m):
        self.assertIsInstance(self.charge, Charge)

    def test_str(self, m):
        string = str(self.charge)
        self.assertTrue(string == "Charge #1: 12.34 Test Charge")

    def test_delete(self, m):
        register_uris({"charge": ["delete"]}, m)

        resp = self.charge.delete()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 204)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/charges/1",
            text=validate_update,
            status_code=200,
        )

        self.charge.update(description="New Description")
        self.assertTrue(m.called)
