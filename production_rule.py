#!/usr/bin/env python

class ProductionRule:

    lhs = ''
    rhs = []
    prob = -1.0

    def __init__(self, lhs, rhs, prob):
        self.lhs = lhs
        self.rhs = rhs
        self.prob = prob

    def get_lhs(self):
        return self.lhs

    def get_rhs(self):
        return self.rhs

    def get_rhs_element(self, index):
        return self.rhs[index]

    def get_rhs_length(self):
        return len(self.rhs)

    def get_prob(self):
        return self.prob

    def print_prod_rule(self):
        print self.lhs + ' ---> ' \
            + self.format_rhs() \
            + ' [' + str(self.prob) + ']'

    def format_rhs(self):
        return self.rhs[0] if len(self.rhs) == 1 else ' '.join(self.rhs)
    
    def __str__(self):
        return "%s = %s (%s)" % (self.lhs, " ".join(self.rhs), self.prob)