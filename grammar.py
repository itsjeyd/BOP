#!/usr/bin/env python

import re
from production_rule import ProductionRule

class Grammar:

    lexicon = None   # Set; the parser uses this to quickly check the
                     # input sentence for unknown words
    rules = None     # Dictionary: First element on RHS (key), list of
                     # associated production rules (value)

    def __init__(self, grammar_file):
        self.lexicon = set()
        self.rules = {}
        self.load_grammar(grammar_file)

    def load_grammar(self, grammar_file):
        '''
        Load grammar rules from a grammar file, extract lexical items
        from the rule set and put them into the lexicon, then clean up
        all remaining quotation marks from the rules
        '''
        self.load_rules_from_file(grammar_file)
        self.extract_lexicon_from_rules()
        self.remove_remaining_quot_marks()


    ### START internal auxiliary methods ###

    def load_rules_from_file(self, grammar_file):
        '''
        Populate the set of rules by extracting all
        possible rules from every line in the input grammar
        '''
        for line in open(grammar_file, 'r'):
            prod_rules = self.extract_rules_from_line(line)
            for prod_rule in prod_rules:
                self.add_to_rules(prod_rule)

    def extract_rules_from_line(self, line):
        '''
        Extract all rules from a single line of the input grammar,
        create ProductionRule instances from them and return a list of
        these instances
        '''
        rules_in_line = []
        lhs = self.extract_lhs_from_line(line)
        for rhs_string in self.extract_rhs_strings_from_line(line):
            prob = self.extract_prob_from_rhs_string(rhs_string)
            rhs = self.split_rhs_tokens(rhs_string)
            rules_in_line.append(self.generate_prod_rule(lhs, rhs, prob))
        return rules_in_line

    def extract_lhs_from_line(self, line):
        '''
        Extract LHS of production rule(s) represented by one line of
        the input grammar

        We allow a single line of the input grammar to look like this:

        S -> NP VP [1.0]

        Or like this:

        NP -> NNS [0.5] | JJ NNS [0.3] | NP CC NP [0.2]

        Lines providing information on the POS of individual words
        generally follow the same pattern, but they put the first -
        and only - element on their RHS in single or double quotes:

        NP -> 'Jack' [0.2]
        CC  -> "and" [0.9] | "or" [0.1]

        This method splits a single line of input at the arrow (->)
        and returns the element to the *left* of the arrow, which
        represents the LHS of all ProductionRules that can be
        extracted from the line as a whole
        '''
        return re.split(' *-> *', line)[0]

    def extract_rhs_strings_from_line(self, line):
        '''
        Extract RHS(es) of production rule(s) represented by one
        line of the input grammar

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
        return [rhs_string for rhs_string in re.split(' *\| *', rhses)]

    def extract_prob_from_rhs_string(self, rhs_string):
        '''
        Extract the probability of a production rule from its RHS

        After extracting it from a line of input, a single RHS looks
        like this:

        'JJ NNS [0.3]' (INPUT)

        This method extracts the probability of the given RHS and
        returns it so it can be used to construct a ProductionRule
        instance:

        0.3 (OUTPUT)
        '''
        return float(re.split('[\[\]]', rhs_string)[1])

    def split_rhs_tokens(self, rhs_string):
        '''
        Turn string representing an RHS into list of individual RHS
        tokens

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
        rhs = re.split('\[', rhs_string)[0]
        return [token for token in rhs.split()]

    def generate_prod_rule(self, lhs, rhs, prob):
        '''
        *** Factory method ***
        This method returns a new instance of ProductionRule with the
        given LHS, RHS, and probability
        '''
        return ProductionRule(lhs, rhs, prob)

    def add_to_rules(self, prod_rule):
        '''
        Adds a single production rule to the set of production rules

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

    def extract_lexicon_from_rules(self):
        '''
        Build a lexicon from all lexical items in the grammar

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

    def remove_remaining_quot_marks(self):
        '''
        Clean up quotation marks that remain on RHS of production
        rules representing lexical items after extracting the grammar
        from file

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
                    prod_rule.rhs = [stripped_rhs]
            else:
                pass


    ### START external methods ###

    def get_lexicon(self):
        '''
        Returns the lexicon
        '''
        return self.lexicon


    # TODO: I still don't like this function name
    def get_possible_parent_rules(self, token):
        '''
        Returns list of production rules whose
        first RHS element is the given token
        '''
        if self.rules.has_key(token):
            return self.rules[token]
        else:
            return []

    def print_rules(self):
        '''
        Pretty-prints all production rules of the grammar
        '''
        for prod_rules in self.rules.values():
            for prod_rule in prod_rules:
                print prod_rule.__str__()
