#!/usr/bin/env python

class Chart:

    chart = []
    size = 0

    def __init__(self, size):
        pass

    def get_size(self):
        pass

    def add_edge(self, edge):
        pass

    def get_edges(self, i, j):
        pass

    def get_edges_starting_at(self, i):
        pass

    def get_edges_ending_at(self, j):
        pass

    def get_s_edges(self):
        pass

    def print_chart(self):
        pass


class Edge:

    start = -1
    end = -1
    prob = -1.0
    prod_rule = None
    dot = -1
    complete = False
    known_dtrs = None

    def __init__(self, start, end, prod_rule, dot, known_dtrs):
        pass

    def __str__(self):
        pass

    def calc_prob(self, prod_rule, known_dtrs):
        pass

    def set_complete(self):
        pass

    def get_start(self):
        pass

    def get_end(self):
        pass

    def get_prob(self):
        pass

    def get_prod_rule(self):
        pass

    def get_dot(self):
        pass

    def is_complete(self):
        pass

    def get_known_dtrs(self):
        pass


class Queue:

    queue = None

    def __init__(self):
        pass

    def get_next_edge(self):
        pass

    def add_edge(self):
        pass

    def is_empty(self):
        pass


class ProductionRule:

    lhs = ''
    rhs = []
    prob = -1.0


    def __init__(self, lhs, rhs, prob):
        pass

    def __str__(self):
        pass

    def get_lhs(self):
        pass

    def get_rhs(self):
        pass

    def get_rhs_element(self, index):
        pass

    def get_rhs_length(self):
        pass

    def get_prob(self):
        pass


class BottomUpChartParser:

    grammar = None
    chart = None
    queue = None

    def __init__(self, grammar):
        pass

    def parse(self, sentence, n=1):
        '''
        (1) Tokenize input sentence
        (2) Check for unknown words
        (3) Initialize empty chart and queue
        (4) Apply init_rule to each word in input sentence
        (5) Until no more edges are added or enough parses found:
            - Transfer edge from queue to chart
            - Apply predict rule everywhere it applies
            - Apply fundamental rule everywhere it applies
            - Push new edges to queue
        (6) Display parses
        '''
        pass

    def tokenize(self, sentence):
        pass

    def get_unknown_words(self, tokens):
        pass

    def init_rule(self, token, pos):
        pass

    def enough_parses_found(self, n):
        pass

    def predict_rule(self, complete_edge):
        pass

    def fundamental_rule(self, incomplete_edge):
        pass

    def display_parses(self):
        pass

    def build_parse_from_edge(self, edge, root):
        pass


class Grammar:

    rules = None
    lexicon = None

    def __init__(self, grammar_file):
        pass

    def load_grammar(self, grammar_file):
        pass

    def load_rules_from_file(self, grammar_file):
        pass

    def extract_rules_from_line(self, line):
        pass

    def extact_lhs_from_line(self, line):
        pass

    def extract_rhs_strings_from_line(self, line):
        pass

    def extract_prob_from_rhs_string(self, rhs_string):
        pass

    def split_rhs_tokens(self, rhs_string):
        pass

    def generate_prod_rule(self, lhs, rhs, prob):
        pass

    def add_to_rules(self, prod_rule):
        pass

    def extract_lexicon_from_rules(self):
        pass

    def remove_remaining_quot_marks(self):
        pass

    def get_lexicon(self):
        pass

    def get_possible_parent_rules(self, token):
        pass

    def print_rules(self):
        pass


class ParseException:
    def __init__(self, value):
        pass

    def __str__(self):
        pass


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_simple(self):
        pass
