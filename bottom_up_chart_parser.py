#!/usr/bin/env python

from chart import Chart
from queue import Queue
from edge import Edge
from production_rule import ProductionRule
from grammar import Grammar
from parse_exception import ParseException

class BottomUpChartParser:

    grammar = None  # Grammar object that includes lexicon and
                    # production rules
    queue = None    # Queue object on which new edges are stacked
    chart = None    # Chart object in which edges are stored for the
                    # final parse generation

    def __init__(self, grammar):
        self.grammar = Grammar(grammar)

    def parse(self, sentence, n=1):
        '''
        Parse the input sentence

        This is the central method to be called from outside.
        '''
        ### Preprocessing ###
        # Tokenize input sentence
        tokens = self.tokenize(sentence)

        # Check for unknown tokens
        unknown_words = self.get_unknown_words(tokens)
        if unknown_words:
            # TODO: Run fallback solutions to fix unknown words, else
            # raise exception
            raise ParseException("Could not parse, due to the following unknown words: %s" % unknown_words)

        ### Main steps ###
        # (1) Initialize empty chart and queue
        n = len(tokens)
        self.chart = Chart(n+1)
        self.queue = Queue()

        # (2) For every token, create a complete edge and push it to the queue
        self.init_rule(tokens)

        # (3) Repeat until no more edges are added
        #     or sufficient number of parses has been found:
        while not self.queue.is_empty() and not self.enough_parses_found(n):
            # (3.1) Add next element on queue to the chart
            edge = self.queue.get_next_edge()
            self.chart.add_edge(edge)

            # (3.2) If input edge is complete,
            #       apply predict rule and fundamental rule.
            #       If input edge is incomplete,
            #       apply fundamental rule only
            if edge.is_complete():
                self.predict_rule(edge)

            self.fundamental_rule(edge)

        # 4) Display generated parses
        print '========================='
        self.display_parses()
        print '========================='


    def tokenize(self, sentence):
        '''
        Separate a sentence into a list of tokens and return the list.
        Currently this simply splits at each whitespace character with no
        special preprocessing
        '''
        return sentence.split()

    def get_unknown_words(self, tokens):
        '''
        Check list of tokens for unknown words by consulting the
        lexicon and return them
        '''
        lexicon = self.grammar.get_lexicon()
        unknown_words = [token for token in tokens if token not in lexicon]
        return unknown_words

    def init_rule(self, tokens):
        '''
        Generate initial edges for all given tokens and add them to
        the queue

        Formal definition:
            For every word w_i add the edge [w_i -> . , (i, i+1)]
        '''
        node = -1   # Position between tokens of sentence
                    # (0 is start of sentence)
        for token in tokens:
            node += 1
            rule = ProductionRule(token, [], 1.0)
            edge = Edge(node, node+1, rule, 0, [])
            self.queue.add_edge(edge)

    def enough_parses_found(self, n):
        '''
        Check if enough parses have been found for the input sentence

        Return True if the number of complete S edges that the chart
        contains is >= the number of parses that the user wants, else
        False
        '''
        return True if len(self.chart.get_s_edges()) >= n else False

    def predict_rule(self, complete_edge):
        '''
        If the LHS of a complete edge can be the first RHS element of
        a production rule, create a self-loop edge with that rule and
        push it to the queue

        Input: Complete edge
        Push to queue: Incomplete self-loop edges

        Formal definition:
            For each complete edge [A -> alpha . , (i, j)]
            and each production rule  B -> A beta,
            add the self-loop edge [B -> . A beta , (i, i)]
        '''
        start = complete_edge.get_start()
        lhs = complete_edge.get_prod_rule().get_lhs()
        parent_rules = self.grammar.get_possible_parent_rules(lhs)

        for parent_rule in parent_rules:
            new_edge = Edge(start, start, parent_rule, 0, [])
            print "Predict rule: [%s] + [%s] = [%s]" \
                  % (complete_edge, parent_rule, new_edge)
            self.queue.add_edge(new_edge)

    def fundamental_rule(self, input_edge):
        '''
        If an incomplete edge can be advanced by a complete edge,
        create a new edge with the advanced dot.

        Create new edges (which can be complete or incomplete) by
        "advancing the dot", i.e. by matching incomplete edges with
        appropriate complete ones:

        (1) If the input edge is incomplete, find all complete edges
            - whose start node equals the end node of the input edge
            - whose LHS matches the RHS element
              that the input edge is currently looking for.
            If the input edge is complete, find all incomplete edges
            - whose end node equals the start node of the input edge
            - whose dot can be advanced by pairing them with the input
              edge.
        (2) From every pairing, create a new edge with the dot
            advanced over the RHS element that has just been found.
        (3) Push that edge to the queue.

        Input: Single edge
        Push to queue: Complete and incomplete edges

        Formal definition:
            If the chart contains the edges [A -> alpha . B beta, (i, j)]
            and [B -> gamma . , (j, k)]
            then add a new edge [A -> alpha B . beta, (i, k)].
        '''
        if input_edge.is_complete():
            j = input_edge.get_start()
            incomplete_edges = [edge for edge \
                                in self.chart.get_edges_ending_at(j) \
                                if not edge.is_complete()]
            complete_edges = [input_edge]
        else:
            j = input_edge.get_end()
            incomplete_edges = [input_edge]
            complete_edges = [edge for edge \
                              in self.chart.get_edges_starting_at(j) \
                              if edge.is_complete()]

        ### New Edges ###
        for incomp_edge in incomplete_edges:

            # Prepare info from incomplete edge that is necessary to ...
            prod_rule = incomp_edge.get_prod_rule()
            dot = incomp_edge.get_dot()
            next_missing_dtr = prod_rule.get_rhs_element(dot)
            for comp_edge in complete_edges:
                # ... check for compatibility with complete edges:
                if next_missing_dtr == comp_edge.get_prod_rule().get_lhs():

                    # Prepare additional info from incomplete edge
                    i = incomp_edge.get_start()
                    known_dtrs = incomp_edge.get_known_dtrs()

                    # Prepare info from complete edge
                    k = comp_edge.get_end()

                    # Combine info from both edges,
                    # and use it to create new edge
                    known_dtrs += [comp_edge]
                    new_edge = Edge(i, k, prod_rule, dot+1, known_dtrs)
                    print "Fundamental rule: [%s] + [%s] = [%s]" \
                          % (incomp_edge, comp_edge, new_edge)
                    # Add new edge to queue
                    self.queue.add_edge(new_edge)

    def display_parses(self):
        '''
        Display parse trees for all successful parses
        '''
        s_edges = self.chart.get_s_edges()
        for s_edge in s_edges:
            print '[ ' + self.build_parse_from_edge(s_edge, 'S') + ' ] ' \
                  + str(s_edge.get_prob())

    def build_parse_from_edge(self, edge, root):
        '''
        Recursively work your way down through the known daughters of
        the input edge; return a bracketed structure representing the
        parse tree.

        In order to obtain a complete structure, this
        method needs to be called with a string representing
        the appropriate tree root (as the second argument)
        '''
        if not edge.get_known_dtrs() == []:
            for dtr in edge.get_known_dtrs():
                root += ' [ ' + dtr.get_prod_rule().get_lhs() + self.build_parse_from_edge(dtr, '') + ' ]'
        return root
