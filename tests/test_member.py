"""Tests for the Member class."""
# pylint: disable=missing-function-docstring, missing-class-docstring, invalid-name, unused-argument, protected-access

import unittest
import warnings

import requests_mock

from fabman import Fabman
from fabman.embedded_list import EmbeddedList
from fabman.exceptions import ResourceDoesNotExist
from fabman.member import (
    Member,
    MemberBalanceItems,
    MemberChange,
    MemberCredit,
    MemberCreditUse,
    MemberDevice,
    MemberDeviceChange,
    MemberInvitation,
    MemberKey,
    MemberPackage,
    MemberPaymentAccount,
    MemberPaymentMethod,
    MemberPaymentMethodMandatePreview,
    MemberPrivileges,
    MemberTrainedResources,
    MemberTraining,
)
from fabman.package import Package
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
        self.assertTrue("1: Julian Bashear" == string)

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

        resp = self.member.delete()
        self.assertTrue(m.called)
        self.assertTrue(resp.status_code == 204)

    def test_get_balance_items(self, m):
        register_uris({"member": ["get_balance_items"]}, m)

        balance_items = self.member.get_balance_items()

        self.assertIsInstance(balance_items, MemberBalanceItems)

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
        self.assertIsInstance(device, MemberDevice)
        self.assertEqual(device.name, "Starfleet Tricorder")

    def test_get_device_embeded(self, m):
        register_uris({"fabman": ["get_member_by_id_device_embed"]}, m)

        member = self.fabman.get_member(1, embed=["device"])

        self.assertIsInstance(member, Member)
        device = member.get_device()
        self.assertTrue(device.name == "Device 1")

    def test_get_device_changes(self, m):
        register_uris({"member": ["get_device_changes"]}, m)
        changes = self.member.get_device_changes()

        self.assertIsInstance(changes, list)
        self.assertIsInstance(changes[0], MemberDeviceChange)
        self.assertEqual(len(changes), 2)

    def test_get_device_changes_by_id(self, m):
        register_uris({"member": ["get_device_change_by_id"]}, m)

        change = self.member.get_device_change(1)

        self.assertIsInstance(change, MemberDeviceChange)

    def test_get_embeds(self, m):
        register_uris({"member": ["get_embeds"]}, m)

        member = self.fabman.get_member(
            1, embed=["memberPackages", "trainings", "key", "privileges", "device"]
        )
        self.assertIsInstance(member, Member)
        self.assertTrue(hasattr(member, "_embedded"))
        self.assertTrue("memberPackages" in member._embedded)
        self.assertTrue("trainings" in member._embedded)
        self.assertTrue("key" in member._embedded)
        self.assertTrue("privileges" in member._embedded)
        self.assertTrue("device" in member._embedded)

        # memberPackages
        packages = member.get_packages()
        self.assertIsInstance(packages, EmbeddedList)
        self.assertIsInstance(packages[0], MemberPackage)
        self.assertEqual(packages[0].member_id, 1)

        package = member.get_package(1)
        self.assertIsInstance(package, MemberPackage)
        self.assertEqual(package.member_id, 1)

        # trainings
        trainings = member.get_trainings()
        self.assertIsInstance(trainings, EmbeddedList)
        self.assertIsInstance(trainings[0], MemberTraining)
        self.assertTrue(trainings[0].id == 2)
        self.assertTrue(trainings[0].member_id == 1)

        training = member.get_training(2)
        self.assertIsInstance(training, MemberTraining)
        self.assertTrue(training.id == 2)
        self.assertTrue(training.member_id == 1)

        # key
        key = member.get_key()
        self.assertIsInstance(key, MemberKey)
        self.assertTrue(key.lockVersion == 4)
        self.assertTrue(key.member_id == 1)

        # privileges
        privileges = member.get_privileges()
        self.assertIsInstance(privileges, MemberPrivileges)
        self.assertTrue(privileges.privileges == "member")
        self.assertEqual(privileges.member_id, 1)

        # device
        device = member.get_device()
        self.assertIsInstance(device, MemberDevice)
        self.assertTrue(device.name == "Starfleet Tricorder")

    def test_get_invitation(self, m):
        register_uris({"member": ["get_invitation"]}, m)

        invitation = self.member.get_invitation()
        self.assertIsInstance(invitation, MemberInvitation)
        self.assertEqual(invitation.member_id, 1)

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

        self.assertIsInstance(key, MemberKey)
        self.assertTrue(key.type == "em4102")

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

        self.assertIsInstance(payment_acct, MemberPaymentAccount)
        self.assertEqual(payment_acct.member_id, 1)

    def test_get_payment_methods_exists(self, m):
        register_uris({"member": ["get_payment_method_exists"]}, m)

        payment_method = self.member.get_payment_method()
        self.assertIsInstance(payment_method, MemberPaymentMethod)
        self.assertEqual(payment_method.member_id, 1)

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
        self.assertIsInstance(mandate_preview, MemberPaymentMethodMandatePreview)
        self.assertEqual(mandate_preview.member_id, 1)

    def test_get_privileges(self, m):
        register_uris({"member": ["get_privileges"]}, m)

        priv = self.member.get_privileges()
        self.assertIsInstance(priv, MemberPrivileges)
        self.assertEqual(priv.privileges, "admin")
        self.assertEqual(priv.member_id, 1)
        self.assertTrue(str(priv) == "Member #1 is admin")

    def test_get_trained_resources(self, m):
        register_uris({"member": ["get_trained_resources"]}, m)

        train_res = self.member.get_trained_resources()
        self.assertIsInstance(train_res, MemberTrainedResources)
        self.assertEqual(train_res.member_id, 1)
        self.assertTrue(str(train_res) == "Member #1 is trained on 3 resources")
        self.assertListEqual(train_res.resources, [1, 2, 3])

    def test_get_trainings(self, m):
        register_uris({"member": ["get_trainings"]}, m)

        trainings = self.member.get_trainings()
        self.assertIsInstance(trainings, PaginatedList)
        self.assertIsInstance(trainings[0], MemberTraining)

    def test_get_training_by_id(self, m):
        register_uris({"member": ["get_training_by_id"]}, m)

        training = self.member.get_training(1)
        self.assertIsInstance(training, MemberTraining)

    def test_refresh(self, m):
        register_uris({"fabman": ["get_member_by_id"]}, m)

        before = self.member.id
        self.member.refresh()
        self.assertTrue(m.called)
        self.assertTrue(before == self.member.id)

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
class TestMemberChange(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_member_by_id"]}, m)
            register_uris({"member": ["get_changes"]}, m)

            self.member: Member = self.fabman.get_member(1)
            self.changes: list = self.member.get_changes()
            self.change = self.changes[0]

    def test_instance(self, m):
        self.assertIsInstance(self.change, MemberChange)

    def test_string(self, m):
        self.assertEqual(str(self.change), "Change #1 for member #1")

    def test_delete(self, m):
        register_uris({"member": ["delete_change"]}, m)

        resp = self.change.delete()
        self.assertTrue(m.called)
        self.assertTrue(resp.status_code == 204)


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

        resp = self.credit.delete()
        self.assertTrue(m.called)
        self.assertTrue(resp.status_code == 204)

    def test_get_uses(self, m):
        register_uris({"member": ["get_credit_uses"]}, m)

        uses = self.credit.get_uses()
        self.assertIsInstance(uses, list)
        self.assertIsInstance(uses[0], MemberCreditUse)
        self.assertTrue(uses[0].id == 1)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            "https://fabman.io/api/v1/members/1/credits/1",
            text=validate_update,
            status_code=200,
        )

        self.credit.update(amount=12.34)
        self.assertTrue(m.called)


