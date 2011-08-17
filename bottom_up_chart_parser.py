#!/usr/bin/env python

from chart import Chart
from queue import Queue
from edge import Edge
from grammar import Grammar
from parse_exception import ParseException

class BottomUpChartParser:

    grammar = None  # Grammar object that includes lexicon and dictionary
    queue = None    # Queue object on which new edges are stacked
    chart = None    # Chart object in which edges are stored for the final parse generation

    def __init__(self, grammar):
        self.grammar = Grammar(grammar)

    def parse(self, sentence):
        '''
        Parses a given sentence.
        This is the central method to be called from outside.
        '''
        ### Preprocessing ###
        # Tokenize the given sentence
        tokens = self.tokenize(sentence)

        # Check whether all tokens are contained in the lexicon
        unknown_words = self.get_unknown_words(tokens)
        if unknown_words:
            # TODO: Run fallback solutions to fix unknown words, else raise exception
            raise ParseException("Could not parse, due to the following unknown words: %s" % unknown_words)
            
        ### Main steps ###
        # 1) Initialize empty chart and queue
        n = len(tokens)
        self.chart = Chart(n+1)
        self.queue = Queue()
        
        # 2) Create initial edges for all tokens and push them to the queue
        self.init_rule(tokens)
        
        # 3) Repeat until no more edges are added:
        enough_parses_found = False
        while not self.queue.is_empty() and not enough_parses_found:
            # Push next queue element to the chart
            edge = self.queue.get_next_edge()
            self.chart.add_edge(edge)
            
            if edge.is_complete():
                # Apply prediction rule wherever it applies and push to queue
                self.predict_rule(edge)
            else:
                # Apply fundamental rule wherever it applies and push to queue
                self.fundamental_rule(edge)
        
        # 4) Return the generated parses
        return self.generate_parses()
        
    
    def tokenize(self, sentence):
        ''' 
        Separate a sentence into a list of tokens and return the list.
        Currently this simply splits at each whitespace character with no 
        special preprocessing
        '''
        return sentence.split()
    
    def sentence_contains_unknown_words(self, tokens):
        '''TODO: Legacy function. Will remove if no one misses it. '''
        unknown_words = self.get_unknown_words(tokens)
        return True if unknown_words else False
    
    def get_unknown_words(self, tokens):
        lexicon = self.grammar.get_lexicon()
        unknown_words = [token for token in tokens if token not in lexicon]
        return unknown_words

    def init_rule(self, tokens):
        '''
        Generates initial edges for all given tokens and adds them to the queue.
        
        Formal definition:
            For every word w_i add the edge [w_i -> . , (i, i+1)]
        '''
        node = -1   # Position between tokens of sentence (0 is start of sentence)
        for token in tokens:
            node += 1
            rules = self.grammar.get_rules_via_lhs(token)
            for rule in rules:
                edge = Edge(node, node+1, rule, 0, [])
                self.queue.add_edge(edge)

    def predict_rule(self, complete_edge):
        '''
        
        Formal definition: 
            For each complete edge [A -> alpha ., (i, j)] 
            and each production B -> A beta, 
            add the self-loop edge [B -> . A beta , (i, i)]
        
        Input: Complete edge
        Push to queue: List of incomplete edges (or empty list)
        '''
        start = complete_edge.get_start()
        lhs = complete_edge.get_prod_rule().get_lhs()
        parents = self.grammar.get_possible_parent_rules(lhs)
        
        for parent in parents:
            incomplete_edge = Edge(start, start, parent, 0, None)
            self.queue.add_edge(incomplete_edge)

    def fundamental_rule(self, incomplete_edge):
        '''
        
        Formal definition:
            If the chart contains the edges [A -> alpha . B beta, (i, j)] 
            and [B -> gamma . , (j, k)] 
            then add a new edge [A -> alpha B . beta, (i, k)].
        
        Input: Incomplete edge
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
                self.queue.add_edge(new_edge)
        
        ''' We have: start: i
                     end: j
                     LHS: A
                     RHS element immediately after dot: B
            We check chart for: LHS: B
                                Start: j
                                End: k
                                Complete: True 
            We create: edge(i,k) '''
    
    def generate_parses(self):
        pass
