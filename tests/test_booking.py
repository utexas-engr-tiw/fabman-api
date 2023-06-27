"""Tests for Booking class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.booking import Booking
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestBooking(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_booking_by_id"]}, m)

            self.booking: Booking = self.fabman.get_booking(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)
