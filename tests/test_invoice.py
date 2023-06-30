"""Tests for the Invoice class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.invoice import Invoice, InvoiceDetails
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_invoice_by_id"]}, m)

            self.invoice: Invoice = self.fabman.get_invoice(1)

    def test_instance(self, m):
        self.assertIsInstance(self.invoice, Invoice)

    def test_str(self, m):
        string = str(self.invoice)

        self.assertTrue(string == "Invoice #1: 12.34 unpaid")

    def test_cancel(self, m):
        m.register_uri(
            "POST",
            f"{settings.BASE_URL_WITH_VERSION}/invoices/1/cancel",
            text=validate_update,
            status_code=200,
        )

        self.invoice.cancel()
        self.assertTrue(m.called)

    def test_details(self, m):
        register_uris({"invoice": ["details"]}, m)

        details = self.invoice.details()
        self.assertTrue(m.called)
        self.assertIsInstance(details, InvoiceDetails)
        self.assertTrue(details.id == 1)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/invoices/1",
            text=validate_update,
            status_code=200,
        )

        self.invoice.update()
        self.assertTrue(m.called)
