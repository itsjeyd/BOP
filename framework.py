#!/usr/bin/env python

class Chart:

    chart = []
    
    def __init__(self, size):
        pass

    def add_edge(self, edge):
        pass

    def get_edges(self, i, j):
        pass

    def get_edges_starting_at(self, i):
        pass


class Edge:

    start = -1
    end = -1
    prob = -1.0
    prod_rule = None # Object of type ProductionRule
    dot = -1
    complete = False
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

    def is_complete(self):
        return self.complete

    def set_complete(self):
        pass

    def get_daughters(self):
        pass

    # Methods for subtrees


class Queue:

    def get_next_element(self):
        pass

    def add_element(self):
        pass
    

class FIFOQueue(Queue):
    pass

class ProductionRule:

    lhs = ''
    rhs = []
    prob = -1.0

    
    def __init__(self, lhs, rhs, prob):
        pass

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

    def tokenize(self, sentence):
        return sentence.split()

    def init_rule(self, token, pos):
        pass # pos = start of Edge

    def predict_rule(self, complete_edge):
        pass

    def fundamental_rule(self, incomplete_edge):
        pass

    def generate_parses(self):
        pass


class Grammar:

    rules = None # Dictionary: First element on RHS (key), list of
                 # associated production rules (value)

    def __init__(self, file):
        pass # calls load

    def load(self):
        pass

    def get_possible_parent_rules(self, token):
        ''' Returns list of production rules whose
            first RHS element is the given token
        '''
        pass
    

# class Main: pass
