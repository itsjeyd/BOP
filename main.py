#!/usr/bin/env python

import sys
from bottom_up_chart_parser import BottomUpChartParser
from parse_exception import ParseException
from queue_exception import QueueException

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
        print 'Usage:\
        \nThe program will prompt you for three things:\
        \n\n(1) a sentence\
        \n(2) the maximum number of parses you would like to see for it;\
        \n    if you want to see all possible parses, this should be -1\
        \n(3) the parsing strategy: {fifo, bestfirst}\
        \n\nThe maximum number of parses defaults to 1.\
        \nThe parsing strategy defaults to bestfirst.\
        \nIf you are OK with the defaults, just press Enter without typing anything.\
        \nIf you want to exit the program, at any given point just type EXIT.\n\n'

    def initialize_parser(self):
        self.parser = BottomUpChartParser('sample.pcfg')

    def print_vocabulary(self):
        print 'Vocabulary: '
        print ', '.join(self.parser.grammar.get_lexicon())
        print '\n'

    def run(self):
        while True:
            sentence = raw_input('Sentence: ')
            if sentence == 'EXIT':
                print '\nGoodbye!\n'
                break
            number_of_parses = raw_input('Number of parses: ')
            if number_of_parses == 'EXIT':
                print '\nGoodbye!\n'
                break
            strategy = raw_input('Strategy: ')
            if strategy == 'EXIT':
                print '\nGoodbye!\n'
                break

            if number_of_parses == '':
                number_of_parses = 1
            if strategy == '':
                strategy = 'bestfirst'

            try:
                self.parser.parse(sentence, int(number_of_parses), strategy)
            except ParseException as e:
                print '\n' + e.value + '\n'
                self.print_vocabulary()
            except QueueException as e:
                print '\n' + e.value + '\n'



if __name__ == '__main__':
    main = Main()
    main.run()
