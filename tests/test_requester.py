"""Tests for the Requester Class"""
# pylint: disable=missing-docstring, invalid-name, unused-argument, protected-access

import json
import unittest

import requests_mock

from fabman.exceptions import (
    BadRequest,
    Conflict,
    FabmanException,
    ForbiddenError,
    InvalidAccessToken,
    RateLimitExceeded,
    Unauthorized,
    UnprocessableEntity,
)
from fabman.requester import Requester
from tests import settings
from tests.util import test_exceptions


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

    def test_cache(self, m):
        m.register_uri("GET", f"{settings.BASE_URL_WITH_VERSION}/test", status_code=200)
        for i in range(4):
            self.assertTrue(len(self.requester._Requester__cache) == i)
            self.requester.request("GET", "/test")
            self.assertTrue(len(self.requester._Requester__cache) == i + 1)

        self.requester.request("GET", "/test")
        self.assertTrue(len(self.requester._Requester__cache) == 4)

    def test_400(self, m):
        m.register_uri(
            "GET",
            f"{settings.BASE_URL_WITH_VERSION}/test_400",
            text=test_exceptions,
            status_code=400,
        )

        with self.assertRaises(BadRequest, msg="Bad Request"):
            self.requester.request("GET", "/test_400")

            self.assertTrue(m.called)

    def test_401(self, m):
        m.register_uri(
            "GET",
            f"{settings.BASE_URL_WITH_VERSION}/test_401_invalid",
            text=test_exceptions,
            status_code=401,
        )

        with self.assertRaises(InvalidAccessToken, msg="Invalid access token"):
            self.requester.request("GET", "/test_401_invalid")

            self.assertTrue(m.called)

    def test_401_unauthorized(self, m):
        m.register_uri(
            "GET",
            f"{settings.BASE_URL_WITH_VERSION}/test_401_unauthorized",
            text=test_exceptions,
            status_code=401,
        )

        with self.assertRaises(Unauthorized, msg="Unauthorized"):
            self.requester.request("GET", "/test_401_unauthorized")

            self.assertTrue(m.called)

    def test_403(self, m):
        m.register_uri(
            "GET",
            f"{settings.BASE_URL_WITH_VERSION}/test_403",
            text=test_exceptions,
            status_code=403,
        )

        with self.assertRaises(ForbiddenError, msg="Forbidden"):
            self.requester.request("GET", "/test_403")

            self.assertTrue(m.called)

    def test_404(self, m):
        m.register_uri(
            "GET",
            f"{settings.BASE_URL_WITH_VERSION}/test_404",
            text=test_exceptions,
            status_code=404,
        )

        with self.assertRaises(FabmanException, msg="Not Found"):
            self.requester.request("GET", "/test_404")

            self.assertTrue(m.called)

    def test_409(self, m):
        m.register_uri(
            "GET",
            f"{settings.BASE_URL_WITH_VERSION}/test_409",
            text=test_exceptions,
            status_code=409,
        )

        with self.assertRaises(Conflict, msg="Conflict"):
            self.requester.request("GET", "/test_409")

            self.assertTrue(m.called)

    def test_422(self, m):
        m.register_uri(
            "GET",
            f"{settings.BASE_URL_WITH_VERSION}/test_422",
            text=test_exceptions,
            status_code=422,
        )

        with self.assertRaises(UnprocessableEntity, msg="Unprocessable Entity"):
            self.requester.request("GET", "/test_422")

            self.assertTrue(m.called)

    def test_429(self, m):
        m.register_uri(
            "GET",
            f"{settings.BASE_URL_WITH_VERSION}/test_429",
            text=test_exceptions,
            status_code=429,
        )

        with self.assertRaises(RateLimitExceeded, msg="Rate Limit Exceeded"):
            self.requester.request("GET", "/test_429")

            self.assertTrue(m.called)

    def test_4xx(self, m):
        m.register_uri(
            "GET",
            f"{settings.BASE_URL_WITH_VERSION}/test_420",
            text=test_exceptions,
            status_code=420,
        )

        with self.assertRaises(FabmanException, msg="Unknown 420"):
            self.requester.request("GET", "/test_420")

            self.assertTrue(m.called)
