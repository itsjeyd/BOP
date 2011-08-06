#!/usr/bin/env python
from chart import Chart
from queue import Queue

class BottomUpChartParser:

    grammar = None

    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, sentence):        
        ''' Tokenize given sentence '''
        tokens = self.tokenize(sentence)
        
        ''' 1) Initialize empty chart and queue '''
        n = len(tokens)
        chart = Chart(n+1)
        queue = Queue()
        
        ''' 2) Apply init_rule to each word in input sentence '''
        self.init_rule(tokens)
        
        ''' 3) Until no more edges are added '''
        enough_parses_found = False
        while not queue.is_empty() and not enough_parses_found:
            ''' Push queue element to chart '''
            edge = queue.get_next_element()
            chart.add_edge(edge)
            
            ''' Apply predict_rule everywhere it applies (push to queue) '''
            self.predict_rule()
            
            ''' Apply fundamental rule everywhere it applies (push to queue)'''
            self.fundamental_rule()
        
        '''4) Return parses'''
        return self.generate_parses(chart)
        
    
    def tokenize(self, sentence):
        ''' Separate sentence into list of tokens '''
        return sentence.split()

    def init_rule(self, tokens):
        pos = -1
        for token in tokens:
            pos += 1
            edge = self.init_rule(token, pos)
            self.queue.add_element(edge)
        pass # pos = start of Edge

    def predict_rule(self):
        pass

    def fundamental_rule(self):
        pass
    
    def generate_parses(self, chart):
        pass