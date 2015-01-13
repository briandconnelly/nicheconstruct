# -*- coding: utf-8 -*-

"""Functions for working with Metapopulation topologies"""

import os

import networkx as nx


def build_topology(config):
    """Create a metapopulation topology

    The specific topology is defined in Metapopulation:Topology
    """
    top_type = config['Metapopulation']['Topology']
    assert top_type.lower() in ['moore', 'vonneumann', 'smallworld',
                                'complete', 'regular']

    if top_type.lower() == 'moore':
        return build_topology_moore(config)
    elif top_type.lower() == 'vonneumann':
        return build_topology_vonneumann(config)
    elif top_type.lower() == 'smallworld':
        return build_topology_smallworld(config)
    elif top_type.lower() == 'complete':
        return build_topology_complete(config)
    elif top_type.lower() == 'regular':
        return build_topology_regular(config)


def build_topology_moore(config):
    """Build a lattice graph with Moore neighborhood"""
    columns = int(config['MooreTopology']['width'])
    rows = int(config['MooreTopology']['height'])
    periodic = config['MooreTopology'].getboolean('periodic')
    radius = int(config['MooreTopology']['radius'])
    assert rows > 0 and columns > 0 and radius > 0

    top = nx.empty_graph()
    top.name = "Moore Lattice: {r} rows, {c} columns, radius={rx}".format(r=rows,
                                                                          c=columns,
                                                                          rx=radius)
    if periodic:
        top.name += ' with periodoc boundaries'

    top.add_nodes_from(list(range(rows * columns)))

    for node in top.nodes_iter():
        (myrow, mycol) = divmod(node, columns)

        for r in range(myrow - radius, myrow + radius + 1):
            if periodic == False and (r < 0 or r >= rows):
                continue

            for c in range(mycol - radius, mycol + radius + 1):
                if periodic == False and (c < 0 or c >= columns):
                    continue

                neighbor = (columns * (r % rows)) + (c % columns)

                if node != neighbor:
                    top.add_edge(node, neighbor)

    return top


def build_topology_vonneumann(config):
    """Build a lattice graph with Von Neumann neighborhood"""

    width = int(config['VonNeumannTopology']['width'])
    height = int(config['VonNeumannTopology']['height'])
    periodic = config['VonNeumannTopology'].getboolean('periodic')
    assert width > 0 and height > 0

    graph = nx.grid_2d_graph(m=width, n=height, periodic=periodic)
    graph = nx.convert_node_labels_to_integers(graph)
    graph.name = "VonNeumann Lattice: {r} rows, {c} columns".format(r=height,
                                                                    c=width)

    if periodic:
        graph.name += ' with periodic boundaries'

    return graph


def build_topology_smallworld(config):
    """Build a small world network"""

    size = int(config['SmallWorldTopology']['size'])
    neighbors = int(config['VonNeumannTopology']['neighbors'])
    edgeprob = float(config['VonNeumannTopology']['edgeprob'])
    seed = int(config['Simulation']['seed'])

    assert size > 0
    assert neighbors >= 0
    assert 0 <= edgeprob <= 1

    top = nx.newman_watts_strogatz_graph(n=size, k=neighbors, p=edgeprob,
                                         seed=seed)
    top.name = 'Small World network: {s} nodes, {n} neighbors, ' \
               '{p} edge probability'.format(s=size, n=neighbors, p=edgeprob)

    return top


def build_topology_complete(config):
    """Build a complete graph"""

    size = int(config['CompleteTopology']['size'])
    assert size > 0

    return nx.complete_graph(n=size)


def build_topology_regular(config):
    """Build a N-regular graph"""

    size = int(config['RegularTopology']['size'])
    degree = int(config['RegularTopology']['degree'])
    seed = int(config['Simulation']['seed'])

    assert size > 0
    assert degree >= 0

    top = nx.random_regular_graph(d=degree, n=size, seed=seed)
    top.name = 'Random Regular Graph: {n} nodes, {d} degree'.format(n=size,
                                                                    d=degree)
    return top


def export_topology(topology, filename='topology.gml'):
    """Write the topology to a file in Graph Modelling Language (GML) format
    
    Filenames ending in .bz2 or .gz will be compressed
    """

    nx.write_gml(topology, filename)


def nodes(topology):
    """Get the nodes in the topology
    
    This function returns a list containing all nodes in the topology. When
    iterating through all nodes in the list, nodes_iter is preferable.
    """
    return topology.nodes()


def nodes_iter(topology):
    """Get an iterator for all nodes in the topology"""
    return topology.nodes_iter()


def neighbors_iter(topology, n):
    """Get an iterator for all of a node's neighbors"""
    return topology[n]


def neighbors(topology, n):
    """Get a list of a node's neighbors
    
    For iterating through a node's neighbors, neighbors_iter is preferable.
    """
    return [n for n in topology[n]]

