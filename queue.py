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
        return self.queue.pop() if not self.is_empty() else None

    def add_edge(self, edge):
        '''
        Push new edge onto queue
        '''
        self.queue.insert(0, edge)

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


class BestFirstQueue(Queue):
    '''
    This class implements a queue sorted according to edge probabilites
    '''

    from bisect import bisect

    def add_edge(self, new_edge):
        '''
        Push new edge onto queue

        Insert edge into the queue according to its probability
        '''
        pos = bisect([edge.get_prob() for edge in self.queue], new_edge)
        self.queue.insert(pos, new_edge)

