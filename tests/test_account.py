"""Tests for the Account class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.account import Account
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestAccount(unittest.TestCase):
    def setUp(self) -> None:
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_account_by_id"]}, m)

            self.account: Account = self.fabman.get_account(1)

    def test_sanity(self, m) -> None:
        self.assertEqual(1, 1)
