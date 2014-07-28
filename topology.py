# -*- coding: utf-8 -*-

import networkx as nx


def moore_lattice(rows, columns, radius=1, periodic=False):
    """ Return the 2d lattice graph of rows x columns nodes, each connected to
    its nearest 8 neighbors within a given radius.  Optional argument
    periodic=True will connect boundary nodes via periodic boundary conditions.

    Parameters:

    *rows*
        The number of rows to be in the graph
    *columns*
        The number of columns to be in the graph
    *radius*
        The radius of interactions in the graph (there will be an edge
        between a node and all other nodes within N hops)
    *periodic*
        Prevent edge effects using periodic boundaries

    """
    G = nx.empty_graph()
    G.add_nodes_from(list(range(rows * columns)))

    for n in G.nodes():
        myrow = n // columns
        mycol = n % columns

        for r in range(myrow - radius, myrow + radius + 1):
            if periodic == False and (r < 0 or r >= rows):
                continue

            for c in range(mycol - radius, mycol + radius + 1):
                if periodic == False and (c < 0 or c >= columns):
                    continue

                neighbor = (columns * (r % rows)) + (c % columns)

                if n != neighbor:
                    G.add_edge(n, neighbor)

    return G

def vonneumann_lattice(rows, columns, periodic=False):
    """ Return the 2d lattice graph of rows x columns nodes, each connected to
    its nearest 4 neighbors.  Optional argument periodic=True will connect
    boundary nodes via periodic boundary conditions.

    Parameters:

    *rows*
        The number of rows to be in the graph
    *columns*
        The number of columns to be in the graph
    *periodic*
        Prevent edge effects using periodic boundaries

    """
    return nx.grid_2d_graph(m=columns, n=rows, periodic=periodic)


def topology_smallworld(size, neighbors, edgeprob):
    assert size > 0
    assert neighbors >= 0
    assert edgeprob >= 0 and edgeprob <= 1

    return nx.newman_watts_strogatz_graph(n=size, k=neighbors, p=edgeprob)

