"""Tests for the Space class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.space import Space
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestSpace(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_space_by_id"]}, m)

            self.space: Space = self.fabman.get_space(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)
