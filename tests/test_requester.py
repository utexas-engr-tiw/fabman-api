"""Tests for the Requester Class"""
# pylint: disable=missing-docstring, invalid-name, unused-argument

import unittest

import requests_mock

from fabman.requester import Requester
from tests import settings


@requests_mock.Mocker()
class TestRequester(unittest.TestCase):
    def setUp(self):
        self.requester = Requester(settings.BASE_URL_WITH_VERSION, settings.API_KEY)

    def test_sanity(self, m):
        self.assertEqual(1, 1)

    def test_instance(self, m):
        self.assertIsInstance(self.requester, Requester)

    def test_get(self, m):
        m.register_uri(
            "GET",
            f"{settings.BASE_URL_WITH_VERSION}/test",
            status_code=200,
        )

        resp = self.requester.request("GET", "/test")

        self.assertTrue(resp.status_code == 200)

    def test_post(self, m):
        m.register_uri(
            "POST",
            f"{settings.BASE_URL_WITH_VERSION}/test",
            status_code=201,
        )

        resp = self.requester.request("POST", "/test")

        self.assertTrue(resp.status_code == 201)

    def test_put(self, m):
        m.register_uri("PUT", f"{settings.BASE_URL_WITH_VERSION}/test", status_code=200)

        resp = self.requester.request("PUT", "/test")

        self.assertTrue(resp.status_code == 200)

    def test_delete(self, m):
        m.register_uri(
            "DELETE", f"{settings.BASE_URL_WITH_VERSION}/test", status_code=204
        )

        resp = self.requester.request("DELETE", "/test")

        self.assertTrue(resp.status_code == 204)

    def test_invalid(self, m):
        m.register_uri(
            "GAHBAGE", f"{settings.BASE_URL_WITH_VERSION}/test", status_code=420
        )

        with self.assertRaises(ValueError, msg="Invalid method GAHBAGE"):
            self.requester.request("GAHBAGE", "/test")
