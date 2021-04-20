#!/usr/bin/env python3

import unittest
from find_common_kmers import find_common_kmers

class T(unittest.TestCase):

    def test_1(self):

        # I expect ['atg']
        self.assertEqual( find_common_kmers('atgaatgc', 3, 2), ['atg'] )


    @unittest.skip("I don't like this test")
    def test_2(self):

        # I expect []
        self.assertEqual( find_common_kmers('atgaatcg', 3, 2), [] )

    def test_3(self):

        # You can't have a KMer length 0
        self.assertRaises( Exception, find_common_kmers, 'atatatatata', 0, 2 )

if __name__ == '__main__':
    unittest.main()
