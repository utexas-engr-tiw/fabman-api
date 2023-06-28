"""Tests for the Package class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests
import requests_mock

from fabman import Fabman
from fabman.package import Package, PackageCredit, PackagePermission
from fabman.paginated_list import PaginatedList
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestPackage(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_package_by_id"]}, m)

            self.package: Package = self.fabman.get_package(1)

    def test_instance(self, m):
        self.assertIsInstance(self.package, Package)

    def test_str(self, m):
        string = str(self.package)

        self.assertTrue(string == "Package #1: Test Package")

    def test_delete(self, m):
        register_uris({"package": ["delete"]}, m)

        resp = self.package.delete()
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 204)

    def test_get_credit(self, m):
        register_uris({"package": ["get_credit"]}, m)

        credit = self.package.get_credit(1)

        self.assertIsInstance(credit, PackageCredit)
        self.assertTrue(hasattr(credit, "id"))
        self.assertTrue(credit.id == 1)

    def test_get_credits(self, m):
        register_uris({"package": ["get_credits"]}, m)

        credits = self.package.get_credits()
        self.assertIsInstance(credits, PaginatedList)
        self.assertIsInstance(credits[0], PackageCredit)
        self.assertTrue(hasattr(credits[0], "id"))
        self.assertTrue(credits[0].id == 1)

    def test_get_permission(self, m):
        register_uris({"package": ["get_permission"]}, m)

        permission = self.package.get_permission(1)
        self.assertIsInstance(permission, PackagePermission)
        self.assertTrue(hasattr(permission, "id"))
        self.assertTrue(permission.id == 1)

    def test_get_permissions(self, m):
        register_uris({"package": ["get_permissions"]}, m)

        permissions = self.package.get_permissions()
        self.assertIsInstance(permissions, PaginatedList)
        self.assertIsInstance(permissions[0], PackagePermission)
        self.assertTrue(hasattr(permissions[0], "id"))
        self.assertTrue(permissions[0].id == 1)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/packages/1",
            text=validate_update,
            status_code=200,
        )

        self.package.update(name="Test Package")
        self.assertTrue(m.called)


@requests_mock.Mocker()
class TestMemberCredit(unittest.TestCase):
    def setUp(self) -> None:
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {"fabman": ["get_package_by_id"], "package": ["get_credit"]}, m
            )

            self.package = self.fabman.get_package(1)
            self.credit = self.package.get_credit(1)

    def test_instance(self, m):
        self.assertIsInstance(self.credit, PackageCredit)

    def test_str(self, m):
        string = str(self.credit)
        self.assertTrue(string == "PackageCredit #1, Package #1: booking")

    def test_delete(self, m):
        register_uris({"package": ["delete_credit"]}, m)

        resp = self.credit.delete()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 204)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/packages/1/credits/1",
            text=validate_update,
            status_code=200,
        )

        self.credit.update(scope="spoofing")
        self.assertTrue(m.called)


@requests_mock.Mocker()
class TestPackagePermission(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {"fabman": ["get_package_by_id"], "package": ["get_permission"]}, m
            )

            self.package = self.fabman.get_package(1)
            self.permission = self.package.get_permission(1)

    def test_instance(self, m):
        self.assertIsInstance(self.permission, PackagePermission)

    def test_str(self, m):
        string = str(self.permission)
        self.assertTrue(string == "PackagePermission #1, Package #1: everything")

    def test_delete(self, m):
        register_uris({"package": ["delete_permission"]}, m)

        resp = self.permission.delete()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 204)
