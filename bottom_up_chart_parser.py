#!/usr/bin/env python
from chart import Chart
from queue import Queue
from edge import Edge

class BottomUpChartParser:

    grammar = None
    queue = None
    chart = None

    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, sentence):        
        ''' Tokenize given sentence '''
        tokens = self.tokenize(sentence)
        
        ''' 1) Initialize empty chart and queue '''
        n = len(tokens)
        self.chart = Chart(n+1)
        self.queue = Queue()
        
        ''' 2) Apply init_rule to each word in input sentence '''
        self.init_rule(tokens)
        
        ''' 3) Until no more edges are added '''
        enough_parses_found = False
        while not self.queue.is_empty() and not enough_parses_found:
            ''' Push queue element to chart '''
            edge = self.queue.get_next_element()
            self.chart.add_edge(edge)
            
            if edge.is_complete():
                ''' Apply predict_rule everywhere it applies (push to queue) '''
                self.predict_rule(edge)
            else:
                ''' Apply fundamental rule everywhere it applies (push to queue)'''
                self.fundamental_rule(edge)
        
        '''4) Return parses'''
        return self.generate_parses()
        
    
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

    def predict_rule(self, complete_edge):
        ''' Input: Complete edge
            Push to queue: List of incomplete edges (or empty list)
        '''
        start = complete_edge.get_start()
        lhs = complete_edge.get_prod_rule().get_lhs()
        parents = self.grammar.get_possible_parent_rules(lhs)
        
        for parent in parents:
            incomplete_edge = Edge(start, start, parent, 0, None)
            self.queue.add_element(incomplete_edge)

    def fundamental_rule(self, incomplete_edge):
        ''' Input: Incomplete edge
            Push to queue: List of edges (both complete and incomplete) or empty list
        '''
        ''' *** Incomplete Edge *** '''
        i = incomplete_edge.get_start()
        j = incomplete_edge.get_end()
        dot = incomplete_edge.get_dot()
        prod_rule = incomplete_edge.get_prod_rule()
        known_dtrs = incomplete_edge.get_daughters()
        ''' Get next RHS element after dot '''
        next_missing_daughter = prod_rule.get_rhs_element(dot)
        
        
        ''' *** Complete Edges *** '''
        complete_edges = [edge for edge in self.chart.get_edges_starting_at(j) if edge.is_complete()]
        for comp_edge in complete_edges:
            if next_missing_daughter == comp_edge.get_prod_rule().get_lhs():
                ''' *** New Edge *** '''
                k = comp_edge.get_end()
                new_edge = Edge(i, k, prod_rule, dot+1, known_dtrs+comp_edge)
                self.queue.add_element(new_edge)
        
        ''' We have: start: i
                     end: j
                     LHS: A
                     RHS element immediately after dot: B
            We check chart for: LHS: B
                                Start: j
                                End: k
                                Complete: True 
            We create: edge(i,k)'''
    
    def generate_parses(self):
        pass