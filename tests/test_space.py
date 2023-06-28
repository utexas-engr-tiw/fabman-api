"""Tests for the Space class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests
import requests_mock

from fabman import Fabman
from fabman.paginated_list import PaginatedList
from fabman.space import Space, SpaceBillingSettings, SpaceHoliday
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestSpace(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_space_by_id"]}, m)

            self.space: Space = self.fabman.get_space(1)

    def test_instance(self, m):
        self.assertIsInstance(self.space, Space)

    def test_str(self, m):
        string = str(self.space)
        self.assertTrue(string.startswith("Space #1: Operations Center"))

    def test_create_holiday(self, m):
        register_uris({"space": ["create_holiday"]}, m)

        holiday = self.space.create_holiday(
            title="Test Holiday",
            fromDateTime="2023-06-28T00:00",
            untilDateTime="2023-06-28T23:59",
            affects="all",
        )

        self.assertIsInstance(holiday, SpaceHoliday)
        self.assertTrue(hasattr(holiday, "id"))
        self.assertTrue(holiday.id == 1)

    def test_delete(self, m):
        register_uris({"space": ["delete"]}, m)

        response = self.space.delete()
        self.assertTrue(m.called)
        self.assertIsInstance(response, requests.Response)
        self.assertTrue(response.status_code == 204)

    def test_delete_calendar_token(self, m):
        register_uris({"space": ["delete_calendar_token"]}, m)

        response = self.space.delete_calendar_token()
        self.assertTrue(m.called)
        self.assertIsInstance(response, requests.Response)
        self.assertTrue(response.status_code == 204)

    def test_get_billing_settings(self, m):
        register_uris({"space": ["get_billing_settings"]}, m)

        billing = self.space.get_billing_settings()
        self.assertIsInstance(billing, SpaceBillingSettings)
        self.assertTrue(hasattr(billing, "space_id"))

    def test_get_holiday(self, m):
        register_uris({"space": ["get_holiday"]}, m)

        holiday = self.space.get_holiday(1)
        self.assertIsInstance(holiday, SpaceHoliday)
        self.assertTrue(hasattr(holiday, "id"))
        self.assertTrue(holiday.id == 1)

    def test_get_holidays(self, m):
        register_uris({"space": ["get_holidays"]}, m)

        holiday = self.space.get_holidays()
        self.assertIsInstance(holiday, PaginatedList)
        self.assertIsInstance(holiday[0], SpaceHoliday)
        self.assertTrue(hasattr(holiday[0], "id"))
        self.assertTrue(holiday[0].id == 1)

    def test_get_opening_hours(self, m):
        register_uris({"space": ["get_opening_hours"]}, m)

        resp = self.space.get_opening_hours()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 200)

    def test_update_calendar_token(self, m):
        register_uris({"space": ["update_calendar_token"]}, m)

        resp = self.space.update_calendar_token()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 200)
        self.assertTrue(hasattr(self.space, "calendarToken"))
        self.assertTrue(self.space.calendarToken == "abcdef-1234-5678")

    def test_update_hours(self, m):
        register_uris({"space": ["update_opening_hours"]}, m)

        resp = self.space.update_opening_hours()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 200)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/spaces/1",
            text=validate_update,
            status_code=200,
        )

        self.space.update(name="Operations Center")

        self.assertTrue(m.called)


@requests_mock.Mocker()
class testSpaceBillingSettings(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {"space": ["get_billing_settings"], "fabman": ["get_space_by_id"]}, m
            )

            self.space: Space = self.fabman.get_space(1)
            self.billing: SpaceBillingSettings = self.space.get_billing_settings()

    def test_instance(self, m):
        self.assertIsInstance(self.billing, SpaceBillingSettings)

    def test_str(self, m):
        string = str(self.billing)
        self.assertTrue(string.startswith("SpaceBillingSettings for space #1"))

    def test_delete_stripe(self, m):
        register_uris({"space": ["delete_stripe"]}, m)

        resp = self.billing.delete_stripe()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 204)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/spaces/1/billing-settings",
            text=validate_update,
            status_code=200,
        )

        self.billing.update()
        self.assertTrue(m.called)


@requests_mock.Mocker()
class TestSpaceHoliday(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"space": ["get_holiday"], "fabman": ["get_space_by_id"]}, m)

            self.space: Space = self.fabman.get_space(1)
            self.holiday: SpaceHoliday = self.space.get_holiday(1)

    def test_instance(self, m):
        self.assertIsInstance(self.holiday, SpaceHoliday)

    def test_str(self, m):
        string = str(self.holiday)
        self.assertTrue(string.startswith("SpaceHoliday #1: Emissary's Day"))

    def test_delete(self, m):
        register_uris({"space": ["delete_holiday"]}, m)

        resp = self.holiday.delete()
        self.assertTrue(m.called)
        self.assertIsInstance(resp, requests.Response)
        self.assertTrue(resp.status_code == 204)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/spaces/1/holidays/1",
            text=validate_update,
            status_code=200,
        )

        self.holiday.update()
        self.assertTrue(m.called)
