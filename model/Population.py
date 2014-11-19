# -*- coding: utf-8 -*-

import numpy as np
from numpy import sum as nsum
from numpy import zeros as zeros
from numpy.random import multinomial

import genome


class Population(object):
    """Represent a population within a metapopulation

    A population is a collection of individuals. Each individual is represented
    by a number. The binary representation of that number defines that
    individual's genotype. The state of the highest order bit determines whether
    (1) or not (0) that individual is a producer.

    * genome_length_min: the minimum length of the genome. this occurs in
        environments that haven't been constructed
    * genome_length_max: the minimum length of the genome. this occurs in
        environments that have been maximally constructed
    * enable_construction: whether or not populations can alter their environment
    * density_threshold: the cumulative density at which an environmental change
        (construction) is triggered. See cumulative_density.
    * cumulative_density: The densities that this population has accumulated
        over time. This value is added to during each growth cycle and reset
        when an environmental change occurs.
    * mutation_rate_tolerance: the probability of an individual acquiring a
        mutation that allows it to survive a change of environment (stress)
    * mutation_rate_social: the probability of a mutation (bit flip) occuring at
        the social locus
    * mutation_rate_adaptation: the probability of a mutation (bit flip) at a
        non-social locus
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

        self.genome_length_min = config.getint(section='Population',
                                               option='genome_length_min')
        self.genome_length_max = config.getint(section='Population',
                                               option='genome_length_max')
        self.enable_construction = config.getboolean(section='Population',
                                                     option='enable_construction')
        self.density_threshold = config.getint(section='Population',
                                               option='density_threshold')
        self.mutation_rate_tolerance = config.getfloat(section='Population',
                                                       option='mutation_rate_tolerance')
        self.mutation_rate_social = config.getfloat(section='Population',
                                                    option='mutation_rate_social')
        self.mutation_rate_adaptation = config.getfloat(section='Population',
                                                        option='mutation_rate_adaptation')
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

        assert self.genome_length_min >= 0, 'genome_length_min must be non-negative'
        assert self.genome_length_max >= self.genome_length_min, 'genome_length_max must be at least as large as genome_length_min'
        assert self.mutation_rate_tolerance >= 0 and self.mutation_rate_tolerance <= 1
        assert self.mutation_rate_social >= 0 and self.mutation_rate_social <= 1
        assert self.mutation_rate_adaptation >= 0 and self.mutation_rate_adaptation <= 1
        assert self.dilution_factor >=0 and self.dilution_factor <= 1, 'dilution_factor must be between 0 and 1'
        assert self.capacity_min >= 0
        assert self.capacity_max >= 0 and self.capacity_max >= self.capacity_min
        assert self.initialize.lower() in ['empty', 'random'], "initialize must be one of 'empty', 'random'"

        if self.enable_construction:
            assert self.density_threshold > 0

        self.environment_changed = False
        self.cumulative_density = 0

        self.genome_length = self.genome_length_min
        # TODO: adjust the genome length based on how the population was initialized??

        # Build the fitness landscape
        self.fitness_landscape = self.build_fitness_landscape()

        # Create an empty population
        if self.initialize.lower() == 'empty':
            self.empty()
        elif self.initialize.lower() == 'random':
            self.randomize()

        # Delta stores the differences in abundaces due to immigration and emigration
        self.delta = zeros(2**(self.genome_length + 1), dtype=np.int32)

        # Mark this population as having been changed
        self.set_dirty()

    def __repr__(self):
        """Return a string representation of a Population object"""
        res = "Population: Size {s}, {p:.1%} producers".format(s=self.size(),
                                                               p=self.prop_producers())
        return res

    def empty(self):
        """Empty a population"""
        self.abundances = zeros(2**(self.genome_length_max + 1),
                                dtype=np.uint32)
        self.set_dirty()

    def randomize(self):
        """Create a random population"""
        self.abundances = np.random.random_integers(low=0,
                                                    high=self.capacity_min,
                                                    size=2**(self.genome_length_max+1))
        self.set_dirty()

    def build_fitness_landscape(self):
        """Build a fitness landscape

        The fitness landscape is based on the genome length, which represents
        the number of fitness-affecting alleles, and the configured
        distribution of fitness effects, which is sampled from to assign
        fitness effects for each locus.
        """

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

        assert base_fitness >= 0

        if exponential:
            effects = np.random.exponential(scale=avg_effect,
                                            size=self.genome_length)
        else:
            effects = np.random.uniform(low=min_effect,
                                        high=2*avg_effect-min_effect,
                                        size=self.genome_length)

        effects = np.append(-1.0*production_cost, effects)

        landscape = zeros(2**(self.genome_length + 1))

        for i in range(2**(self.genome_length + 1)):
            # TODO: is there a more efficient way to do this vector algebra without first converting to base 2?
            genotype = genome.base10_as_bitarray(i)
            genotype = np.append(zeros(len(effects) - len(genotype)), genotype)
            landscape[i] = sum(genotype * effects) + (base_fitness + production_cost)

        self.set_dirty()
        return landscape


    def get_mutation_probabilities(self, genotype):
        """Get a vector of the mutation probabilities for a given genotype
        in the population
        """
        tmp = zeros(2**(self.genome_length) + 1)
        tmp[genotype] = 1
        # TODO: if mutations not allowed in non-visible loci, make sure these are zero
        return tmp


    def dilute(self):
        """Dilute a population
        
        dilute reduces the population's size stochastically by the configured
        dilution factor (dilution_factor in Population section). This does
        not get done if the population just experienced an environmental change
        (which does a dilution of its own)
        """

        if not self.environment_changed:
            self.bottleneck(survival_rate=self.dilution_factor)


    def grow(self):
        """Grow the population to carrying capacity
        
        The final population size is determined based on the proportion of
        producers present. This population is determined by drawing from a
        multinomial with the probability of each genotype proportional to its
        abundance times its fitness.
        """

        if self.is_empty():
            return

        landscape = self.fitness_landscape

        final_size = self.capacity_min + \
                (self.capacity_max - self.capacity_min) * \
                self.prop_producers()

        grow_probs = self.abundances * (landscape/nsum(landscape))

        if nsum(grow_probs) > 0:
            norm_grow_probs = grow_probs/nsum(grow_probs)
            self.abundances = multinomial(final_size, norm_grow_probs, 1)[0]

        self.cumulative_density += nsum(self.abundances)
        self.set_dirty()


    def mutate(self):
        """Mutate a Population
        
        Each genotype mutates to another with probability inversely proportional
        to the Hamming distance (# different bits in binary representation)
        between them. The distances between all pairs of genotypes is
        pre-calculated at the beginning of a run and stored in
        metapopulation.mutation_probs.
        
        """

        mutated_population = zeros(2**(self.genome_length_max + 1),
                                   dtype=np.uint32)

        # For all of the genotypes with >0 abundance, mutate
        # should we only do this for genotypes that are visible?
        # - difficulty is that since we use a full abundances vector, there
        #   would be a gap between producers and producers
        # - handle this decision in the get_mutation_probs. if we are ignoring
        #   invisible loci completely, their abundances will be zero.
        for g in np.where(self.abundances > 0):
            mu_probs = self.get_mutation_probabilities(g)
            mutated_population += multinomial(self.abundances[g], mu_probs,
                                              size=1)[0]

        self.abundances = mutated_population
        self.set_dirty()


    def select_migrants(self, migration_rate):
        """Select individuals to migrate
                                    
        Select genotypes to migrate. The amount of each genotype that migrates
        is chosen in proportion to that genotype's abundance.
                                    
        """

        assert migration_rate >= 0 and migration_rate <= 1
        return np.random.binomial(self.abundances, migration_rate)


    def remove_emigrants(self, emigrants):
        """Remove emigrants from the population
                                    
        remove_emigrants removes the given emigrants from the population. The
        genotypes are not immediately removed to the population, but their
        counts are placed in a temporary area until census() is called.

        """
        self.delta -= emigrants
        self.set_dirty()


    def add_immigrants(self, immigrants):
        """Add immigrants to the population
                                    
        add_immigrants adds the given immigrants to the population. The new
        genotypes are not immediately added to the population, but placed in
        a temporary area until census() is called.

        """
        self.delta += immigrants
        self.set_dirty()


    def census(self):
        """Update the population's abundances after migration
        
        When migration occurs, the immigrants and emigrants are not directly
        accounted for in the list of genotype abundances. This function adds
        immigrants and removes emigrants to/from the abundances.
                                    
        """

        self.abundances += self.delta
        self.delta = zeros(2**(self.genome_length_max + 1), dtype=np.int32)
        self.set_dirty()


    def construct(self):
        """Change the environment when appropriate

        If the cumulative density has risen above the threshold, the environment
        will be updated at this patch
        """

        if self.enable_construction and \
                self.cumulative_density > self.density_threshold and \
                self.genome_length < self.genome_length_max:

            self.genome_length += 1
            self.fitness_landscape = self.build_fitness_landscape()
            self.environment_changed = True
            self.cumulative_density = 0
            self.set_dirty()
        else:
            self.environment_changed = False


    def reset_loci(self):
        """Reset the loci of the population to all zeros

        When an environment changes, the population is not yet adapted to it.
        This function captures this change by resetting all fitness-encoding
        loci to zero.
        """

        L = self.genome_length_max
        num_producers = self.abundances[2**L:].sum()
        num_nonproducers = self.abundances[:2**L].sum()

        self.abundances = zeros(2**(L + 1), dtype=np.uint32)
        self.abundances[0] = num_nonproducers
        self.abundances[2**L] = num_producers

        self.set_dirty()


    def bottleneck(self, survival_rate):
        """ Pass the population through a bottleneck

        This function passes the population through a bottleneck. The
        probability of survival is specified as the survival_rate parameter
        [0,1]. 
        """

        assert survival_rate >= 0
        assert survival_rate <= 1

        self.abundances = np.random.binomial(self.abundances, survival_rate)
        self.set_dirty()


    def size(self):
        """Get the size of the population"""
        return self.abundances.sum()

    def __len__(self):
        return self.abundances.sum()

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
        return self.abundances[producer_genomes].sum()


    def prop_producers(self):
        """Get the proportion of producers"""
        popsize = self.size()
        
        try:
            retval = 1.0 * self.num_producers() / self.size()
        except ZeroDivisionError:
            retval = -1

        return retval


    def average_fitness(self):
        """Get the average fitness in the population"""

        popsize = self.size()
        landscape = self.fitness_landscape
        # TODO: update for population-specific fitness landscapes
        # TODO: check the calculation of this

        if popsize == 0:
            return 'NA'
        else:
            return nsum(self.abundances * landscape)/popsize

    def max_fitnesses(self):
        """Get the maximum fitness among producers and non-producers"""

        popsize = self.size()
        # TODO: handle dirty

        if popsize == 0:
            return (0,0)

        # Get the fitnesses of genotypes present in the population
        # TODO: check the calculation of this
        fitnesses = np.array(self.abundances > 0, dtype=int) * self.fitness_landscape

        gl = self.genome_length
        max_producer = fitnesses[2**gl:].max()
        max_nonproducer = fitnesses[:2**gl].max()

        return (max_producer, max_nonproducer)

    def set_dirty(self):
        self._dirty = True
        self.metapopulation.set_dirty()

    def clear_dirty(self):
        self._dirty = False

    def is_dirty(self):
        return self._dirty

