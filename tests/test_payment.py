"""Tests for the Payment class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.payment import Payment
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestPayment(unittest.TestCase):
    def setUp(self) -> None:
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_payment_by_id"]}, m)

            self.payment: Payment = self.fabman.get_payment(1)

    def test_sanity(self):
        self.assertEqual(1, 1)
