#!/usr/bin/env python

class ProductionRule:

    lhs = ''
    rhs = []
    prob = -1.0

    def get_lhs(self): return self.lhs

    def get_rhs(self): return self.rhs

    def get_rhs_element(self, index): return self.rhs[index]

    def get_rhs_length(self): return len(self.rhs)

    def get_prob(self): return self.prob
