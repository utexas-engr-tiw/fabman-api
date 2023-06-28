"""Tests for the Invoice class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.invoice import Invoice
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_invoice_by_id"]}, m)

            self.invoice: Invoice = self.fabman.get_invoice(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)