import os
import sys
import configparser
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import fabman

conf = configparser.ConfigParser()
conf.read('config.ini')

key = conf['FABMAN']['API_TOKEN']
fm = fabman.Fabman(key)

class EndpointTest(unittest.TestCase):
    def test_user_me(self):
        user = fm.get_user_me()
        self.assertEqual(user["members"][0]["memberNumber"], "1")
    
    def test_accounts(self):
        accounts = fm.get_accounts()
        self.assertGreaterEqual(len(accounts), 1)
        self.assertLessEqual(len(accounts), 50)
        
if __name__ == "__main__":
    unittest.main()