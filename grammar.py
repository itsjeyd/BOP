#!/usr/bin/env python

import re
from production_rule import ProductionRule

class Grammar:

    lexicon = None   # Set; the parser uses this to quickly check the
                     # input sentence for unknown words
    rules = None     # Dictionary: First element on RHS (key), list of
                     # associated production rules (value)

    def __init__(self, grammar):
        self.lexicon = set()
        self.rules = {}
        self.load(grammar)

    def load(self, grammar):
        '''
        This method is in charge of getting everything set up
        '''
        self.build_rules(grammar)
        self.build_lexicon()
        self.remove_quotation_marks()

    ### Internal auxiliary methods ###
    def build_rules(self, grammar):
        '''
        This method populates the set of rules by extracting all
        possible rules from every line in the input grammar
        '''
        for line in open(grammar, 'r'):
            self.extract_rules(line)

    def extract_rules(self, line):
        '''
        This method extracts all possible rules from a single line of
        the input grammar, creates ProductionRule instances from them
        and adds appropriate entries for these instances to self.rules
        '''
        lhs = self.extract_lhs(line)
        for rhs in self.extract_rhses(line):
            prob = self.extract_prob(rhs)
            rhs = self.seperate_dtrs(rhs)
            prod_rule = self.generate_prod_rule(lhs, rhs, prob)
            self.add_to_rules(prod_rule)

    def extract_lhs(self, line):
        '''
        We allow a single line of the input grammar to look like this:

        S -> NP VP [1.0]

        Or like this:

        NP -> NNS [0.5] | JJ NNS [0.3] | NP CC NP [0.2]

        Lines providing information on the POS of individual words
        generally follow the same pattern, but they put the first (and
        only) element on their RHS in single or double quotes:

        NP -> 'Jack' [0.2]
        CC  -> "and" [0.9] | "or" [0.1]

        This method splits a single line of input at the arrow (->)
        and returns the element to the *left* of the arrow, which
        represents the LHS of all ProductionRules that can be
        extracted from the line as a whole
        '''
        return re.split(' *-> *', line)[0]

    def extract_rhses(self, line):
        '''
        We allow a single line of the input grammar to look like this:

        S -> NP VP [1.0]

        Or like this:

        NP -> NNS [0.5] | JJ NNS [0.3] | NP CC NP [0.2]

        Lines providing information on the POS of individual words
        generally follow the same pattern, but they put the first (and
        only) element on their RHS in single or double quotes:

        NP -> 'Jack' [0.2]
        CC  -> "and" [0.9] | "or" [0.1]

        This method first splits a single line of input at the arrow
        (->). It then splits the element to the *right* of the arrow
        at the bar indicating disjunction (|), returning a list of all
        possible RHSes of the element to the left of the arrow and
        their probabilities, e.g.:

        ['NNS [0.5]', 'JJ NNS [0.3]', 'NP CC NP [0.2]']
        ["'Jack' [0.2]"]
        '''
        rhses = re.split(' *-> *', line)[1]
        return [rhs for rhs in re.split(' *\| *', rhses)]

    def seperate_dtrs(self, rhs):
        '''
        After extracting it from a line of input, a single RHS looks
        like this:

        'JJ NNS [0.3]' (INPUT)

        The RHS of a ProductionRule, however, is defined as a *list*
        of strings -- with each string representing one individual
        element of the RHS -- and should therefore look like this:

        ['JJ', 'NNS'] (OUTPUT)

        This method returns the list of daughters we are looking for
        by
        - removing the probability from the input string
        - breaking down the remaining string appropriately
        '''
        dtrs = re.split('\[', rhs)[0]
        return [dtr for dtr in dtrs.split()]

    def extract_prob(self, rhs):
        '''
        After extracting it from a line of input, a single RHS looks
        like this:

        'JJ NNS [0.3]' (INPUT)

        This method extracts the probability of the given RHS and
        returns it so it can be used to construct a ProductionRule
        instance:

        0.3 (OUTPUT)
        '''
        return float(re.split('[\[\]]', rhs)[1])

    def generate_prod_rule(self, lhs, rhs, prob):
        '''
        *** Factory method ***
        This method returns a new instance of ProductionRule with the
        given LHS, RHS, and probability
        '''
        return ProductionRule(lhs, rhs, prob)

    def add_to_rules(self, prod_rule):
        '''
        To facilitate rule lookup in the predict step of the parsing
        process, production rules are stored in a dictionary (by the
        first element on their RHS) instead of a plain list. This means
        that we can not simply append a given rule.

        Instead, this method checks if the first element on the RHS of
        the given ProductionRule has already been added as a key to
        self.rules. If it has, it simply adds the rule to the
        appropriate entry. If it has not, it creates a new entry with
        the first RHS element as a key and a list containing the rule
        as its value
        '''
        first_rhs_element = prod_rule.get_rhs_element(0)
        if self.rules.has_key(first_rhs_element):
            self.rules[first_rhs_element].append(prod_rule)
        else:
            self.rules[first_rhs_element] = [prod_rule]

    def build_lexicon(self):
        '''
        Lines containing lexical items and POS information look like
        this:

        NP -> 'Jack' [0.2]
        CC  -> "and" [0.9] | "or" [0.1]

        When first building self.rules, quotation marks
        surrounding the lexical items are *not* stripped away. This
        means that before cleanup, lexical items are easily
        distinguishable from non-terminals in the set of RHS elements
        that make up the keys for self.rules.

        This method makes use of this fact. It populates the lexicon
        with exactly those keys it recognizes as lexical items. Before
        adding each item it strips away all quotation marks, as they
        are useless in the lexicon itself
        '''
        self.lexicon = [key.strip('\'').strip('\"') for key \
                            in self.rules.keys() \
                            if key.startswith('\'') or key.startswith('\"')]

    def remove_quotation_marks(self):
        '''
        Lines containing lexical items and POS information look like
        this:

        NP -> 'Jack' [0.2]
        CC  -> "and" [0.9] | "or" [0.1]

        When first building self.rules, quotation marks
        surrounding the lexical items are *not* stripped away.

        This method removes all quotation marks. It should only be
        called *after* the lexicon has been built.
        '''
        for rhs, prod_rules in self.rules.items():
            if rhs.startswith('\'') or rhs.startswith('\"'):
                stripped_rhs = rhs.strip('\'').strip('\"')
                self.rules[stripped_rhs] = self.rules.pop(rhs)
                for prod_rule in prod_rules:
                    prod_rule.rhs = [stripped_rhs] # Setter method for
                                                   # RHS of
                                                   # ProductionRule
                                                   # instance would be
                                                   # cleaner?
            else:
                pass


    ### External methods ###
    def get_lexicon(self):
        '''
        Returns the lexicon
        '''
        return self.lexicon


    ## TODO: I still don't like this function name
    def get_possible_parent_rules(self, token):
        '''
        Returns list of production rules whose
        first RHS element is the given token
        '''
        return self.rules[token]

    def print_rules(self):
        '''
        Pretty-prints all production rules of the grammar
        '''
        for prod_rules in self.rules.values():
            for prod_rule in prod_rules:
                prod_rule.print_prod_rule()
