"""Tests for the Payment class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests
import requests_mock

from fabman import Fabman
from fabman.payment import Payment
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestPayment(unittest.TestCase):
    """
    Test cases for the Payment class. Note that the developers of this library
    are cheap and have not validated against real data. Sample data is taken from
    the Fabman API POST command model.
    """

    def setUp(self) -> None:
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_payment_by_id"]}, m)

            self.payment: Payment = self.fabman.get_payment(1)

    def test_instance(self, m):
        """Tests to make sure the constructor worked as expected"""
        self.assertIsInstance(self.payment, Payment)

    def test_str(self, m):
        string = str(self.payment)
        self.assertTrue(string == "Payment #1: Test Payment")

    def test_delete(self, m):
        register_uris({"payment": ["delete"]}, m)

        resp = self.payment.delete()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 204)

    def test_request_payment(self, m):
        register_uris({"payment": ["request_payment"]}, m)

        resp = self.payment.request_payment()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 201)

    def test_update(self, m):
        """Checks to ensure lockVersion is added and used"""
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/payments/1",
            text=validate_update,
            status_code=200,
        )

        self.payment.update(notes="Updated Notes")
        self.assertTrue(m.called)
