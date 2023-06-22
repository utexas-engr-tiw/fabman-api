import os
import sys
import configparser
import unittest
from fabman import Fabman
from fabman.member import Member

conf = configparser.ConfigParser()
conf.read('config.ini')
key = conf['FABMAN']['API_TOKEN']

class TestMembers(unittest.TestCase):
    
    def setUp(self):
        self.fabman = Fabman(key)

    def test_sanity(self):
        self.assertEqual(1, 1)
        
        
        