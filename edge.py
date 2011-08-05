#!/usr/bin/env python

class Edge:

    start = -1
    end = -1
    prob = -1.0
    prod_rule = None # Object of type ProductionRule
    dot = -1
    # complete = False
    # subtrees = [] # List of immediate daughters of type Edge

    def __init__(self, start, end, prod_rule, dot, known_dtrs):
        pass

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_prob(self):
        return self.prob

    def get_prod_rule(self):
        return self.prod_rule

    def get_dot(self):
        return self.dot

    def calc_prob(self, prod_rule, known_dtrs):
        pass # called by __init__

    # Methods for complete

    # Methods for subtrees
