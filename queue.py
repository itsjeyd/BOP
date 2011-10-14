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


from bisect import bisect

class BestFirstQueue(Queue):
    '''
    This class implements a queue sorted according to edge probabilites
    '''

    def add_edge(self, new_edge):
        '''
        Push new edge onto queue

        Insert edge into the queue according to its probability
        '''
        pos = bisect([edge.get_prob() for edge in self.queue], new_edge)
        self.queue.insert(pos, new_edge)

class AltSearchQueue(BestFirstQueue):
    '''
    This class implements a best first queue with a secondary queue and
    specialised get_next_edge functionality
    '''
    prioq_active = False
    prioq = None
    qdict = None

    def __init__(self, size):
        self.queue = []
        self.prioq = []
        self.qdict = [[{} for col in range(size)] for row in range(size)]

    def get_next_edge(self):
        '''
        Pop first element from active queue.
        Accesses priority queue if it was activated, otherwise base queue.
        If priority queue is active but empty, it is deactivated and the next
        base queue element is popped.
        '''
        # Pop from priority queue if it is active and not empty
        if self.prioq_active:
            if not self.is_priority_empty():
                return self.prioq.pop()
            else:   # If priority queue is empty, deactivate it
                self.prioq_active = False
        if not self.is_empty(): # Otherwise pop from base queue and clean qdict
            edge = self.queue.pop()
            self.remove_edge2dict(edge)
            return edge
        else:
            return None

    def add_edge(self, new_edge):
        '''
        Push new edge onto active queue
        '''
        if self.prioq_active:
            pos = bisect([edge.get_prob() for edge in self.prioq], new_edge)
            self.prioq.insert(pos, new_edge)
        else:
            pos = bisect([edge.get_prob() for edge in self.queue], new_edge)
            self.queue.insert(pos, new_edge)
            self.add_edge2dict(new_edge)

    def is_empty(self):
        '''
        Check whether both queues contain no items
        '''
        return True if (len(self.queue) + len(self.prioq)) == 0 else False

    def has_edge(self, edge):
        """
        Check if either queue contains the input edge
        """
        for queued_edge in self.queue:
            if queued_edge.is_equal_to(edge):
                return True
        for queued_edge in self.prioq:
            if queued_edge.is_equal_to(edge):
                return True
        return False

    def get_next_particular_edge(self, lhs, start, end):
        '''
        Pop first edge from base queue that is complete and
        has the right lhs, start and end.
        Returns None if no such edge is on the base queue
        '''
        if lhs in self.qdict[start][end] and len(self.qdict[start][end][lhs]) > 0:
            edge = self.qdict[start][end][lhs].pop()
            self.queue.remove(edge)
            return edge
        else:
            return None


    def activate_priority_queue(self):
        self.prioq_active = True

    def is_priority_active(self):
        ''' Returns true if priority queue is currently being used '''
        return self.prioq_active

    def is_priority_empty(self):
        '''
        Check whether the priority queue contains any items
        '''
        return True if len(self.prioq) == 0 else False

    def add_edge2dict(self, new_edge):
        ''' Internal auxiliary method that adds edge to queue dictionary
            if it is a complete edge
        '''
        if new_edge.is_complete():
            start = new_edge.get_start()
            end = new_edge.get_end()
            lhs = new_edge.get_prod_rule().get_lhs()
            if lhs in self.qdict[start][end]:
                pos = bisect([edge.get_prob() for edge in self.qdict[start][end][lhs]], new_edge)
                self.qdict[start][end][lhs].insert(pos, new_edge)
            else:
                self.qdict[start][end][lhs] = [new_edge]

    def remove_edge2dict(self, edge):
        ''' Internal auxiliary method that removes edge from queue dictionary '''
        if edge.is_complete():
            start = edge.get_start()
            end = edge.get_end()
            lhs = edge.get_prod_rule().get_lhs()
            self.qdict[start][end][lhs].remove(edge)
