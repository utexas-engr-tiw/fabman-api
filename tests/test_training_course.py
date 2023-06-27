"""Tests for the TrainingCourse class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.training_course import TrainingCourse
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestTrainingCourse(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_training_course_by_id"]}, m)

            self.training_course: TrainingCourse = self.fabman.get_training_course(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)
