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
    G.name = "Moore Lattice: {r} rows, {c} columns, radius={rx}".format(r=rows,
                                                                        c=columns,
                                                                        rx=radius)
    
    if periodic:
        G.name += ' with periodoc boundaries' 

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

    g = nx.grid_2d_graph(m=columns, n=rows, periodic=periodic)
    g = nx.convert_node_labels_to_integers(g)
    g.name = "VonNeumann Lattice: {r} rows, {c} columns".format(r=rows,
                                                                c=columns)

    if periodic:
        g.name += ' with periodic boundaries'

    return g


def smallworld(size, neighbors, edgeprob, seed=None):
    assert size > 0
    assert neighbors >= 0
    assert edgeprob >= 0 and edgeprob <= 1

    if seed:
        g = nx.newman_watts_strogatz_graph(n=size, k=neighbors, p=edgeprob,
                                           seed=seed)

    else:
        g = nx.newman_watts_strogatz_graph(n=size, k=neighbors, p=edgeprob)

    g.name = 'Small World network: {s} nodes, {n} neighbors, ' \
             '{p} edge probability'.format(s=size, n=neighbors, p=edgeprob)

    return g

def regular(size, degree, seed=None):
    assert size > 0
    assert degree >= 0

    if seed:
        g = nx.random_regular_graph(d=degree, n=size, seed=seed)
    else:
        g = nx.random_regular_graph(d=degree, n=size)

    g.name = 'Random Regular Graph: {n} nodes, {d} degree'.format(n=size,
                                                                  d=degree)
    return g
