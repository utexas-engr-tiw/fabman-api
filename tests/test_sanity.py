"""Sanity Checks"""
import unittest

import fabman


class SanityTest(unittest.TestCase):
    """Quick sanity check to make sure tests are working fine"""

    def test_sanity(self):
        """Quick sanity check to make sure tests are working fine"""
        self.assertEqual(1, 1)

    def test_fabman_import(self):
        """Quick sanity to check to ensure fabman is imported correctly"""
        key = '123'
        fab = fabman.Fabman(key)
        self.assertEqual(fab.__class__.__name__, 'Fabman')


if __name__ == '__main__':
    unittest.main()
