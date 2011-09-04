#!/usr/bin/env python

import itertools

class Chart:

    chart = None
    size = 0

    def __init__(self, size):
        self.chart = [[[] for col in range(size)] for row in range(size)]
        self.size = size

    def get_size(self):
        '''
        Return size of the chart
        '''
        return self.size

    def add_edge(self, edge):
        '''
        Add a newly created edge to the appropriate cell of the
        chart
        '''
        self.chart[edge.get_start()][edge.get_end()].append(edge)

    def get_edges(self, i, j):
        '''
        Return a list of all edges that live in a specific cell of the
        chart

        Every cell of the chart stores not only one edge but a *list*
        of edges; each of these edges spans the input string from i to
        j. In other words, the coordinates of a cell indicate length,
        start and end point of the edges stored in the cell.
        '''
        return self.chart[i][j]

    def get_edges_starting_at(self, i):
        '''
        Return all edges *starting* at a specific node

        The starting point of an edge is indicated by the row of the
        chart it lives in. Therefore, in order to obtain some kind of
        collection of all edges starting at a certain point i, we
        could simply return row i of the chart. In that case, we would
        end up with a list of lists. But since we do not care about
        the endpoints of the edges in question, what we are actually
        interested in is a *flat*/one-dimensional list of edges. The
        itertools.chain method provides the appropriate functionality
        for achieving this.
        '''
        return [edge for edge in itertools.chain(*self.chart[i])]

    def get_edges_ending_at(self, j):
        '''
        Return all edges *ending* at a specific node

        The ending point of an edge is indicated by the *column* of
        the chart it lives in.
        '''
        edges = []
        for row in self.chart:
            edges.append(row[j])
        return [edge for edge in itertools.chain(*edges)]


    def print_chart(self):
        '''
        Systematically print contents of each cell of the chart
        '''
        row = 0
        for line in self.chart:
            column = 0
            for cell in line:
                if len(cell) > 0:
                    cell_str = " | ".join([edge.__str__() for edge in cell])
                else:
                    cell_str = ""
                print "%i:%i : %s" % (row, column, cell_str)
                column += 1
            print "---------------"
            row += 1
