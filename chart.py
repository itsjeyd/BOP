#!/usr/bin/env python

import itertools

class Chart:

    chart = None
    
    def __init__(self, size):
        self.chart = [[None for col in range(size)] for row in range(size)]

    def add_edge(self, edge):
        '''
        Since all cells in the chart are initialized as None, we can't
        just append the edge to the appropriate cell. Instead, we need
        to first check whether or not the cell already contains one or
        more edges. If it does, we simply append; if it does not, we
        replace it with a list containing the new edge as the only
        element.
        '''
        i, j = edge.get_start(), edge.get_end()
        self.chart[i][j] = [edge] if self.chart[i][j] == None \
            else self.chart[i][j].append(edge)

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
