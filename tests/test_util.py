"""Utility Function tests"""
import unittest

import requests_mock

from fabman.util import clean_headers

# pylint: disable=missing-class-docstring, missing-function-docstring, too-many-public-methods


@requests_mock.Mocker()
class TestUtil(unittest.TestCase):
    def test_clean_headers_no_auth(
        self, m
    ):  # pylint: disable=missing-function-docstring
        headers = {
            "a": "b",
        }
        out = clean_headers(headers)
        self.assertDictEqual(headers, out)

    def test_clean_headers_auth(self, m):  # pylint: disable=missing-function-docstring
        headers = {"Authorization": "thisisatoken"}
        out = clean_headers(headers)
        self.assertEqual(out["Authorization"], "****oken")
