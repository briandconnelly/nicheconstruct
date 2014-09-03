# -*- coding: utf-8 -*-

import os

import networkx as nx
import numpy as np

import genome
import Population
import topology
import DemographicsOutput
import GenotypesOutput
import FitnessOutput
from ChangeEnvironment import ChangeEnvironment


class Metapopulation(object):

    def __init__(self, config):
        """Initialize a Metapopulation object"""
        self.config = config
        self.time = 0

        self.migration_rate = self.config.getfloat(section='Metapopulation',
                                                   option='migration_rate')
        self.migration_dest = self.config.get(section='Metapopulation',
                                              option='migration_dest')
        self.topology_type = self.config.get(section='Metapopulation',
                                             option='topology')
        self.log_frequency = self.config.getint(section='Simulation',
                                                option='log_frequency')
        self.dilution_stochastic = self.config.getboolean(section='Population',
                                                          option='dilution_stochastic')


        assert self.migration_rate >= 0 and self.migration_rate <= 1
        assert self.migration_dest in ['single', 'neighbors']
        assert self.topology_type is not None, 'Topology must be specified'
        assert self.topology_type in ['moore', 'vonneumann', 'smallworld',
                                      'complete', 'regular']
        assert self.log_frequency > 0

        if self.topology_type.lower() == 'moore':
            width = self.config.getint(section='MooreTopology',
                                       option='width')
            height = self.config.getint(section='MooreTopology',
                                        option='height')
            periodic = self.config.getboolean(section='MooreTopology',
                                              option='periodic')
            radius = self.config.getint(section='MooreTopology',
                                        option='radius')

            assert width > 0
            assert height > 0
            assert radius > 0

            self.topology = topology.moore_lattice(rows=height, columns=width,
                                                   radius=radius,
                                                   periodic=periodic)

        elif self.topology_type.lower() == 'vonneumann':
            width = self.config.getint(section='VonNeumannTopology',
                                       option='width')
            height = self.config.getint(section='VonNeumannTopology',
                                        option='height')
            periodic = self.config.getboolean(section='VonNeumannTopology',
                                              option='periodic')

            assert width > 0
            assert height > 0

            self.topology = topology.vonneumann_lattice(rows=height,
                                                        columns=width,
                                                        periodic=periodic)

        elif self.topology_type.lower() == 'smallworld':
            size = self.config.getint(section='SmallWorldTopology',
                                      option='size')
            neighbors = self.config.getint(section='SmallWorldTopology',
                                           option='neighbors')
            edgeprob = self.config.getfloat(section='SmallWorldTopology',
                                            option='edgeprob')
            seed = self.config.getint(section='Simulation', option='seed')

            assert size > 0
            assert neighbors >= 0
            assert edgeprob >= 0 and edgeprob <= 1

            self.topology = topology.smallworld(size=size, neighbors=neighbors,
                                                edgeprob=edgeprob, seed=seed)

        elif self.topology_type.lower() == 'complete':
            size = self.config.getint(section='CompleteTopology',
                                      option='size')

            assert size > 0

            self.topology = nx.complete_graph(n=size)

        elif self.topology_type.lower() == 'regular':
            size = self.config.getint(section='RegularTopology',
                                      option='size')
            degree = self.config.getint(section='RegularTopology',
                                        option='degree')
            seed = self.config.getint(section='Simulation', option='seed')

            self.topology = topology.regular(size=size, degree=degree,
                                             seed=seed)


        export_topology = self.config.getboolean(section='Simulation',
                                                 option='export_topology')

        # Export the structure of the topology, allowing the topology to be
        # re-created. This is especially useful for randomly-generated
        # topologies.
        if export_topology:
            data_dir = self.config.get(section='Simulation', option='data_dir')
            nx.write_gml(self.topology, os.path.join(data_dir, 'topology.gml'))


        # Store the probabilities of mutations between all pairs of genotypes
        self.mutation_probs = self.get_mutation_probabilities()

        # Create the fitness landscape
        self.fitness_landscape = self.build_fitness_landscape()

        # Create each of the populations
        for n, d in self.topology.nodes_iter(data=True):
            d['population'] = Population.Population(metapopulation=self, config=config)

            if n == 0:
                # TODO: all coops
                genome_length = self.config.getint(section='Population',
                                                   option='genome_length')
                d['population'].abundances[2**genome_length] = self.config.getint('Population',
                                                                   'capacity_max')

            if n == len(self.topology)-1:
                d['population'].abundances[0] = self.config.getint('Population',
                                                                   'capacity_min')


        data_dir = self.config.get(section='Simulation', option='data_dir')
        self.log_demographics = self.config.getboolean(section='Simulation',
                                                       option='log_demographics')
        self.log_genotypes = self.config.getboolean(section='Simulation',
                                                    option='log_genotypes')
        self.log_fitness = self.config.getboolean(section='Simulation',
                                                  option='log_fitness')

        # log_objects is a list of any logging objects used by this simulation
        self.log_objects = []


        if self.log_demographics:
            out_demographics = DemographicsOutput.DemographicsOutput(metapopulation=self,
                                                       filename=os.path.join(data_dir, 'demographics.csv.bz2'))

            self.log_objects.append(out_demographics)

        if self.log_genotypes:
            out_genotypes = GenotypesOutput.GenotypesOutput(metapopulation=self,
                                                            filename=os.path.join(data_dir, 'genotypes.csv.bz2'))
            self.log_objects.append(out_genotypes)

        if self.log_fitness:
            out_fitness = FitnessOutput.FitnessOutput(metapopulation=self,
                                                      filename=os.path.join(data_dir, 'fitness.csv.bz2'))
            self.log_objects.append(out_fitness)


        self.actions = []
        self.actions.append(ChangeEnvironment(metapopulation=self))


    def __repr__(self):
        """Return a string representation of the Metapopulation object"""
        prop_producers = self.prop_producers()

        if prop_producers == 'NA':
            res = "Metapopulation: Size {s}, NA% producers".format(s=self.size())
        else:
            maxfit = self.max_fitnesses()
            maxfit_p = max(maxfit[0]) / max(self.fitness_landscape)
            maxfit_np = max(maxfit[1]) / max(self.fitness_landscape)
            #res = "Metapopulation: Size {s}, {p:.1%} producers".format(s=self.size(),
            #                                                        p=self.prop_producers())

            if maxfit_p > maxfit_np:
                symbol = '>'
            elif maxfit_p < maxfit_np:
                symbol = '<'
            else:
                symbol = '='

            res = "Metapopulation: Size {s}, {p:.1%} producers. w(P): {mp:.2} "\
                  "{sym} w(Np): {mnp:.2}.".format(s=self.size(), p=self.prop_producers(),
                                                 mp=maxfit_p, mnp=maxfit_np, sym=symbol)

        return res

    def build_fitness_landscape(self):
        """Build a fitness landscape

        TODO documentation
        """

        genome_length = self.config.getint(section='Population',
                                           option='genome_length')
        base_fitness = self.config.getfloat(section='Population',
                                            option='base_fitness')
        production_cost = self.config.getfloat(section='Population',
                                               option='production_cost')
        exponential = self.config.getboolean(section='Population',
                                             option='fitness_exponential')
        avg_effect = self.config.getfloat(section='Population',
                                          option='fitness_avg_effect')
        min_effect = self.config.getfloat(section='Population',
                                          option='fitness_min_effect')

        assert genome_length >= 0
        assert base_fitness >= 0

        if exponential:
            effects = np.random.exponential(scale=avg_effect,
                                            size=genome_length)
        else:
            effects = np.random.uniform(low=min_effect,
                                        high=2*avg_effect-min_effect,
                                        size=genome_length)

        effects = np.append(-1.0*production_cost, effects)

        landscape = np.zeros(2**(genome_length + 1))

        for i in range(2**(genome_length + 1)):
            genotype = genome.base10_as_bitarray(i)
            genotype = np.append(np.zeros(len(effects) - len(genotype)),
                                 genotype)
            landscape[i] = sum(genotype * effects) + (base_fitness + production_cost)

        return landscape


    def get_mutation_probabilities(self):
        """Get a table of probabilities among all pairs of genotypes
        
        This works by first generating the Hamming distances between all of the
        possible genotypes. These distances are then used to calculate the
        probabilities of mutating by:

            (1-mu)^(#matching bits) * mu^(#different bits)

        Where #matching bits is the genome length - Hamming distance and
        #different bits is the Hamming distance.
        
        """

        genome_length = self.config.getint(section='Population',
                                           option='genome_length')
        mutation_rate = self.config.getfloat(section='Population',
                                             option='mutation_rate')

        # Get the pairwise Hamming distance for all genotypes
        # NOTE: this doesn't differentiate between producer-nonproducer
        # mutations
        hamming_v = np.vectorize(genome.hamming_distance)
        genotypes = np.arange(start=0, stop=2**(genome_length+1))
        xx, yy = np.meshgrid(genotypes, genotypes)
        hamming_distances = hamming_v(xx, yy)

        return np.power(1-mutation_rate, genome_length+1-hamming_distances) * \
                np.power(mutation_rate, hamming_distances)


    def dilute(self, stochastic=True):
        """Dilute the metapopulation

        Dilute the metapopulation by diluting each population by the dilution
        factor specified with the dilution_factor option in the Population
        section of the configuration file.

        * stochastic: If True, the population will be diluted stochastically by
            sampling from a binomial distribution. If False, the population will
            be diluted by multiplying abundances by the dilution factor and
            taking the floor.

        """
        for n, d in self.topology.nodes_iter(data=True):
            d['population'].dilute(stochastic=stochastic)

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

    def cycle(self):
        """Cycle the metapopulation

        In each cycle, the metapopulation cycles its state by diluting each
        population, allowing each population to grow to capacity, mutate each
        population, and then migrating among populations.

        """
        self.migrate()
        self.census()
        self.dilute(stochastic=self.dilution_stochastic)
        self.grow()
        self.mutate()

        self.write_logfiles()
        self.perform_actions()

        self.time += 1

    def change_environment(self):
        """Change the environment

        The change_environment function changes the environment for the
        metapopulation. This re-generates the fitness landscape and zeros out
        all fitness-encoding loci. This is meant to represent the metapopulation
        being subjected to different selective pressures. The number of
        individuals of each genotype that survive this event are proportional to
        the abundance of that genotype times the mutation rate (representing
        individuals that acquired the mutation that allows them to persist).
        """

        self.fitness_landscape = self.build_fitness_landscape()

        mutation_rate = self.config.getfloat(section='Population',
                                             option='mutation_rate')

        for n, d in self.topology.nodes_iter(data=True):
            d['population'].bottleneck(survival_rate=mutation_rate)
            d['population'].reset_loci()

    def size(self):
        """Return the size of the metapopulation

        The size of the metapopulation is the sum of the sizes of the
        subpopulations
        """
        return sum(len(d['population']) for n, d in self.topology.nodes_iter(data=True))

    def __len__(self):
        """Return the length of a Metapopulation

        We'll define the length of a metapopulation as its size, so len(metapop)
        returns the number of individuals in all populations of Metapopulation
        metapop
        """
        return self.size()

    def num_producers(self):
        """Return the number of producers in the metapopulation"""
        return sum(d['population'].num_producers() for n, d in self.topology.nodes_iter(data=True))

    def prop_producers(self):
        """Get the proportion of producers in the metapopulation"""
        metapopsize = self.size()

        if metapopsize == 0:
            return 'NA'
        else:
            return 1.0 * self.num_producers() / self.size()


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

    def perform_actions(self):
        """Perform any actions"""

        for a in self.actions:
            a.update(time=self.time)


    def cleanup(self):
        for l in self.log_objects:
            l.close()

