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
        return self.queue.pop(0) if not self.is_empty() else None

    def add_edge(self, edge):
        '''
        Push new edge onto queue
        '''
        self.queue.append(edge)

    def is_empty(self):
        '''
        Check whether or not queue contains any items
        '''
        return True if len(self.queue) == 0 else False

    def has_edge(self, edge):
        """
        Check if queue contains the input edge
        """
        for queued_edge in self.queue:
            if queued_edge.is_equal_to(edge):
                return True
        return False