@requests_mock.Mocker()
class TestMemberDeviceChange(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_member_by_id"]}, m)
            register_uris({"member": ["get_device_changes"]}, m)

            self.member: Member = self.fabman.get_member(1)
            self.device_changes: list = self.member.get_device_changes()
            self.device_change = self.device_changes[0]

    def test_instance(self, m):
        self.assertIsInstance(self.device_change, MemberDeviceChange)

    def test_str(self, m):
        self.assertEqual(str(self.device_change), "DeviceChange #1 for member #1")

    def test_delete(self, m):
        register_uris({"member": ["delete_device_change"]}, m)

        resp = self.device_change.delete()
        self.assertTrue(m.called)
        self.assertTrue(resp.status_code == 204)


@requests_mock.Mocker()
class TestMemberPaymentMethod(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_member_by_id"]}, m)
            register_uris({"member": ["get_payment_method_exists"]}, m)

            self.member: Member = self.fabman.get_member(1)
            self.payment_method: MemberPaymentMethod = self.member.get_payment_method()

    def test_instance(self, m):
        self.assertIsInstance(self.payment_method, MemberPaymentMethod)

    def test_str(self, m):
        self.assertEqual(
            str(self.payment_method), "Member #1 has a stripe payment method"
        )

    def test_delete(self, m):
        register_uris({"member": ["delete_payment_method"]}, m)

        resp = self.payment_method.delete()
        self.assertTrue(m.called)
        self.assertTrue(resp.status_code == 204)


@requests_mock.Mocker()
class TestMemberKey(unittest.TestCase):
    def setUp(self):
        self.fabman: Fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {"member": ["get_key_data"], "fabman": ["get_member_by_id"]}, m
            )
            self.key: MemberKey = self.fabman.get_member(1).get_key()

    def test_to_str(self, m):
        string = str(self.key)
        self.assertIsInstance(string, str)
        self.assertTrue("1 - em4102" == string)

    def test_delete(self, m):
        register_uris({"member": ["delete_key"]}, m)

        resp = self.key.delete()
        self.assertTrue(m.called)
        self.assertTrue(resp.status_code == 204)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/members/1/key",
            text=validate_update,
            status_code=200,
        )

        self.key.update(type="blowfish")  # the reallest key
        self.assertTrue(m.called)


