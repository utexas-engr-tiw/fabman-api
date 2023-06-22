import os
import sys
import configparser
import unittest

import fabman

conf = configparser.ConfigParser()
conf.read('config.ini')
key = conf['FABMAN']['API_TOKEN']

class SanityTest(unittest.TestCase):
    def test_sanity(self):
        """Quick sanity check to make sure tests are working fine"""
        self.assertEqual(1, 1)

    def test_fabman_import(self):
        """Quick sanity to check to ensure fabman is imported correctly"""
        fm = fabman.Fabman(key)
        self.assertEqual(fm.__class__.__name__, 'Fabman')
        
        
if __name__ == '__main__':
    unittest.main()