from fabman.util import combine_kwargs, flatten_kwarg, clean_headers, is_multivalued
import unittest
from itertools import chain
# pylint: disable=missing-class-docstring, missing-function-docstring, too-many-public-methods

import requests_mock

@requests_mock.Mocker()
class TestUtil(unittest.TestCase):
# is_multivalued()
    def test_is_multivalued_bool(self, m):
        self.assertFalse(is_multivalued(False))

    def test_is_multivalued_integer(self, m):
        self.assertFalse(is_multivalued(int(1)))

    def test_is_multivalued_str(self, m):
        self.assertFalse(is_multivalued("string"))

    def test_is_multivalued_unicode(self, m):
        self.assertFalse(is_multivalued("unicode"))

    def test_is_multivalued_bytes(self, m):
        self.assertFalse(is_multivalued(b"bytes"))

    def test_is_multivalued_list(self, m):
        self.assertTrue(is_multivalued(["item"]))

    def test_is_multivalued_list_iter(self, m):
        self.assertTrue(is_multivalued(iter(["item"])))

    def test_is_multivalued_tuple(self, m):
        self.assertTrue(is_multivalued(("item",)))

    def test_is_multivalued_tuple_iter(self, m):
        self.assertTrue(is_multivalued(iter(("item",))))

    def test_is_multivalued_set(self, m):
        self.assertTrue(is_multivalued({"element"}))

    def test_is_multivalued_set_iter(self, m):
        self.assertTrue(is_multivalued(iter({"element"})))

    def test_is_multivalued_dict(self, m):
        self.assertTrue(is_multivalued({"key": "value"}))

    def test_is_multivalued_dict_iter(self, m):
        self.assertTrue(is_multivalued(iter({"key": "value"})))

    def test_is_multivalued_dict_keys(self, m):
        self.assertTrue(is_multivalued({"key": "value"}.keys()))

    def test_is_multivalued_dict_values(self, m):
        self.assertTrue(is_multivalued({"key": "value"}.values()))

    def test_is_multivalued_dict_items(self, m):
        self.assertTrue(is_multivalued({"key": "value"}.items()))

    def test_is_multivalued_generator_expr(self, m):
        self.assertTrue(is_multivalued(item for item in ("item",)))

    def test_is_multivalued_generator_call(self, m):
        def yielder():
            yield "item"

        self.assertTrue(is_multivalued(yielder()))

    def test_is_multivalued_chain(self, m):
        self.assertTrue(is_multivalued(chain((1,), (2,))))

    def test_is_multivalued_zip(self, m):
        self.assertTrue(is_multivalued(zip((1,), (2,))))
        
    def test_clean_headers_no_auth(self, m):  #pylint: disable=missing-function-docstring
        headers = {
            "a": "b",
        }
        out = clean_headers(headers)
        self.assertDictEqual(headers, out)
        
    def test_clean_headers_auth(self, m):  #pylint: disable=missing-function-docstring
        headers = {
            "Authorization": "thisisatoken"
        }
        out = clean_headers(headers)
        self.assertEqual(out["Authorization"], "****oken")
        
    # combine_kwargs()
    def test_combine_kwargs_empty(self, m):
        result = combine_kwargs()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
    
    def test_combine_kwargs_single(self, m):
        result = combine_kwargs(var="test")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn(("var", "test"), result)
        
    def test_combine_kwargs_single_list_empty(self, m):
        result = combine_kwargs(var=[])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        
    def test_combine_kwargs_single_list_single_item(self, m):
        result = combine_kwargs(var=["test"])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn(("var", "test"), result)
        
    def test_combine_kwargs_single_list_multiple_items(self, m):
        result = combine_kwargs(var=["test1", "test2"])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIn(("var", "test1"), result)
        self.assertIn(("var", "test2"), result)