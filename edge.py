#!/usr/bin/env python

class Edge:

    start = -1
    end = -1
    prob = -1.0
    prod_rule = None # Object of type ProductionRule
    dot = -1
    complete = False
    # subtrees = [] # List of immediate daughters of type Edge

    def __init__(self, start, end, prod_rule, dot, known_dtrs):
        self.start = start
        self.end = end
        self.prod_rule = prod_rule
        self.dot = dot
        self.prob = self.calc_prob(known_dtrs)
        self.set_complete()
    
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

    def calc_prob(self, known_dtrs):
        prob = self.prod_rule.get_prob()
        for dtr in known_dtrs:
            prob *= dtr.get_prob()
        return prob
    
    def is_complete(self):
        return self.complete

    def set_complete(self):
        if self.dot == len(self.prod_rule.get_rhs()):
            self.complete = True

    # Methods for subtrees
