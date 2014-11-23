# -*- coding: utf-8 -*-

"""Functions for building different graph topologies"""

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

    assert rows > 0
    assert columns > 0
    assert radius >= 0

    graph = nx.empty_graph()
    graph.name = "Moore Lattice: {r} rows, {c} columns, "\
                 "radius={rx}".format(r=rows, c=columns, rx=radius)

    if periodic:
        graph.name += ' with periodoc boundaries'

    graph.add_nodes_from(list(range(rows * columns)))

    for node in graph.nodes_iter():
        (myrow, mycol) = divmod(node, columns)

        for row in range(myrow - radius, myrow + radius + 1):
            if periodic == False and (row < 0 or row >= rows):
                continue

            for col in range(mycol - radius, mycol + radius + 1):
                if periodic == False and (col < 0 or col >= columns):
                    continue

                neighbor = (columns * (row % rows)) + (col % columns)

                if node != neighbor:
                    graph.add_edge(node, neighbor)

    return graph


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

    assert rows > 0
    assert columns > 0

    graph = nx.grid_2d_graph(m=columns, n=rows, periodic=periodic)
    graph = nx.convert_node_labels_to_integers(graph)
    graph.name = "VonNeumann Lattice: {r} rows, {c} columns".format(r=rows,
                                                                    c=columns)

    if periodic:
        graph.name += ' with periodic boundaries'

    return graph


def smallworld(size, neighbors, edgeprob, seed=None):
    """Return a small world network with the given properties"""
    assert size > 0
    assert neighbors >= 0
    assert edgeprob >= 0 and edgeprob <= 1

    if seed:
        graph = nx.newman_watts_strogatz_graph(n=size, k=neighbors, p=edgeprob,
                                               seed=seed)

    else:
        graph = nx.newman_watts_strogatz_graph(n=size, k=neighbors, p=edgeprob)

    graph.name = 'Small World network: {s} nodes, {n} neighbors, ' \
                 '{p} edge probability'.format(s=size, n=neighbors, p=edgeprob)

    return graph


def regular(size, degree, seed=None):
    """Return a regular graph with the given properties"""
    assert size > 0
    assert degree >= 0

    if seed:
        graph = nx.random_regular_graph(d=degree, n=size, seed=seed)
    else:
        graph = nx.random_regular_graph(d=degree, n=size)

    graph.name = 'Random Regular Graph: {n} nodes, {d} degree'.format(n=size,
                                                                      d=degree)
    return graph

