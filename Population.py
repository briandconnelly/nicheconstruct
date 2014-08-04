# -*- coding: utf-8 -*-

import numpy as np

import genome


class Population(object):
    """Represent a population within a metapopulation

    A population is a collection of individuals. Each individual is represented
    by a number. The binary representation of that number defines that
    individual's genotype. The state of the highest order bit determines whether
    (1) or not (0) that individual is a producer.

    * genome_length: the length of the genome. The production allele is added to
        this, so the number of genotypes is 2^(genome_length+1)
    * mutation_rate: the probability of a single locus mutating (bit flip)
    * prod_mutation_rate: the probability of the production locus mutating
    * capacity_min: the minimum size of a fully-grown population. This occurs
        when there are no producers
    * capacity_max: the maximum size of a fully-grown population. This occurs
        when a population consists entirely of producers
    * production_cost: the fitness cost of production. This manifests itself as
        a decrease in growth rate
    * initialize: How to initialize the population
        empty: the population will have no individuals


    """

    def __init__(self, metapopulation, config):
        """Initialize a Population object"""
        self.metapopulation = metapopulation
        self.config = config

        self.genome_length = config.getint(section='Population',
                                           option='genome_length')
        self.mutation_rate = config.getfloat(section='Population',
                                             option='mutation_rate')
        self.prod_mutation_rate = config.getfloat(section='Population',
                                                   option='prod_mutation_rate')
        self.dilution_factor = config.getfloat(section='Population',
                                               option='dilution_factor')
        self.capacity_min = config.getint(section='Population',
                                          option='capacity_min')
        self.capacity_max = config.getint(section='Population',
                                          option='capacity_max')
        self.production_cost = config.getfloat(section='Population',
                                          option='production_cost')
        self.initialize = config.get(section='Population',
                                     option='initialize')

        assert self.genome_length > 0, 'genome_length must be larger than 0'
        assert self.mutation_rate >= 0 and self.mutation_rate <= 1
        assert self.prod_mutation_rate >= 0 and self.prod_mutation_rate <= 1
        assert self.dilution_factor >=0 and self.dilution_factor <= 1, 'dilution_factor must be between 0 and 1'
        assert self.capacity_min >= 0
        assert self.capacity_max >= 0 and self.capacity_max >= self.capacity_min
        assert self.initialize.lower() in ['empty', 'random'], "initialize must be one of 'empty', 'random'"

        # Create an empty population
        if self.initialize.lower() == 'empty':
            self.empty()
        elif self.initialize.lower() == 'random':
            self.randomize()

        self.delta = np.zeros(2**(self.genome_length + 1), dtype=np.uint32)

    def __repr__(self):
        """Return a string representation of a Population object"""
        res = "Population: Size {s}, {p:.1%} producers".format(s=self.size(),
                                                               p=self.prop_producers())
        return res

    def empty(self):
        """Empty a population"""
        self.abundances = np.zeros(2**(self.genome_length + 1), dtype=np.uint32)

    def randomize(self):
        """Create a random population"""
        self.abundances = np.random.random_integers(low=0,
                                                    high=self.capacity_min,
                                                    size=2**(self.genome_length+1))


    def dilute(self, stochastic=True):
        """Dilute a population
        
        dilute dilutes the population by the dilution factor, which is specified
        in the Population section of the configuration as dilution_factor. If
        the stochastic parameter is True (default), dilution will be done
        randomly. Otherwise, the abundances of each genotype will be multiplied
        by the dilution factor and rounded down.

        """
        if self.is_empty():
            return

        if stochastic:
            self.abundances = np.random.binomial(self.abundances,
                                                 self.dilution_factor)
        else:
            self.abundances = np.floor(self.abundances * self.dilution_factor).astype(np.uint32)


    def grow(self):
        """Grow the population to carrying capacity
        
        The final population size is determined based on the proportion of
        producers present. This population is determined by drawing from a
        multinomial with the probability of each genotype proportional to its
        abundance times its fitness.
        """

        if self.is_empty():
            return

        landscape = self.metapopulation.fitness_landscape

        final_size = self.capacity_min + \
                (self.capacity_max - self.capacity_min) * \
                self.prop_producers()

        grow_probs = self.abundances * landscape

        if sum(grow_probs) > 0:
            norm_grow_probs = grow_probs/sum(grow_probs)
            self.abundances = np.random.multinomial(final_size, norm_grow_probs,
                                                    1)[0]


    def mutate(self):
        """Mutate a Population
        
        Each genotype mutates to another with probability inversely proportional
        to the Hamming distance (# different bits in binary representation)
        between them. The distances between all pairs of genotypes is
        pre-calculated at the beginning of a run and stored in
        metapopulation.mutation_probs.
        
        """

        if self.is_empty():
            return

        mutated_population = np.zeros(2**(self.genome_length + 1), dtype=np.uint32)

        multinomial = np.random.multinomial

        for i in range(len(self.abundances)):
            mutated_population += multinomial(self.abundances[i],
                                              self.metapopulation.mutation_probs[i],
                                              size=1)[0]

        self.abundances = mutated_population


    def select_migrants(self, migration_rate):
        """Select individuals to migrate
                                    
        Select genotypes to migrate. The amount of each genotype that migrates
        is chosen in proportion to that genotype's abundance.
                                    
        """

        assert migration_rate >= 0 and migration_rate <= 1

        migrants = np.random.binomial(self.abundances, migration_rate)

        return migrants

    def remove_emigrants(self, emigrants):
        """Remove emigrants from the population
                                    
        remove_emigrants removes the given emigrants from the population. The
        genotypes are not immediately removed to the population, but their
        counts are placed in a temporary area until census() is called.

        """
        self.delta -= emigrants

    def add_immigrants(self, immigrants):
        """Add immigrants to the population
                                    
        add_immigrants adds the given immigrants to the population. The new
        genotypes are not immediately added to the population, but placed in
        a temporary area until census() is called.

        """
        self.delta += immigrants

    def census(self):
        """Update the population's abundances after migration
        
        When migration occurs, the immigrants and emigrants are not directly
        accounted for in the list of genotype abundances. This function adds
        immigrants and removes emigrants to/from the abundances.
                                    
        """

        self.abundances += self.delta
        self.delta = np.zeros(2**(self.genome_length + 1), dtype=np.uint32)

    def size(self):
        """Get the size of the population"""
        return np.sum(self.abundances)

    def __len__(self):
        return np.sum(self.abundances)

    def is_empty(self):
        """Return whether or not the population is empty"""
        return self.size() == 0

    def num_producers(self):
        """Get the number of producers"""

        # How this works:
        # 1. generate all indices whose producer bit is set
        #    - this is all numbers from 2^nbits through 2^(nbits+1)-1
        # 2. get the abundances at those indices
        # 3. sum them up

        gl = self.genome_length
        producer_genomes = np.arange(start=2**gl, stop=2**(gl+1))
        return np.sum(self.abundances[producer_genomes])


    def prop_producers(self):
        """Get the proportion of producers"""
        popsize = self.size()
        
        if popsize == 0:
            return 'NA'
        else:
            return 1.0 * self.num_producers() / popsize

    def average_fitness(self):
        """Get the average fitness in the population"""

        popsize = self.size()
        landscape = self.metapopulation.fitness_landscape

        if popsize == 0:
            return 'NA'
        else:
            return sum(self.abundances * landscape)/popsize

