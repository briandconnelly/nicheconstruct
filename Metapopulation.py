# -*- coding: utf-8 -*-

import os

import networkx as nx
import numpy as np

import genome
import Population
import topology


import FitnessOutput
import PopSizeOutput
import ProducerOutput

class Metapopulation(object):

    def __init__(self, config):
        """Initialize a Metapopulation object"""
        self.config = config
        self.time = 0

        self.migration_rate = self.config.getfloat(section='Metapopulation',
                                                   option='migration_rate')
        self.topology_type = self.config.get(section='Metapopulation',
                                             option='topology')


        assert self.migration_rate >= 0 and self.migration_rate <= 1
        assert self.topology_type is not None, 'Topology must be specified'
        assert self.topology_type in ['moore', 'vonneumann', 'smallworld',
                                      'complete']

        if self.topology_type.lower() == 'moore':
            width = self.config.getint(section='Metapopulation',
                                       option='width')
            height = self.config.getint(section='Metapopulation',
                                        option='height')
            periodic = self.config.getboolean(section='Metapopulation',
                                              option='periodic')
            radius = self.config.getint(section='Metapopulation',
                                        option='radius')

            assert width > 0
            assert height > 0
            assert radius > 0

            self.topology = topology.moore_lattice(rows=height, columns=width,
                                                   radius=radius,
                                                   periodic=periodic)

        elif self.topology_type.lower() == 'vonneumann':
            width = self.config.getint(section='Metapopulation',
                                       option='width')
            height = self.config.getint(section='Metapopulation',
                                        option='height')
            radius = self.config.getint(section='Metapopulation',
                                        option='radius')

            assert width > 0
            assert height > 0
            assert radius > 0

            self.topology = topology_vonneumann_latice(rows=height,
                                                       columns=width,
                                                       periodic=periodic)

        elif self.topology_type.lower() == 'smallworld':
            size = self.config.getint(section='Metapopulation',
                                      option='size')
            neighbors = self.config.getint(section='Metapopulation',
                                           option='neighbors')
            edgeprob = self.config.getint(section='Metapopulation',
                                          option='edgeprob')

            assert size > 0
            assert neighbors >= 0
            assert edgeprob >= 0 and edgeprob <= 1

            self.topology = topology_smallworld(size=size, neighbors=neighbors,
                                                edgeprob=edgeprob)

        elif self.topology_type.lower() == 'complete':
            size = self.config.getint(section='Metapopulation',
                                      option='size')

            assert size > 0

            self.topology = nx.complete_graph(n=size)


        # Store the probabilities of mutations between all pairs of genotypes
        self.mutation_probs = self.get_mutation_probabilities()

        # Create the fitness landscape
        self.fitness_landscape = self.build_fitness_landscape()

        # Create each of the populations
        for n, d in self.topology.nodes_iter(data=True):
            d['population'] = Population.Population(metapopulation=self, config=config)


        data_dir = self.config.get(section='Simulation', option='data_dir')
        self.out_popsize = PopSizeOutput.PopSizeOutput(metapopulation=self,
                                                       filename=os.path.join(data_dir,
                                                                            'popsize.csv'))
        self.out_fitness = FitnessOutput.FitnessOutput(metapopulation=self,
                                                       filename=os.path.join(data_dir,
                                                                             'fitness.csv'))
        self.out_producers = ProducerOutput.ProducerOutput(metapopulation=self,
                                                           filename=os.path.join(data_dir,
                                                                                 'producers.csv'))

    def __repr__(self):
        """Return a string representation of the Metapopulation object"""
        res = "Metapopulation: Size {s}, {p:.1%} producers".format(s=self.size(),
                                                                p=self.prop_producers())
        return res

    def build_fitness_landscape(self):
        """Build a fitness landscape

        TODO documentation
        """

        genome_length = self.config.getint(section='Population',
                                           option='genome_length')
        base_fitness = self.config.getfloat(section='Population',
                                            option='base_fitness')
        exponential = self.config.getboolean(section='Population',
                                             option='fitness_exponential')
        avg_effect = self.config.getfloat(section='Population',
                                          option='fitness_avg_effect')
        min_effect = self.config.getfloat(section='Population',
                                          option='fitness_min_effect')

        assert genome_length > 0
        assert base_fitness >= 0

        if exponential:
            effects = np.random.exponential(scale=avg_effect,
                                            size=genome_length)

        else:
            effects = np.random.uniform(low=min_effect,
                                        high=2*avg_effect-min_effect,
                                        size=genome_length)

        landscape = np.ones(2**(genome_length + 1)) * base_fitness

        # Set the social bit to 0 (no fitness effect)
        #landscape[ZZZ] = 0

        # TODO: build the landscape
        


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
            if single_dest:
                migrants = pop.select_migrants(migration_rate=self.migration_rate)
                dest_index = np.random.choice(range(len(self.topology)))
                dest = self.topology.node[self.topology.nodes()[dest_index]]['population']
                dest.add_immigrants(migrants)
                pop.remove_emigrants(migrants)
            # Distribute the migrants among the neighboring populations
            else:
                num_neighbors = self.topology.degree(n)
                for neighbor in self.topology.neighbors(n):
                    migrants = pop.select_migrants(migration_rate=self.migration_rate/num_neighbors)
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
        self.dilute()
        self.grow()
        self.mutate()

        self.out_popsize.update(time=self.time)
        self.out_fitness.update(time=self.time)
        self.out_producers.update(time=self.time)

        self.time += 1

    def size(self):
        """Return the size of the metapopulation

        The size of the metapopulation is the sum of the sizes of the
        subpopulations
        """
        return sum([d['population'].size() for n, d in self.topology.nodes_iter(data=True)])

    def __len__(self):
        return self.size()

    def num_producers(self):
        """Return the number of producers in the metapopulation"""
        return sum([d['population'].num_producers() for n, d in self.topology.nodes_iter(data=True)])

    def pop_producers(self):
        """Get the proportion of producers in the metapopulation"""
        metapopsize = self.size()

        if metapopsize == 0:
            return 0
        else:
            return 1.0 * self.num_producers() / self.size()

