"""Tests for the Member class."""
# pylint: disable=missing-function-docstring, missing-class-docstring, invalid-name, unused-argument

import unittest
import warnings

import requests_mock

from fabman import Fabman
from fabman.exceptions import ResourceDoesNotExist
from fabman.member import Member, MemberCredit, MemberKey, MemberPackage
from fabman.paginated_list import PaginatedList
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestMembers(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_member_by_id"]}, m)

            self.member: Member = self.fabman.get_member(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)

    def test_to_str(self, m):
        string = str(self.member)
        self.assertIsInstance(string, str)
        self.assertTrue("1: John Doe" == string)

    def test_create_credit(self, m):
        register_uris({"member": ["create_credit"]}, m)

        credit = self.member.create_credit(amount=12.34)
        self.assertIsInstance(credit, MemberCredit)
        self.assertTrue(hasattr(credit, "amount"))
        self.assertTrue(credit.amount == 12.34)

    def test_create_key(self, m):
        register_uris({"member": ["create_key"]}, m)

        key = self.member.create_key(type="em4102", token="12345678")
        self.assertIsInstance(key, MemberKey)
        self.assertTrue(hasattr(key, "type"))
        self.assertTrue(key.type == "em4102")

    def test_delete(self, m):
        register_uris({"member": ["delete"]}, m)

        self.member.delete()
        self.assertTrue(m.called)

    def test_get_balance_items(self, m):
        register_uris({"member": ["get_balance_items"]}, m)

        balance_items = self.member.get_balance_items()

        self.assertIsInstance(balance_items, dict)

    def test_get_get_changes(self, m):
        register_uris({"member": ["get_changes"]}, m)

        changes = self.member.get_changes()
        self.assertIsInstance(changes, list)

    def test_get_credits(self, m):
        register_uris({"member": ["get_credits"]}, m)

        _credits = self.member.get_credits()
        self.assertIsInstance(_credits, PaginatedList)

    def test_get_credit_by_credit_id(self, m):
        register_uris({"member": ["get_credit_by_id"]}, m)

        credit = self.member.get_credit(1)
        self.assertIsInstance(credit, MemberCredit)

    def test_get_device(self, m):
        register_uris({"member": ["get_device"]}, m)

        device = self.member.get_device()
        self.assertIsInstance(device, dict)
        self.assertEqual(device["name"], "Apple iPhone")

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
                ),
            )

    def test_get_key(self, m):
        register_uris({"member": ["get_key_data"]}, m)
        key = self.member.get_key()

        self.assertIsInstance(key, dict)

    def test_get_packages(self, m):
        register_uris({"member": ["get_packages"]}, m)
        key = self.member.get_packages()

        self.assertIsInstance(key, PaginatedList)

    def test_get_package_by_id(self, m):
        register_uris({"member": ["get_package_by_id"]}, m)
        key = self.member.get_package(1)

        self.assertIsInstance(key, MemberPackage)

    def test_get_package_by_id_doesnt_hold(self, m):
        register_uris({"member": ["get_package_by_id_doesnt_hold"]}, m)

        self.assertRaises(ResourceDoesNotExist, self.member.get_package, 2)

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
                ),
            )

    def test_get_payment_method_mandate_preview(self, m):
        register_uris({"member": ["get_payment_method_mandate_preview"]}, m)

        mandate_preview = self.member.get_payment_method_mandate_preview()
        self.assertIsInstance(mandate_preview, dict)

    def test_get_privileges(self, m):
        register_uris({"member": ["get_privileges"]}, m)

        priv = self.member.get_privileges()
        self.assertIsInstance(priv, dict)
        self.assertEqual(priv["privileges"], "admin")

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

    def test_update(self, m):
        m.register_uri(
            "PUT",
            "https://fabman.io/api/v1/members/1",
            text=validate_update,
            status_code=200,
        )

        self.member.update(firstName="John", lastName="Doe")
        self.assertTrue(m.called)


@requests_mock.Mocker()
class TestMemberCredit(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_member_by_id"]}, m)
            register_uris({"member": ["get_credit_by_id"]}, m)

            self.member: Member = self.fabman.get_member(1)
            self.credit: MemberCredit = self.member.get_credit(1)

    def test_member_id(self, m):
        self.assertTrue(hasattr(self.credit, "member_id"))

    def test_to_str(self, m):
        string = str(self.credit)
        self.assertIsInstance(string, str)
        self.assertTrue("1: global - 12.34" == string)

    def test_delete(self, m):
        register_uris({"member": ["delete_credit"]}, m)

        self.credit.delete()
        self.assertTrue(m.called)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            "https://fabman.io/api/v1/members/1/credits/1",
            text=validate_update,
            status_code=200,
        )

        self.credit.update(amount=12.34)
        self.assertTrue(m.called)
