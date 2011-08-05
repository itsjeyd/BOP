#!/usr/bin/env python

class BottomUpChartParser:

    grammar = None
    chart = None
    queue = None

    def __init__(self, grammar):
        pass

    def parse(self, sentence):
        edges = None
        
        # Tokenize given sentence
        tokens = self.tokenize(sentence)
        n = len(tokens)
        
        '''1) Initialize empty chart'''
        chart = Chart(n+1)
        
        
        '''2) Apply init_rule to each word in input sentence'''
        pos = 0
        for token in tokens:
            edges = self.init_rule(token, pos)
            chart.add_edges() # add add_edges for multiple edges
            pos += 1
        
        '''3) Until no more edges are added:
        - Apply predict_rule everywhere it applies (push to queue)
        - Apply fundamental rule everywhere it applies (push to queue)'''
        
        
        '''4) Return parses'''
        
        pass
    
    def tokenize(self, sentence):
        ''' Separate sentence into list of tokens '''
        pass

    def init_rule(self, token, pos):
        pass # pos = start of Edge

    def predict_rule(self, complete_edge):
        pass

    def fundamental_rule(self, incomplete_edge):
        pass
    
    def generate_parses(self, chart):
        pass