#!/usr/bin/env python

import unittest
from bottom_up_chart_parser import BottomUpChartParser

class Test(unittest.TestCase):
    bop = None

    def setUp(self):
        self.bop = BottomUpChartParser("sample.pcfg")

    def tearDown(self):
        pass

    def runTest(self):
        self.setUp()
        self.bop.parse('big cats and dogs saw Jack with telescopes')
        self.bop.chart.print_chart()
        self.tearDown()


if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:
        pass
