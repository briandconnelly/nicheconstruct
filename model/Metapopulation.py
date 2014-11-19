# -*- coding: utf-8 -*-

import os

import networkx as nx
import numpy as np

import genome
from Population import Population
import topology
from DemographicsOutput import DemographicsOutput
from FitnessOutput import FitnessOutput


class Metapopulation(object):

    def __init__(self, config):
        """Initialize a Metapopulation object"""
        self.config = config
        self.time = 0

        # Build the topology, which links the subpopulations
        self.build_topology()

        # Store the probabilities of mutations between all pairs of genotypes
        self.mutation_probs = self.get_mutation_probabilities()

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

        for n, d in self.topology.nodes_iter(data=True):
            d['population'] = Population(metapopulation=self, config=config)

            if initial_state == 'corners':
                # Place all producers in one corner and all non-producers in
                # the other
                if n == 0:
                    d['population'].abundances[2**genome_length_max] = max_cap
                    d['population'].dilute()
                elif n == len(self.topology)-1:
                    d['population'].abundances[0] = min_cap
                    d['population'].dilute()

            elif initial_state == 'stress':
                cap = int(min_cap + ( (max_cap - min_cap) * initial_producer_proportion))
                num_producers = int(cap * initial_producer_proportion)
                num_nonproducers = cap - num_producers

                d['population'].abundances[0] = num_producers
                d['population'].abundances[2**genome_length_max] = num_nonproducers
                d['population'].bottleneck(survival_rate=mutation_rate_tolerance)

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
            maxfit = self.max_fitnesses()
            # TODO get the maximum fitnesses among producers and non-producers
            maxfit_p = 99
            maxfit_np = 99

            if maxfit_p > maxfit_np:
                symbol = '>'
            elif maxfit_p < maxfit_np:
                symbol = '<'
            else:
                symbol = '='

          #  res = "Metapopulation: Size {s}, {p:.1%} producers. w(P): {mp:.2} "\
          #        "{sym} w(Np): {mnp:.2}.".format(s=self.size(), p=self.prop_producers(),
          #                                       mp=maxfit_p, mnp=maxfit_np, sym=symbol)

            res = "Metapopulation: Size {s}, TODO".format(s=self.size())

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


    def get_mutation_probabilities(self):
        """Get a table of probabilities among all pairs of genotypes
        
        This works by first generating the Hamming distances between all of the
        possible genotypes. These distances are then used to calculate the
        probabilities of mutating by:

            (1-mu)^(#matching bits) * mu^(#different bits)

        Where #matching bits is the genome length - Hamming distance and
        #different bits is the Hamming distance.
        
        """

        # TODO: this should be moved to the Population level
        genome_length = self.config.getint(section='Population',
                                           option='genome_length_max')
        mutation_rate_social = self.config.getfloat(section='Population',
                                                    option='mutation_rate_social')
        mutation_rate_adaptation = self.config.getfloat(section='Population',
                                                        option='mutation_rate_adaptation')

        S = np.vstack((np.array([[0]*2**genome_length + [1]*2**genome_length]).repeat(repeats=2**genome_length, axis=0),
                       np.array([[1]*2**genome_length + [0]*2**genome_length]).repeat(repeats=2**genome_length, axis=0)))


        # TODO: to handle things like P->NP but not NP->P (or vice versa), just
        # manipulate the mr vector.

        # Get the pairwise Hamming distance for all genotypes
        hamming_v = np.vectorize(genome.hamming_distance)
        genotypes = np.arange(start=0, stop=2**(genome_length+1))
        xx, yy = np.meshgrid(genotypes, genotypes)
        hamming_distances = hamming_v(xx, yy)

        # nonsocial_hd is a matrix containing the pairwise Hamming distances
        # between all genomes considering only the non-social loci
        nonsocial_hd = hamming_distances - S

        # mr is a matrix where each element contains the probability of mutating
        # from one genome to the other.
        # mr = npower(1-m1, L-NS) * npower(m1, NS) * npower(1-m2, S2) * npower(m2, S)

        npower = np.power
        mr = npower(1-mutation_rate_adaptation, genome_length-nonsocial_hd) *\
                npower(mutation_rate_adaptation, nonsocial_hd) *\
                npower(1-mutation_rate_social, S==0) *\
                npower(mutation_rate_social, S)

        return mr

    def dilute(self):
        """Dilute the metapopulation

        Dilute the metapopulation by diluting each population by the dilution
        factor specified with the dilution_factor option in the Population
        section of the configuration file.
        """

        for n, d in self.topology.nodes_iter(data=True):
            d['population'].dilute()

    def grow(self):
        """Grow the metapopulation ...."""
        for n, d in self.topology.nodes_iter(data=True):
            d['population'].grow()

    def mutate(self):
        """Mutate the metapopulation ...."""
        for n, d in self.topology.nodes_iter(data=True):
            d['population'].mutate()

    def migrate(self, single_dest=True):
        """Migrate individuals among the populations
        
        * single_dest: if True (default), all migrants will go to a single
            neighbor population. Otherwise, migrants will be distributed among
            all neighbors. 
        
        """
        if self.migration_rate == 0:
            return

        for n, d in self.topology.nodes_iter(data=True):
            pop = d['population']

            # Migrate everything to one neighboring population
            if self.migration_dest.lower() == 'single':
                migrants = pop.select_migrants(migration_rate=self.migration_rate)
                neighbor_index = np.random.choice(self.topology.neighbors(n))
                neighbor = self.topology.node[neighbor_index]['population']
                neighbor.add_immigrants(migrants)
                pop.remove_emigrants(migrants)
            # Distribute the migrants among the neighboring populations
            elif self.migration_dest.lower() == 'neighbors':
                num_neighbors = self.topology.degree(n)
                for neighbor_node in self.topology.neighbors(n):
                    migrants = pop.select_migrants(migration_rate=self.migration_rate/num_neighbors)
                    neighbor = self.topology.node[neighbor_node]['population']
                    neighbor.add_immigrants(migrants)
                    pop.remove_emigrants(migrants)


    def census(self):
        """Update each population's abundance to account for migration"""
        for n, d in self.topology.nodes_iter(data=True):
            d['population'].census()


    def construct(self):
        """Update a population's environment when appropriate"""
        for n, d in self.topology.nodes_iter(data=True):
            d['population'].construct()


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

        # Dilute the population to allow for growth in the next cycle
        self.dilute()

        self.time += 1


    def change_environment(self):
        """Change the environment

        The change_environment function changes the environment for the
        entire metapopulation. This re-generates the fitness landscape and zeros out
        all fitness-encoding loci. This is meant to represent the metapopulation
        being subjected to different selective pressures. The number of
        individuals of each genotype that survive this event are proportional to
        the abundance of that genotype times the mutation rate (representing
        individuals that acquired the mutation that allows them to persist).
        """

        mutation_rate_tolerance = self.config.getfloat(section='Population',
                                                       option='mutation_rate_tolerance')

        for n, d in self.topology.nodes_iter(data=True):
            # TODO could these 3 steps be encapsulated in a Population-level function?
            d['population'].bottleneck(survival_rate=mutation_rate_tolerance)
            d['population'].reset_loci()
            d['population'].fitness_landscape = d['population'].build_fitness_landscape()

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
            for l in self.log_objects:
                l.update(time=self.time)

    def cleanup(self):
        for l in self.log_objects:
            l.close()

    def set_dirty(self):
        self._dirty = True

    def clear_dirty(self):
        for n, d in self.topology.nodes_iter(data=True):
            d['population'].clear_dirty()
        self._dirty = False

    def is_dirty(self):
        return self._dirty

