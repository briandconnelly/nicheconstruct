# -*- coding: utf-8 -*-

"""Represent metapopulations: collections of populations of individuals and the
migration between them"""

import os

import networkx as nx
import numpy as np

from Population import Population
from genome import num_ones_v
import topology


class Metapopulation(object):
    """Define a Metapopulation object

    Metapopulations are collections of populations of individuals.

    """

    def __init__(self, simulation):
        """Initialize a Metapopulation object"""
        self.simulation = simulation
        self.config = self.simulation.config

        # Keep some information about the population
        self._dirty = None
        self._size = None
        self._num_producers = None
        self._prop_producers = None
        self._prev_prop_producers = None

        if self.simulation.env_change == 'Metapopulation':
            self.enable_construction = True
            self.density_threshold = self.config.getint(section='Metapopulation',
                                                        option='density_threshold')
            assert self.density_threshold > 0
        else:
            self.enable_construction = False

        self.cumulative_density = 0
        self.environment_changed = False

        # Build the topology, which links the subpopulations
        self.topology = None

        self.build_topology()

        # Create each of the populations
        initial_state = self.config.get(section='Metapopulation',
                                        option='initial_state')
        genome_length_max = self.config.getint(section='Population',
                                               option='genome_length_max')
        max_cap = self.config.getint(section='Population', option='capacity_max')
        min_cap = self.config.getint(section='Population', option='capacity_min')
        initial_producer_proportion = self.config.getfloat(section='Population',
                                                           option='initial_producer_proportion')
        mutation_rate_tolerance = self.config.getfloat(section='Population',
                                                       option='mutation_rate_tolerance')

        self.genotype_num_ones = num_ones_v(np.arange(2**(genome_length_max+1), dtype=int))

        for node, data in self.topology.nodes_iter(data=True):
            data['population'] = Population(simulation=self.simulation,
                                            metapopulation=self)

            if initial_state == 'corners':
                # Place all producers in one corner and all non-producers in
                # the other
                if node == 0:
                    data['population'].abundances[2**genome_length_max] = max_cap
                    data['population'].dilute()
                elif node == len(self.topology)-1:
                    data['population'].abundances[0] = min_cap
                    data['population'].dilute()

            elif initial_state == 'stress':
                cap = int(min_cap + ((max_cap - min_cap) * \
                                     initial_producer_proportion))
                num_producers = int(cap * initial_producer_proportion)
                num_nonproducers = cap - num_producers

                data['population'].abundances[0] = num_producers
                data['population'].abundances[2**genome_length_max] = num_nonproducers
                data['population'].bottleneck(survival_rate=mutation_rate_tolerance)

        # Get the settings for migration among populations
        self.migration_rate = self.config.getfloat(section='Metapopulation',
                                                   option='migration_rate')
        self.migration_dest = self.config.get(section='Metapopulation',
                                              option='migration_dest')
        assert self.migration_rate >= 0 and self.migration_rate <= 1
        assert self.migration_dest in ['single', 'neighbors']

        self.set_dirty()


    def __str__(self):
        """Return a string representation of the Metapopulation object"""
        prop_producers = self.prop_producers()

        if prop_producers == 'NA':
            res = "Metapopulation: Size {s}".format(s=self.size())
        else:
            (pfr, nfr) = self.max_fitnesses()
            pf = max(pfr)
            nf = max(nfr)

            if pf > nf:
                comp = ">"
            elif pf < nf:
                comp = "<"
            else:
                comp = "="

            res = "Metapopulation: Size {s}, {pp:.1%} producers, " \
                    "w(P) {c} w(N)".format(s=self.size(),
                                           pp=self.prop_producers(), c=comp)

        return res


    def __getitem__(self, key):
        """Get a specific population from the metapopulation
        """
        return self.topology.node[key]['population']


    def build_topology(self):
        """Build the topology (a graph) for the metapopulation"""
        topology_type = self.config.get(section='Metapopulation',
                                        option='topology')

        assert topology_type is not None, 'Topology must be specified'
        assert topology_type in ['moore', 'vonneumann', 'smallworld',
                                 'complete', 'regular']

        if topology_type.lower() == 'moore':
            width = self.config.getint(section='MooreTopology',
                                       option='width')
            height = self.config.getint(section='MooreTopology',
                                        option='height')
            periodic = self.config.getboolean(section='MooreTopology',
                                              option='periodic')
            radius = self.config.getint(section='MooreTopology',
                                        option='radius')

            self.topology = topology.moore_lattice(rows=height, columns=width,
                                                   radius=radius,
                                                   periodic=periodic)

        elif topology_type.lower() == 'vonneumann':
            width = self.config.getint(section='VonNeumannTopology',
                                       option='width')
            height = self.config.getint(section='VonNeumannTopology',
                                        option='height')
            periodic = self.config.getboolean(section='VonNeumannTopology',
                                              option='periodic')

            self.topology = topology.vonneumann_lattice(rows=height,
                                                        columns=width,
                                                        periodic=periodic)

        elif topology_type.lower() == 'smallworld':
            size = self.config.getint(section='SmallWorldTopology',
                                      option='size')
            neighbors = self.config.getint(section='SmallWorldTopology',
                                           option='neighbors')
            edgeprob = self.config.getfloat(section='SmallWorldTopology',
                                            option='edgeprob')
            seed = self.config.getint(section='Simulation', option='seed')

            self.topology = topology.smallworld(size=size, neighbors=neighbors,
                                                edgeprob=edgeprob, seed=seed)

        elif topology_type.lower() == 'complete':
            size = self.config.getint(section='CompleteTopology',
                                      option='size')

            self.topology = nx.complete_graph(n=size)

        elif topology_type.lower() == 'regular':
            size = self.config.getint(section='RegularTopology',
                                      option='size')
            degree = self.config.getint(section='RegularTopology',
                                        option='degree')
            seed = self.config.getint(section='Simulation', option='seed')

            self.topology = topology.regular(size=size, degree=degree,
                                             seed=seed)


        # How frequently should the metapopulation be mixed?
        self.mix_frequency = self.config.getint(section='Metapopulation',
                                                option='mix_frequency')
        assert self.mix_frequency >= 0


        # Export the structure of the topology, allowing the topology to be
        # re-created. This is especially useful for randomly-generated
        # topologies.

        export_topology = self.config.getboolean(section='Simulation',
                                                 option='export_topology')

        if export_topology:
            data_dir = self.config.get(section='Simulation', option='data_dir')
            nx.write_gml(self.topology, os.path.join(data_dir, 'topology.gml'))

        self.set_dirty()


    def populations_iter(self):
        """Return an iterator containing all of the Populations in the
        metapopulation
        """
        for node, data in self.topology.nodes_iter(data=True):
            yield data['population']


    def dilute(self):
        """Dilute the metapopulation

        Dilute the metapopulation by diluting each population by the dilution
        factor specified with the dilution_factor option in the Population
        section of the configuration file.
        """

        for node, data in self.topology.nodes_iter(data=True):
            data['population'].dilute()


    def mix(self):
        """Mix the population

        Mix the population. The abundances at all populations are combined and
        re-distributed.
        """

        genome_length_max = self.config.getint(section='Population',
                                               option='genome_length_max')
        abundances = np.zeros(2**(genome_length_max+1), dtype=np.int)

        for n, d in self.topology.nodes_iter(data=True):
            abundances += d['population'].abundances

        for n, d in self.topology.nodes_iter(data=True):
            d['population'].abundances = np.random.binomial(abundances, 1.0/len(self.topology))


    def grow(self):
        """Grow the metapopulation ...."""
        for node, data in self.topology.nodes_iter(data=True):
            data['population'].grow()


    def mutate(self):
        """Mutate the metapopulation ...."""
        for node, data in self.topology.nodes_iter(data=True):
            data['population'].mutate()


    def migrate(self):
        """Migrate individuals among the populations"""
        if self.migration_rate == 0:
            return

        for node, data in self.topology.nodes_iter(data=True):
            pop = data['population']

            # Migrate everything to one neighboring population
            if self.migration_dest.lower() == 'single':
                migrants = pop.select_migrants(migration_rate=self.migration_rate)
                neighbor_index = np.random.choice(self.topology.neighbors(node))
                neighbor = self.topology.node[neighbor_index]['population']
                neighbor.add_immigrants(migrants)
                pop.remove_emigrants(migrants)
            # Distribute the migrants among the neighboring populations
            elif self.migration_dest.lower() == 'neighbors':
                num_neighbors = self.topology.degree(node)
                for neighbor_node in self.topology.neighbors_iter(node):
                    migrants = pop.select_migrants(migration_rate=self.migration_rate/num_neighbors)
                    neighbor = self.topology.node[neighbor_node]['population']
                    neighbor.add_immigrants(migrants)
                    pop.remove_emigrants(migrants)


    def census(self):
        """Update each population's abundance to account for migration"""
        for node, data in self.topology.nodes_iter(data=True):
            data['population'].census()


    def construct(self):
        """Update a population's environment when appropriate"""
        for node, data in self.topology.nodes_iter(data=True):
            data['population'].construct()


    def cycle(self):
        """Cycle the metapopulation

        In each cycle, the metapopulation cycles its state by diluting each
        population, allowing each population to grow to capacity, mutate each
        population, and then migrating among populations.

        """

        # Update some metrics based on the current state of the metapopulation
        ignore = self.size()
        ignore = self.num_producers()
        ignore = self.prop_producers()
        # TODO: handle fitnesses, etc
        self.clear_dirty()

        # Grow and mutate each population
        self.grow()
        self.mutate()

        # Migrate among populations
        self.migrate()
        self.census()

        # Mix the populations
        time = self.simulation.cycle
        if self.mix_frequency > 0 and time > 0 and \
                (time % self.mix_frequency == 0):
            self.mix()

        # Handle environmental change
        self.environment_changed = False
        self.cumulative_density += self.size()

        if self.simulation.env_change == 'Population':
            self.construct()

        elif self.simulation.env_change == 'Metapopulation' and \
                self.cumulative_density > self.density_threshold:
            self.change_environment()
            self.environment_changed = True
            self.cumulative_density = 0

        # Dilute the population to allow for growth in the next cycle
        if not self.environment_changed:
            self.dilute()


    def change_environment(self):
        """Change the environment

        The change_environment function changes the environment for the entire
        metapopulation. This re-generates the fitness landscape and zeros out
        all fitness-encoding loci. This is meant to represent the
        metapopulation being subjected to different selective pressures. The
        number of individuals of each genotype that survive this event are
        proportional to the abundance of that genotype times the mutation rate
        (representing individuals that acquired the mutation that allows them
        to persist).

        """

        mutation_rate_tolerance = self.config.getfloat(section='Population',
                                                       option='mutation_rate_tolerance')

        for node, data in self.topology.nodes_iter(data=True):
            # TODO could these 3 steps be encapsulated in a Population-level function?
            data['population'].bottleneck(survival_rate=mutation_rate_tolerance)
            data['population'].reset_loci()
            data['population'].build_fitness_landscape()

        self.set_dirty()


    def size(self):
        """Return the size of the metapopulation

        The size of the metapopulation is the sum of the sizes of the
        subpopulations
        """
        if self.is_dirty():
            self._size = sum(d['population'].size() for n, d in self.topology.nodes_iter(data=True))

        return self._size


    def __len__(self):
        """Return the length of a Metapopulation

        We'll define the length of a metapopulation as its size, so len(metapop)
        returns the number of individuals in all populations of Metapopulation
        metapop
        """
        return self.size()


    def num_producers(self):
        """Return the number of producers in the metapopulation"""
        if self.is_dirty():
            self._num_producers = sum(d['population'].num_producers() for n, d in self.topology.nodes_iter(data=True))

        return self._num_producers


    def prop_producers(self):
        """Get the proportion of producers in the metapopulation"""
        if self.is_dirty():
            try:
                # TODO: this may use dirty values for num_producers and size
                self._prev_prop_producers = self._prop_producers
                self._prop_producers = 1.0 * self.num_producers() / self.size()
            except ZeroDivisionError:
                self._prop_producers = 'NA'

        return self._prop_producers


    def max_fitnesses(self):
        """Get the maximum fitness among producers and non-producers"""

        prod_max = [d['population'].max_fitnesses()[0] for n, d in self.topology.nodes_iter(data=True)]
        nonprod_max = [d['population'].max_fitnesses()[1] for n, d in self.topology.nodes_iter(data=True)]

        return (prod_max, nonprod_max)


    def max_ones(self):
        """Get the maximum number of ones in the visible portion of producer
        and non-producer genotypes (tuple). This indicates how adapted each
        type is to the environment.
        """
        prod_max = [d['population'].max_ones()[0] for n, d in self.topology.nodes_iter(data=True)]
        nonprod_max = [d['population'].max_ones()[1] for n, d in self.topology.nodes_iter(data=True)]

        return (prod_max, nonprod_max)


    def set_dirty(self):
        """Mark the metapopulation as changed in the current cycle"""
        self._dirty = True


    def clear_dirty(self):
        """Mark the metapopulation as unchanged in the current cycle"""
        for node, data in self.topology.nodes_iter(data=True):
            data['population'].clear_dirty()
        self._dirty = False


    def is_dirty(self):
        """Return whether or not the Metapopulation has been changed"""
        return self._dirty

