#!/usr/bin/env python

class BottomUpChartParser:

    grammar = None
    chart = None
    queue = None

    def __init__(self, grammar):
        pass

    def parse(self, sentence):
        '''
        1) Initialize empty chart
        2) Apply init_rule to each word in input sentence
        3) Until no more edges are added:
        - Apply predict_rule everywhere it applies (push to queue)
        - Apply fundamental rule everywhere it applies (push to queue)
        4) Return parses
        '''
        pass

    def init_rule(self, token, pos):
        pass # pos = start of Edge

    def predict_rule(self, complete_edge):
        pass

    def fundamental_rule(self, incomplete_edge):
        pass
