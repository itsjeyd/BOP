#!/usr/bin/env python

import unittest
from bottom_up_chart_parser import BottomUpChartParser

class Test(unittest.TestCase):
    bop = None  # The parser itself

    def setUp(self):
        self.bop = BottomUpChartParser("sample.pcfg")

    def tearDown(self):
        pass

    def test_parse_simple(self):
        self.bop.parse("Jack saw cats")
        self.bop.chart.print_chart()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
