import os
import sys
import configparser
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import fabman

conf = configparser.ConfigParser()
conf.read('config.ini')
key = conf['FABMAN']['API_TOKEN']

class SanityTest(unittest.TestCase):
    def test_sanity(self):
        self.assertEqual(1, 1)

    def test_fabman_import(self):
        fm = fabman.Fabman(key)
        self.assertEqual(fm.__class__.__name__, 'Fabman')
        
    def test_sanity_token(self):        
        fm = fabman.Fabman(key)
        self.assertEqual(fm.get_api_token(), key)
        
    def test_user_me(self):
        fm = fabman.Fabman(key)
        user = fm.get_user_me()
        self.assertEqual(user["members"][0]["memberNumber"], "1")
        
if __name__ == '__main__':
    unittest.main()