#!/usr/bin/env python

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