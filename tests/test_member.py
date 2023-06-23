"""Tests for the Member class."""
# pylint: disable=missing-function-docstring, missing-class-docstring, invalid-name, unused-argument

import unittest
import warnings
import requests_mock

from fabman import Fabman
from fabman.exceptions import ResourceDoesNotExist
from fabman.member import Member

from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestMembers(unittest.TestCase):

    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_member_by_id"]}, m)

            self.member: Member = self.fabman.get_member(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)

    def test_get_balance_items(self, m):
        register_uris({"member": ["get_balance_items"]}, m)

        balance_items = self.member.get_balance_items()

        self.assertIsInstance(balance_items, dict)

    def test_get_get_changes(self, m):
        register_uris({"member": ["get_changes"]}, m)

        changes = self.member.get_changes()
        print(type(changes))
        self.assertIsInstance(changes, list)

    def test_get_credits(self, m):
        register_uris({"member": ["get_credits"]}, m)

        _credits = self.member.get_credits()
        self.assertIsInstance(_credits, list)

    def test_get_credit_by_credit_id(self, m):
        register_uris({"member": ["get_credit_by_id"]}, m)

        credit = self.member.get_credit_by_id(1)
        self.assertIsInstance(credit, dict)

    # note there are no credits on my test account, so this is unverifiable
    def test_get_credit_uses_by_id(self, m):
        register_uris({"member": ["get_credit_uses_by_id"]}, m)

        credit = self.member.get_credit_uses_by_id(1)
        self.assertIsInstance(credit, list)

    def test_get_device(self, m):
        register_uris({"member": ["get_device"]}, m)

        device = self.member.get_device()
        self.assertIsInstance(device, dict)
        self.assertEqual(device['name'], "Apple iPhone")

    def test_get_device_changes(self, m):
        register_uris({"member": ["get_device_changes"]}, m)
        changes = self.member.get_device_changes()

        self.assertIsInstance(changes, list)
        self.assertEqual(len(changes), 2)

    def test_get_device_changes_by_id(self, m):
        register_uris({"member": ["get_device_change_by_id"]}, m)

        change = self.member.get_device_change(1)

        self.assertIsInstance(change, dict)

    def test_get_invitation(self, m):
        register_uris({"member": ["get_invitation"]}, m)

        invitation = self.member.get_invitation()
        self.assertIsInstance(invitation, dict)

    def test_get_key_empty(self, m):
        register_uris({"member": ["get_key_empty"]}, m)
        with warnings.catch_warnings(record=True):
            key = self.member.get_key()  # pylint: disable=unused-variable
            self.assertRaises(
                UserWarning,
                msg=(
                    "204 No Content returned. This likely means there is no information"
                    "at the resource."
                )
            )

    def test_get_key(self, m):
        register_uris({"member": ["get_key_data"]}, m)
        key = self.member.get_key()

        self.assertIsInstance(key, dict)

    def test_get_packages(self, m):
        register_uris({"member": ["get_packages"]}, m)
        key = self.member.get_packages()

        self.assertIsInstance(key, list)

    def test_get_package_by_id(self, m):
        register_uris({"member": ["get_package_by_id"]}, m)
        key = self.member.get_package(1)

        self.assertIsInstance(key, dict)

    def test_get_package_by_id_doesnt_hold(self, m):
        register_uris({"member": ["get_package_by_id_doesnt_hold"]}, m)

        self.assertRaises(
            ResourceDoesNotExist,
            self.member.get_package,
            2
        )

    def test_get_payment_account(self, m):
        register_uris({"member": ["get_payment_account"]}, m)

        payment_acct = self.member.get_payment_account()

        self.assertIsInstance(payment_acct, list)

    def test_get_payment_methods_exists(self, m):
        register_uris({"member": ["get_payment_method_exists"]}, m)

        payment_method = self.member.get_payment_method()
        self.assertIsInstance(payment_method, dict)

    def test_get_payment_method_doesnt_exist(self, m):
        register_uris({"member": ["get_payment_method_doesnt_exist"]}, m)
        with warnings.catch_warnings(record=True):  # pylint: disable=unused-variable
            self.assertRaises(
                UserWarning,
                msg=(
                    "204 No Content returned. This likely means there is no information"
                    "at the resource."
                )
            )

    def test_get_payment_method_mandate_preview(self, m):
        register_uris({"member": ["get_payment_method_mandate_preview"]}, m)

        mandate_preview = self.member.get_payment_method_mandate_preview()
        self.assertIsInstance(mandate_preview, dict)

    def test_get_privileges(self, m):
        register_uris({"member": ["get_privileges"]}, m)

        priv = self.member.get_privileges()
        self.assertIsInstance(priv, dict)
        self.assertEqual(priv['privileges'], "admin")

    def test_get_trained_resources(self, m):
        register_uris({"member": ["get_trained_resources"]}, m)

        train_res = self.member.get_trained_resources()
        self.assertIsInstance(train_res, list)

    def test_get_trainings(self, m):
        register_uris({"member": ["get_trainings"]}, m)

        trainings = self.member.get_trainings()
        self.assertIsInstance(trainings, list)

    def test_get_training_by_id(self, m):
        register_uris({"member": ["get_training_by_id"]}, m)

        training = self.member.get_training(1)
        self.assertIsInstance(training, dict)
