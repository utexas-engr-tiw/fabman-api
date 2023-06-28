"""Tests for the fabman module."""
# pylint: disable=missing-function-docstring, missing-class-docstring, invalid-name, unused-argument
import unittest
import warnings

import requests_mock

from fabman import Fabman
from fabman.account import Account
from fabman.api_key import ApiKey
from fabman.booking import Booking
from fabman.charge import Charge
from fabman.invoice import Invoice
from fabman.job import Job
from fabman.member import Member
from fabman.package import Package
from fabman.paginated_list import PaginatedList
from fabman.payment import Payment
from fabman.resource import Resource
from fabman.resource_log import ResourceLog
from fabman.resource_type import ResourceType
from fabman.space import Space
from fabman.training_course import TrainingCourse
from fabman.webhook import Webhook
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestFabman(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

    # Test initializing the Fabman instance
    def test_init_no_api_key(self, m):
        with self.assertRaises(ValueError, msg="No access token provided"):
            Fabman("")

    def test_init_empty_api_key(self, m):
        with self.assertRaises(ValueError, msg="No access token provided"):
            Fabman("")

    def test_init_warnings_for_http(self, m):
        with warnings.catch_warnings(record=True):
            Fabman(settings.API_KEY, settings.BASE_URL_AS_HTTP)
            self.assertRaises(
                UserWarning,
                msg=(
                    "Please use HTTPS when possible. Fabman API may not respond as intended and"
                    "user data will not be secure",
                ),
            )

    def test_init_warnings_for_bad_url(self, m):
        with warnings.catch_warnings(record=True):
            Fabman(settings.API_KEY, settings.BASE_URL_AS_INVALID)
            self.assertRaises(
                UserWarning,
                msg=(
                    "An invalid `bad_url` provided. Will likely not work as intended."
                ),
            )

    def test_init_trailing_slash(self, m):
        register_uris({"fabman": ["get_member_by_id"]}, m)
        fabman = Fabman(settings.API_KEY, settings.BASE_URL_WITH_TRAILING_SLASH)
        member = fabman.get_member(1)
        self.assertTrue(m.called)
        self.assertIsInstance(member, Member)

    def test_get_account(self, m):
        register_uris({"fabman": ["get_account_by_id"]}, m)

        account = self.fabman.get_account(1)
        self.assertIsInstance(account, Account)
        self.assertTrue(hasattr(account, "id"))
        self.assertTrue(account.id == 1)

    def test_get_accounts(self, m):
        register_uris({"fabman": ["get_accounts"]}, m)

        accounts = self.fabman.get_accounts()
        self.assertIsInstance(accounts, PaginatedList)
        self.assertIsInstance(accounts[0], Account)
        self.assertTrue(hasattr(accounts[0], "id"))
        self.assertTrue(accounts[0].id == 1)

    def test_get_api_key(self, m):
        register_uris({"fabman": ["get_api_key_by_id"]}, m)

        api_key = self.fabman.get_api_key(1)
        self.assertIsInstance(api_key, ApiKey)
        self.assertTrue(hasattr(api_key, "id"))
        self.assertTrue(api_key.id == 1)

    def test_get_api_keys(self, m):
        register_uris({"fabman": ["get_api_keys"]}, m)

        api_keys = self.fabman.get_api_keys()
        self.assertIsInstance(api_keys, PaginatedList)
        self.assertIsInstance(api_keys[0], ApiKey)
        self.assertTrue(hasattr(api_keys[0], "id"))
        self.assertTrue(api_keys[0].id == 1)

    def test_get_booking(self, m):
        register_uris({"fabman": ["get_booking_by_id"]}, m)

        bookings = self.fabman.get_booking(1)
        self.assertIsInstance(bookings, Booking)
        self.assertTrue(hasattr(bookings, "id"))
        self.assertTrue(bookings.id == 1)

    def test_get_bookings(self, m):
        register_uris({"fabman": ["get_bookings"]}, m)

        bookings = self.fabman.get_bookings()
        self.assertIsInstance(bookings, PaginatedList)
        self.assertIsInstance(bookings[0], Booking)
        self.assertTrue(hasattr(bookings[0], "id"))
        self.assertTrue(bookings[0].id == 1)

    def test_get_charge(self, m):
        register_uris({"fabman": ["get_charge_by_id"]}, m)

        charge = self.fabman.get_charge(1)
        self.assertIsInstance(charge, Charge)
        self.assertTrue(hasattr(charge, "id"))
        self.assertTrue(charge.id == 1)

    def test_get_charges(self, m):
        register_uris({"fabman": ["get_charges"]}, m)

        charges = self.fabman.get_charges()
        self.assertIsInstance(charges, PaginatedList)
        self.assertIsInstance(charges[0], Charge)
        self.assertTrue(hasattr(charges[0], "id"))
        self.assertTrue(charges[0].id == 1)

    def test_get_invoice(self, m):
        register_uris({"fabman": ["get_invoice_by_id"]}, m)

        invoice = self.fabman.get_invoice(1)
        self.assertIsInstance(invoice, Invoice)
        self.assertTrue(hasattr(invoice, "id"))
        self.assertTrue(invoice.id == 1)

    def test_invoices(self, m):
        register_uris({"fabman": ["get_invoices"]}, m)

        invoices = self.fabman.get_invoices()
        self.assertIsInstance(invoices, PaginatedList)
        self.assertIsInstance(invoices[0], Invoice)
        self.assertTrue(hasattr(invoices[0], "id"))
        self.assertTrue(invoices[0].id == 1)

    def test_get_job(self, m):
        register_uris({"fabman": ["get_job_by_id"]}, m)

        job = self.fabman.get_job(1)
        self.assertIsInstance(job, Job)
        self.assertTrue(hasattr(job, "id"))
        self.assertTrue(job.id == 1)
        self.assertTrue(str(job) == "Job #1")

    def test_get_jobs(self, m):
        register_uris({"fabman": ["get_jobs"]}, m)

        jobs = self.fabman.get_jobs()
        self.assertIsInstance(jobs, PaginatedList)
        self.assertIsInstance(jobs[0], Job)
        self.assertTrue(hasattr(jobs[0], "id"))
        self.assertTrue(jobs[0].id == 1)

    def test_get_member(self, m):
        register_uris({"fabman": ["get_member_by_id"]}, m)

        member = self.fabman.get_member(1)
        self.assertIsInstance(member, Member)
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "firstName"))
        self.assertTrue(member.id == 1)

    def test_get_members(self, m):
        register_uris({"fabman": ["get_members"]}, m)

        members = self.fabman.get_members()
        self.assertIsInstance(members, PaginatedList)
        self.assertIsInstance(members[0], Member)
        self.assertTrue(hasattr(members[0], "id"))
        self.assertTrue(members[0].id == 1)

    def test_get_member_with_embed_str(self, m):
        """
        Tests the ability to embed a single resource as a string. Primarily tests
        the functionality of the Requester child object. Embedding does not need
        to be checked for other resources, as they all use the same Requester.
        """
        register_uris({"fabman": ["get_member_by_id_with_embed_str"]}, m)

        member = self.fabman.get_member(1, embed="memberPackages")
        self.assertIsInstance(member, Member)
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "_embedded"))

    def test_get_member_with_embed_single_list(self, m):
        """
        Tests the ability to embed a single resource in a list. Primarily tests
        the functionality of the Requester child object. Embedding does not need
        to be checked for other resources, as they all use the same Requester.
        """
        register_uris({"fabman": ["get_member_by_id_with_embed_str"]}, m)

        member = self.fabman.get_member(1, embed=["memberPackages"])
        self.assertIsInstance(member, Member)
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "_embedded"))

        self.assertTrue(
            "memberPackages" in member._embedded
        )  # pylint: disable=protected-access

    def test_get_member_with_embed_multi_list(self, m):
        """
        Tests the ability to embed multiple resource in a list. Primarily tests
        the functionality of the Requester child object. Embedding does not need
        to be checked for other resources, as they all use the same Requester.
        """
        register_uris({"fabman": ["get_member_by_id_with_embed_list_multi"]}, m)

        member = self.fabman.get_member(1, embed=["memberPackages", "trainings"])
        self.assertIsInstance(member, Member)
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "_embedded"))

        embeds = member._embedded  # pylint: disable=protected-access
        self.assertTrue("memberPackages" in embeds)
        self.assertTrue("trainings" in embeds)

    def test_get_package(self, m):
        register_uris({"fabman": ["get_package_by_id"]}, m)

        package = self.fabman.get_package(1)
        self.assertIsInstance(package, Package)
        self.assertTrue(hasattr(package, "id"))
        self.assertTrue(package.id == 1)

    def test_get_packages(self, m):
        register_uris({"fabman": ["get_packages"]}, m)

        packages = self.fabman.get_packages()
        self.assertIsInstance(packages, PaginatedList)
        self.assertIsInstance(packages[0], Package)
        self.assertTrue(hasattr(packages[0], "id"))
        self.assertTrue(packages[0].id == 1)

    def test_get_payment(self, m):
        register_uris({"fabman": ["get_payment_by_id"]}, m)

        payment = self.fabman.get_payment(1)
        self.assertIsInstance(payment, Payment)
        self.assertTrue(hasattr(payment, "id"))
        self.assertTrue(payment.id == 1)

    def test_get_payments(self, m):
        register_uris({"fabman": ["get_payments"]}, m)

        payments = self.fabman.get_payments()
        self.assertIsInstance(payments, PaginatedList)
        self.assertIsInstance(payments[0], Payment)
        self.assertTrue(hasattr(payments[0], "id"))
        self.assertTrue(payments[0].id == 1)

    def test_get_resource(self, m):
        register_uris({"fabman": ["get_resource_by_id"]}, m)

        resource = self.fabman.get_resource(1)
        self.assertIsInstance(resource, Resource)
        self.assertTrue(hasattr(resource, "id"))
        self.assertTrue(hasattr(resource, "name"))

    def test_get_resources(self, m):
        register_uris({"fabman": ["get_resources"]}, m)

        resources = self.fabman.get_resources()
        self.assertIsInstance(resources, PaginatedList)
        self.assertIsInstance(resources[0], Resource)
        self.assertTrue(hasattr(resources[0], "id"))
        self.assertTrue(resources[0].id == 1)

    def test_get_resource_log(self, m):
        register_uris({"fabman": ["get_resource_log_by_id"]}, m)

        resources = self.fabman.get_resource_log(1)
        self.assertIsInstance(resources, ResourceLog)
        self.assertTrue(hasattr(resources, "id"))
        self.assertTrue(resources.id == 1)

    def test_get_resource_logs(self, m):
        register_uris({"fabman": ["get_resource_logs"]}, m)

        resources = self.fabman.get_resource_logs()
        self.assertIsInstance(resources, PaginatedList)
        self.assertIsInstance(resources[0], ResourceLog)
        self.assertTrue(hasattr(resources[0], "id"))
        self.assertTrue(resources[0].id == 1)

    def test_get_resource_type(self, m):
        register_uris({"fabman": ["get_resource_type_by_id"]}, m)

        resource_type = self.fabman.get_resource_type(1)
        self.assertIsInstance(resource_type, ResourceType)
        self.assertTrue(hasattr(resource_type, "id"))
        self.assertTrue(resource_type.id == 1)

    def test_get_resource_types(self, m):
        register_uris({"fabman": ["get_resource_types"]}, m)

        resource_types = self.fabman.get_resource_types()
        self.assertIsInstance(resource_types, PaginatedList)
        self.assertTrue(hasattr(resource_types[0], "id"))
        self.assertTrue(resource_types[0].id == 1)

    def test_get_space(self, m):
        register_uris({"fabman": ["get_space_by_id"]}, m)

        space = self.fabman.get_space(1)
        self.assertIsInstance(space, Space)
        self.assertTrue(hasattr(space, "id"))
        self.assertTrue(space.id == 1)

    def test_get_spaces(self, m):
        register_uris({"fabman": ["get_spaces"]}, m)

        spaces = self.fabman.get_spaces()
        self.assertIsInstance(spaces, PaginatedList)
        self.assertIsInstance(spaces[0], Space)
        self.assertTrue(hasattr(spaces[0], "id"))
        self.assertTrue(spaces[0].id == 1)

    def test_get_training_course(self, m):
        register_uris({"fabman": ["get_training_course_by_id"]}, m)

        training_course = self.fabman.get_training_course(1)
        self.assertIsInstance(training_course, TrainingCourse)
        self.assertTrue(hasattr(training_course, "id"))
        self.assertTrue(training_course.id == 1)

    def test_get_training_courses(self, m):
        register_uris({"fabman": ["get_training_courses"]}, m)

        training_courses = self.fabman.get_training_courses()
        self.assertIsInstance(training_courses, PaginatedList)
        self.assertIsInstance(training_courses[0], TrainingCourse)
        self.assertTrue(hasattr(training_courses[0], "id"))
        self.assertTrue(training_courses[0].id == 1)

    def test_get_user_me(self, m):
        register_uris({"fabman": ["get_user_me"]}, m)

        member = self.fabman.get_user()
        self.assertIsInstance(member, Member)
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "firstName"))
        self.assertTrue(hasattr(member, "account"))

    def test_get_webhook(self, m):
        register_uris({"fabman": ["get_webhook_by_id"]}, m)

        webhook = self.fabman.get_webhook(1)
        self.assertIsInstance(webhook, Webhook)
        self.assertTrue(hasattr(webhook, "id"))
        self.assertTrue(webhook.id == 1)

    def test_get_webhooks(self, m):
        register_uris({"fabman": ["get_webhooks"]}, m)

        webhooks = self.fabman.get_webhooks()
        self.assertIsInstance(webhooks, PaginatedList)
        self.assertIsInstance(webhooks[0], Webhook)
        self.assertTrue(hasattr(webhooks[0], "id"))
        self.assertTrue(webhooks[0].id == 1)


if __name__ == "__main__":
    unittest.main()
