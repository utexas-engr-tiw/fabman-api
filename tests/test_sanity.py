import os
import sys
import configparser
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import fabman

class SanityTest(unittest.TestCase):
    def test_sanity(self):
        self.assertEqual(1, 1)

    def test_fabman_import(self):
        fm = fabman.Fabman()
        self.assertEqual(fm.__class__.__name__, 'Fabman')
        
    def test_sanity_token(self):
        conf = configparser.ConfigParser()
        conf.read('config.ini')
        key = conf['FABMAN']['API_TOKEN']
        fm = fabman.Fabman(key)
        self.assertEqual(fm.get_api_token(), key)
        
if __name__ == '__main__':
    unittest.main()