#!/usr/bin/env python

import itertools

class Chart:

    chart = None
    size = 0

    def __init__(self, size):
        self.chart = [[[] for col in range(size)] for row in range(size)]
        self.size = size

    def get_size(self):
        return self.size

    def add_edge(self, edge):
        '''
        Adds a newly created edge to the appropriate cell of the
        chart.
        '''
        self.chart[edge.get_start()][edge.get_end()].append(edge)

    def get_edges(self, i, j):
        '''
        Every cell of the chart stores not only one edge but a *list*
        of edges; each of these edges spans the input string from i to
        j. In other words, the coordinates of a cell indicate length,
        start and end point of the edges stored in the cell. As a
        consequence, this method had to be renamed to reflect the fact
        that it returns a list of edges (and not just a single edge).
        '''
        return self.chart[i][j]

    def get_edges_starting_at(self, i):
        '''
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
        edges = []
        for row in self.chart:
            edges.append(row[j])
        return [edge for edge in itertools.chain(*edges)]


    def print_chart(self):
        row = 0
        for line in self.chart:
            column = 0
            for cell in line:
                if len(cell) > 0:
                    elems = []
                    for elem in cell:
                        elems.append(elem.__str__())
                    cell_str = " | ".join(elems)
                else:
                    cell_str = ""
                print "%i:%i = %s" % (row,column,cell_str)
                column += 1
            print "---------------"
            row += 1
