# -*- coding: utf-8 -*-

"""Represent metapopulations: collections of populations of individuals and the
migration between them"""

import os

import networkx as nx
import numpy as np

from DemographicsOutput import DemographicsOutput
from FitnessOutput import FitnessOutput
from Population import Population
import topology


class Metapopulation(object):
    """Define a Metapopulation object

    Metapopulations are collections of populations of individuals.

    """

    def __init__(self, config):
        """Initialize a Metapopulation object"""
        self.config = config
        self.time = 0

        # Keep some information about the population
        self._dirty = None
        self._size = None
        self._num_producers = None
        self._prop_producers = None

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
        self.population_construction = config.getboolean(section='Population',
                                                         option='enable_construction')

        for node, data in self.topology.nodes_iter(data=True):
            data['population'] = Population(metapopulation=self, config=config)

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


        # Set up data logging
        # log_objects is a list of any logging objects used by this simulation
        self.log_demographics = self.config.getboolean(section='Simulation',
                                                       option='log_demographics')
        self.log_fitness = self.config.getboolean(section='Simulation',
                                                  option='log_fitness')
        self.log_frequency = self.config.getint(section='Simulation',
                                                option='log_frequency')
        data_dir = self.config.get(section='Simulation', option='data_dir')
        assert self.log_frequency > 0

        self.log_objects = []

        if self.log_demographics:
            out_demographics = DemographicsOutput(metapopulation=self,
                                                  filename=os.path.join(data_dir, 'demographics.csv.bz2'))
            self.log_objects.append(out_demographics)

        if self.log_fitness:
            out_fitness = FitnessOutput(metapopulation=self,
                                        filename=os.path.join(data_dir, 'fitness.csv.bz2'))
            self.log_objects.append(out_fitness)


        self.set_dirty()


    def __repr__(self):
        """Return a string representation of the Metapopulation object"""
        prop_producers = self.prop_producers()

        if prop_producers == 'NA':
            res = "Metapopulation: Size {s}, NA% producers".format(s=self.size())
        else:
            res = "Metapopulation: Size {s}, {p:.1%} "\
                  "producers".format(s=self.size(), p=self.prop_producers())

        return res


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

        # Export the structure of the topology, allowing the topology to be
        # re-created. This is especially useful for randomly-generated
        # topologies.

        export_topology = self.config.getboolean(section='Simulation',
                                                 option='export_topology')

        if export_topology:
            data_dir = self.config.get(section='Simulation', option='data_dir')
            nx.write_gml(self.topology, os.path.join(data_dir, 'topology.gml'))

        self.set_dirty()


    def dilute(self):
        """Dilute the metapopulation

        Dilute the metapopulation by diluting each population by the dilution
        factor specified with the dilution_factor option in the Population
        section of the configuration file.
        """

        for node, data in self.topology.nodes_iter(data=True):
            data['population'].dilute()

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

        # Add an entry for each log file
        self.write_logfiles()

        # Grow and mutate each population
        self.grow()
        self.mutate()

        # Migrate among populations
        self.migrate()
        self.census()

        # Change the environment in populations where enabled and when that
        # population has triggered the change
        if self.population_construction:
            self.construct()

        # Could also add metapopulation-level construction events here

        # Dilute the population to allow for growth in the next cycle
        self.dilute()

        self.time += 1


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
            data['population'].fitness_landscape = data['population'].build_fitness_landscape()

        self.set_dirty()


    def size(self):
        """Return the size of the metapopulation

        The size of the metapopulation is the sum of the sizes of the
        subpopulations
        """
        if self.is_dirty():
            self._size = sum(len(d['population']) for n, d in self.topology.nodes_iter(data=True))

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
                self._prop_producers = 1.0 * self._num_producers / self._size
            except ZeroDivisionError:
                self._prop_producers = -1

        return self._prop_producers


    def max_fitnesses(self):
        """Get the maximum fitness among producers and non-producers"""

        prod_max = [d['population'].max_fitnesses()[0] for n, d in self.topology.nodes_iter(data=True)]
        nonprod_max = [d['population'].max_fitnesses()[1] for n, d in self.topology.nodes_iter(data=True)]

        return (prod_max, nonprod_max)


    def write_logfiles(self):
        """Write any log files"""

        if self.time % self.log_frequency == 0:
            for log in self.log_objects:
                log.update(time=self.time)


    def cleanup(self):
        """Perform cleanup tasks when the object is cleaned up"""
        for log in self.log_objects:
            log.close()


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

