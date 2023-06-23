import unittest
import warnings
from datetime import datetime

import pytz 
import requests_mock

from fabman import Fabman
from fabman.member import Member
from tests import settings
from tests.util import register_uris

@requests_mock.Mocker()
class TestFabman(unittest.TestCase):  #pylint: disable=missing-class-docstring
    def setUp(self):
        self.fabman = Fabman(settings.API_KEY)
        
    # Test initializing the Fabman instance
    def test_init_no_api_key(self, m):  #pylint: disable=missing-function-docstring
        with self.assertRaises(
            ValueError,
            msg="No access token provided"
        ):
            Fabman(None)
    
    def test_init_empty_api_key(self, m):  #pylint: disable=missing-function-docstring
        with self.assertRaises(
            ValueError,
            msg="No access token provided"
        ):
            Fabman("")
    
    def test_init_warnings_for_http(self, m):  #pylint: disable=missing-function-docstring
        with warnings.catch_warnings(record=True):
            Fabman(settings.API_KEY, settings.BASE_URL_AS_HTTP)
            self.assertRaises(
                UserWarning,
                msg=(
                    "Please use HTTPS when possible. Fabman API may not respond as intended and user"
                    "data will not be secure",
                )
            )
            
    def test_init_warnings_for_bad_url(self, m):  #pylint: disable=missing-function-docstring
        with warnings.catch_warnings(record=True):
            Fabman(settings.API_KEY, settings.BASE_URL_AS_INVALID)
            self.assertRaises(
                UserWarning,
                msg=(
                    "An invalid `bad_url` provided. Will likely not work as intended." 
                )
            )
    
    def test_get_member(self, m):  #pylint: disable=missing-function-docstring
        register_uris({"fabman": ["get_by_id"]}, m)
        
        member = self.fabman.get_member(1)
        self.assertIsInstance(member, Member);
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "firstName"))
        
    def test_get_member_with_embed_str(self, m):  #pylint: disable=missing-function-docstring
        register_uris({"fabman": ["get_by_id_with_embed_str"]}, m)
        
        member = self.fabman.get_member(1, embed="memberPackages")
        self.assertIsInstance(member, Member);
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "_embedded"))
        
    def test_get_member_with_embed_single_list(self, m):  #pylint: disable=missing-function-docstring
        register_uris({"fabman": ["get_by_id_with_embed_str"]}, m)
        
        member = self.fabman.get_member(1, embed=["memberPackages"])
        self.assertIsInstance(member, Member);
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "_embedded"))
        
        self.assertTrue("memberPackages" in member._embedded)
        
    def test_get_member_with_embed_multi_list(self, m):
        register_uris({"fabman": ["get_by_id_with_embed_list_multi"]}, m)
        
        member = self.fabman.get_member(1, embed=["memberPackages", "trainings"])
        self.assertIsInstance(member, Member);
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "_embedded"))
        
        embeds = member._embedded
        self.assertTrue("memberPackages" in embeds)
        self.assertTrue("trainings" in embeds)