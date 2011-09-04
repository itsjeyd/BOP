#!/usr/bin/env python

class ProductionRule:

    lhs = '' # Left-hand side of the production rule; a single non-terminal
    rhs = [] # Right-hand side of the production rule; a list of
             # terminals or non-terminals
    prob = -1.0 # Probability of the production rule as specified by
                # the grammar

    def __init__(self, lhs, rhs, prob):
        self.lhs = lhs
        self.rhs = rhs
        self.prob = prob

    def __str__(self):
        '''
        Return string representation of the production rule
        '''
        return "%s = %s (%s)" % (self.lhs, " ".join(self.rhs), self.prob)

    def get_lhs(self):
        '''
        Return LHS of the production rule
        '''
        return self.lhs

    def get_rhs(self):
        '''
        Return RHS of the production rule
        '''
        return self.rhs

    def get_rhs_element(self, index):
        '''
        Return a specific element on the RHS of the production rule
        '''
        return self.rhs[index]

    def get_rhs_length(self):
        '''
        Return the number of elements on the RHS of the production
        rule
        '''
        return len(self.rhs)

    def get_prob(self):
        '''
        Return the probability of the production rule
        '''
        return self.prob
