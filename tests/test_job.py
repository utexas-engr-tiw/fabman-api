"""Tests for the Jobs class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.job import Job
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestMembers(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_job_by_id"]}, m)

            self.job: Job = self.fabman.get_job(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)
