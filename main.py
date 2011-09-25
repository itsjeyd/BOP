#!/usr/bin/env python

import sys
from bottom_up_chart_parser import BottomUpChartParser

class Main:

    parser = None

    def __init__(self):
        self.print_welcome()
        self.print_usage()
        self.initialize_parser()
        self.print_vocabulary()

    def print_welcome(self):
        print '\n\n;;;;;;;;;;;;;;;;;;;;;;;'
        print ';;; Welcome to BOP! ;;;'
        print ';;;;;;;;;;;;;;;;;;;;;;;\n\n'

    def print_usage(self):
        print 'Usage:\nThe program will prompt you for three things:\n\n(1) a sentence\n(2) the maximum number of parses you would like to see for it\n(3) the parsing strategy: {none,bestfirst}\n\nThe maximum number of parses defaults to 1. The parsing strategy defaults to bestfirst. If you are OK with the defaults, just press Enter without typing anything. If you want to exit the program, at any given point just type EXIT.\n\n'

    def initialize_parser(self):
        self.parser = BottomUpChartParser('sample.pcfg')

    def print_vocabulary(self):
        print 'Vocabulary: '
        print ', '.join(self.parser.grammar.get_lexicon())
        print '\n'

    def main(self):
        interactive = True
        while interactive:
            sentence = raw_input('Sentence: ')
            if sentence == 'EXIT':
                print '\nGoodbye!\n'
                break
            number_of_parses = input('Number of parses: ')
            if number_of_parses == 'EXIT':
                print '\nGoodbye!\n'
                break
            strategy = raw_input('Strategy: ')
            if strategy == 'EXIT':
                print '\nGoodbye!\n'
                break
            self.parser.parse(sentence, number_of_parses, strategy)
            interactive = False



if __name__ == '__main__':
    main = Main()
    main.main()