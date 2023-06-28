"""Tests for Booking class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.booking import Booking
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestBooking(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_booking_by_id"]}, m)

            self.booking: Booking = self.fabman.get_booking(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)

    def test_delete(self, m):
        register_uris({"booking": ["delete"]}, m)

        resp = self.booking.delete()
        self.assertTrue(m.called)
        self.assertTrue(resp.status_code == 204)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/bookings/1",
            text=validate_update,
            status_code=200,
        )

        self.booking.update()
        self.assertTrue(m.called)
