"""Tests for the TrainingCourse class."""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman import Fabman
from fabman.training_course import TrainingCourse
from tests import settings
from tests.util import register_uris, validate_update


@requests_mock.Mocker()
class TestTrainingCourse(unittest.TestCase):
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"fabman": ["get_training_course_by_id"]}, m)

            self.training_course: TrainingCourse = self.fabman.get_training_course(1)

    def test_sanity(self, m):
        self.assertEqual(1, 1)

    def test_instance(self, m):
        self.assertIsInstance(self.training_course, TrainingCourse)
        string = str(self.training_course)
        self.assertTrue(string == "TrainingCourse #1: Bajoran Worker Training")

    def test_delete(self, m):
        register_uris({"training_course": ["delete"]}, m)

        response = self.training_course.delete()

        self.assertTrue(response)

    def test_update(self, m):
        m.register_uri(
            "PUT",
            f"{settings.BASE_URL_WITH_VERSION}/training-courses/1",
            text=validate_update,
            status_code=200,
        )

        self.training_course.update(title="Bajoran Worker Training")
        self.assertTrue(m.called)
