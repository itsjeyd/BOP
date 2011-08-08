#!/usr/bin/env python

class Queue:
    ''' This class implements a standard FIFO queue '''

    queue = None

    def __init__(self):
        self.queue = []

    def get_next_edge(self):
        '''
        Pop first element from queue
        '''
        return self.queue.pop(0) if len(self.queue) >= 1 else None

    def add_edge(self, edge):
        '''
        Push new edge onto queue
        '''
        self.queue.append(edge)
