"""Tests for the Account class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.account import Account, PaymentInfo
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestAccount(unittest.TestCase):
    def setUp(self) -> None:
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_account_by_id"]}, m)

            self.account: Account = self.fabman.get_account(1)

    def test_instance(self, m):
        self.assertIsInstance(self.account, Account)

    def test_str(self, m):
        string = str(self.account)
        self.assertTrue(string == "Account #1: Tarok Nor")

    def test_get_payment_info(self, m):
        register_uris({"accounts": ["get_payment_info"]}, m)

        info = self.account.get_payment_info()
        self.assertIsInstance(info, PaymentInfo)
        self.assertTrue(info.id == 1)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/accounts/1",
            text=validate_update,
            status_code=200,
        )

        self.account.update(name="New Name")
        self.assertTrue(m.called)