@requests_mock.Mocker()
class TestMemberPackage(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {"fabman": ["get_member_by_id"], "member": ["get_package_by_id"]}, m
            )

            self.member = self.fabman.get_member(1)
            self.package = self.member.get_package(1)

    def test_str(self, m):
        string = str(self.package)
        self.assertIsInstance(string, str)
        self.assertTrue("1 - 1" == string)

    def test_delete(self, m):
        register_uris({"member": ["delete_package"]}, m)

        resp = self.package.delete()
        self.assertTrue(m.called)
        self.assertTrue(resp.status_code == 204)

    def test_get_package(self, m):
        register_uris(
            {"member": ["get_package_by_id"], "fabman": ["get_package_by_id"]}, m
        )

        package = self.package.get_package()
        self.assertIsInstance(package, Package)

    def test_get_package_embedded(self, m):
        register_uris({"member": ["get_packages_embedded"]}, m)

        memberPackage = self.member.get_packages(embed=["package"])
        self.assertIsInstance(memberPackage, PaginatedList)
        self.assertIsInstance(memberPackage[0], MemberPackage)

        package = memberPackage[0].get_package()
        self.assertIsInstance(package, Package)
        self.assertTrue(hasattr(package, "name"))
        self.assertTrue(package.name == "Test Package")

    def test_update(self, m):
        m.register_uri(
            "PUT",
            "https://fabman.io/api/v1/members/1/packages/1",
            text=validate_update,
            status_code=200,
        )

        self.package.update()
        self.assertTrue(m.called)


@requests_mock.Mocker()
class TestMemberTraining(unittest.TestCase):
    def setUp(self) -> None:
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {"fabman": ["get_member_by_id"], "member": ["get_training_by_id"]}, m
            )

            self.member = self.fabman.get_member(1)
            self.training = self.member.get_training(1)

    def test_instance(self, m):
        self.assertIsInstance(self.training, MemberTraining)

    def test_str(self, m):
        self.assertTrue(str(self.training) == "MemberTraining #1 for member #1")

    def test_delete(self, m):
        register_uris({"member": ["delete_training"]}, m)

        resp = self.training.delete()
        self.assertTrue(m.called)
        self.assertTrue(resp.status_code == 204)
