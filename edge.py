#!/usr/bin/env python

class Edge:

    start = -1       # Starting node of the edge
    end = -1         # Ending node of the edge
    prob = -1.0      # Probability of the edge
    prod_rule = None # Object of type ProductionRule
    dot = -1         # Position of the dot on the RHS
    complete = False # Trigger shows whether dot is at end of RHS
    # subtrees = [] # List of immediate daughters of type Edge

    def __init__(self, start, end, prod_rule, dot, known_dtrs):
        self.start = start
        self.end = end
        self.prod_rule = prod_rule
        self.dot = dot
        self.prob = self.calc_prob(known_dtrs)
        self.set_complete()
    
    def get_start(self):
        ''' Returns the starting node of the edge '''
        return self.start

    def get_end(self):
        ''' Returns the ending node of the edge '''
        return self.end

    def get_prob(self):
        ''' Returns the probability of the edge '''
        return self.prob

    def get_prod_rule(self):
        ''' Returns the production rule on which the edge is based '''
        return self.prod_rule

    def get_dot(self):
        '''
        Returns the position of the dot on the right hand side.
        This indicates how far the production rule could already be applied.
        0 indicates no part of the right hand side applied yet.
        If the rule was completely applied, the dot position equals the number
            of right hand side tokens.
        '''
        return self.dot

    def calc_prob(self, known_dtrs):
        prob = self.prod_rule.get_prob()
        for dtr in known_dtrs:
            prob *= dtr.get_prob()
        return prob
    
    def is_complete(self):
        '''
        Returns true iff the dot is at the end of the production rule,
        i.e. the rule was completely applied.
        '''
        return self.complete

    def set_complete(self):
        '''
        Sets the completeness trigger to True if dot is at the end of the 
        right hand side and keeps it at False if it is not.
        '''
        if self.dot == self.prod_rule.get_rhs_length():
            self.complete = True

    def get_daughters(self):
        '''
        TODO: Dummy method.
        '''
        return []
    
    def __str__(self):
        lhs = self.prod_rule.get_lhs()
        rhs = self.prod_rule.get_rhs()[:]   # slicing creates a copy, allowing manipulation
        rhs.insert(self.dot, ".")
        rhs_string = " ".join(rhs)
        return "%s = %s (%i:%i, %s)" % (lhs, rhs_string, self.start, self.end, self.prob)
    
    # Methods for subtrees
