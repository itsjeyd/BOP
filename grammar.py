#!/usr/bin/env python

import re
from production_rule import ProductionRule

class Grammar:

    lexicon = None
    rules = None # Dictionary: First element on RHS (key), list of
                 # associated production rules (value)

    def __init__(self, grammar):
        self.lexicon = set()
        self.rules = {}
        self.load(grammar)

    def load(self, grammar):
        for line in open(grammar, 'r'):
            self.extract_rules(line)
        self.build_lexicon()
        self.standardize_rules()

    def extract_rules(self, line):
        lhs = self.extract_lhs(line)
        for rhs in self.extract_rhses(line):
            prob = self.extract_prob(rhs)
            rhs = self.seperate_dtrs(rhs)
            prod_rule = self.generate_prod_rule(lhs, rhs, prob)
            self.add_to_rules(prod_rule)

    def extract_lhs(self, line):
        return re.split(' *-> *', line)[0]
    
    def extract_rhses(self, line):
        rhses = re.split(' *-> *', line)[1]
        return [rhs for rhs in re.split(' *\| *', rhses)]

    def seperate_dtrs(self, rhs):
        dtrs = re.split('\[', rhs)[0]
        return [dtr for dtr in dtrs.split()]

    def extract_prob(self, rhs):
        return re.split('[\[\]]', rhs)[1]

    def generate_prod_rule(self, lhs, rhs, prob):
        '''
        Factory method; returns new instance of ProductionRule
        '''
        return ProductionRule(lhs, rhs, prob)

    def add_to_rules(self, prod_rule):
        first_rhs_element = prod_rule.get_rhs_element(0)
        if self.rules.has_key(first_rhs_element):
            self.rules[first_rhs_element].append(prod_rule)
        else:
            self.rules[first_rhs_element] = [prod_rule]
            
    def build_lexicon(self):
        self.lexicon = [key.strip('\'').strip('\"') for key \
                            in self.rules.keys() \
                            if key.startswith('\'') or key.startswith('\"')]
        
    def standardize_rules(self):
        for key in self.rules.keys():
            if key.startswith('\'') or key.startswith('\"'):
                self.rules[key.strip('\'').strip('\"')] = self.rules.pop(key)
            else:
                pass
        
    def get_lexicon(self):
        return self.lexicon
    
    def get_possible_parent_rules(self, token):
        '''
        Returns list of production rules whose
        first RHS element is the given token
        '''
        parents = self.rules[token]
        return self.rules[token]
