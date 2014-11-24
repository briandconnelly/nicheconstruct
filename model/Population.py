# -*- coding: utf-8 -*-

"""Represent Populations of individuals"""

import numpy as np
from numpy import power as npow
from numpy import sum as nsum
from numpy import zeros as zeros
from numpy.random import multinomial

import genome


class Population(object):
    """Represent a population within a metapopulation

    A population is a collection of individuals. Each individual is represented
    by a number. The binary representation of that number defines that
    individual's genotype. The state of the highest order bit determines
    whether (1) or not (0) that individual is a producer.

    * genome_length_min: the minimum length of the genome. this occurs in
        environments that haven't been constructed
    * genome_length_max: the minimum length of the genome. this occurs in
        environments that have been maximally constructed
    * enable_construction: whether or not populations can alter their
        environment
    * density_threshold: the cumulative density at which an environmental
         change (construction) is triggered. See cumulative_density.
    * cumulative_density: The densities that this population has accumulated
        over time. This value is added to during each growth cycle and reset
        when an environmental change occurs.
    * mutation_rate_tolerance: the probability of an individual acquiring a
        mutation that allows it to survive a change of environment (stress)
    * mutation_rate_social: the probability of a mutation (bit flip) occuring
        at the social locus
    * mutation_rate_adaptation: the probability of a mutation (bit flip) at a
        non-social locus
    * mutate_hidden: whether or not to allow mutations at loci that are not
        exposed
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
        self.mutation_rate_social = config.getfloat(section='Population',
                                                    option='mutation_rate_social')
        self.mutation_rate_adaptation = config.getfloat(section='Population',
                                                        option='mutation_rate_adaptation')
        self.mutate_hidden = config.getboolean(section='Population',
                                               option='mutate_hidden')
        self.mutation_rate_tolerance = config.getfloat(section='Population',
                                                       option='mutation_rate_tolerance')
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
        assert self.dilution_factor >= 0 and self.dilution_factor <= 1, 'dilution_factor must be between 0 and 1'
        assert self.capacity_min >= 0
        assert self.capacity_max >= 0 and self.capacity_max >= self.capacity_min
        assert self.initialize.lower() in ['empty', 'random'], "initialize must be one of 'empty', 'random'"

        if self.enable_construction:
            assert self.density_threshold > 0
        else:
            assert self.genome_length_min == self.genome_length_max


        # Keep some information about the population
        self.environment_changed = False
        self.cumulative_density = 0
        self._dirty = True

        # Build the fitness landscape
        self.fitness_landscape = self.build_fitness_landscape()

        # Set the genome length
        self.genome_length = None
        self.genome_visible = None
        self.set_genome_length(self.genome_length_min)

        # Initialize the population (empty by default)
        self.abundances = zeros(self.fitness_landscape.size, dtype=np.int)

        if self.initialize.lower() == 'random':
            self.randomize()

        # Delta stores the differences in abundaces due to immigration and
        # emigration
        self.delta = zeros(self.abundances.size, dtype=np.int)

        # Mark this population as having been changed
        self.set_dirty()


    def __repr__(self):
        """Return a string representation of a Population object"""
        res = "Population: Size {s}, {p:.1%} producers".format(s=self.size(),
                                                               p=self.prop_producers())
        return res


    def set_genome_length(self, length):
        """Set the length of the genotypes for this population"""
        assert length >= self.genome_length_min and length <= self.genome_length_max

        self.genome_length = L = length
        Lmax = self.genome_length_max

        self.genome_visible = np.zeros(self.fitness_landscape.size,
                                       dtype=np.bool)
        self.genome_visible[:2**L] = True
        self.genome_visible[2**Lmax:2**Lmax+2**L] = True


    def empty(self):
        """Empty a population"""
        self.abundances = zeros(self.fitness_landscape.size, dtype=np.int)
        self.set_dirty()


    def randomize(self):
        """Create a random population"""
        self.abundances = np.random.random_integers(low=0,
                                                    high=self.capacity_min,
                                                    size=self.fitness_landscape.size)
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
                                            size=self.genome_length_max)
        else:
            effects = np.random.uniform(low=min_effect,
                                        high=2*avg_effect-min_effect,
                                        size=self.genome_length_max)

        effects = np.append(-1.0*production_cost, effects)

        num_genotypes = 2**(self.genome_length_max + 1)
        landscape = zeros(num_genotypes)

        for i in xrange(num_genotypes):
            genotype = genome.base10_as_bitarray(i)
            genotype = np.append(zeros(effects.size - genotype.size), genotype)
            landscape[i] = np.sum(genotype * effects) + (base_fitness + production_cost)

        self.set_dirty()
        return landscape


    def get_mutation_probabilities(self, genotype):
        """Get a vector of the mutation probabilities for a given genotype
        in the population
        """

        mu_s = self.mutation_rate_social
        mu_a = self.mutation_rate_adaptation
        Lmax = self.genome_length_max

        genotypes = np.arange(start=0, stop=self.fitness_landscape.size)
        coop_genotypes = genotypes & genotypes.size/2 == genotypes.size/2

        # Get the Hamming distances to all other genotypes at the adaptive
        # and social loci, respectively
        hdist_a = genome.hamming_distance_v(genotype & ((2**Lmax)-1),
                                            genotypes & ((2**Lmax)-1))
        hdist_s = (genome.is_producer(genotype, self.genome_length_max) != coop_genotypes) * 1.0

        probs = npow(1.0 - mu_a, self.genome_length-hdist_a) * \
                npow(mu_a, hdist_a) * \
                npow(1 - mu_s, hdist_s == 0) * \
                npow(mu_s, hdist_s)

        # If configured, disallow mutations to genomes with non-visible loci
        if not self.mutate_hidden:
            probs[self.genome_visible != True] = 0

        # We could adjust probs to allow for non-bidirectionality in social
        # mutations here

        # Normalize the probabilities
        probs = probs/probs.sum()

        return probs


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

        # Zero out the fitness effects at non-visible loci
        landscape[self.genome_visible == False] = 0

        final_size = self.capacity_min + \
                (self.capacity_max - self.capacity_min) * \
                self.prop_producers()

        grow_probs = self.abundances * (landscape/landscape.sum())

        if grow_probs.sum() > 0:
            norm_grow_probs = grow_probs/grow_probs.sum()
            self.abundances = multinomial(final_size, norm_grow_probs, 1)[0]

        # DEBUG - remove this once things have been thoroughly tested
        assert np.all(self.abundances >= 0)

        self.cumulative_density += self.abundances.sum()
        self.set_dirty()


    def mutate(self):
        """Mutate a Population

        Each genotype mutates to another with probability inversely
        proportional to the Hamming distance (# different bits in binary
        representation) between them. The distances between all pairs of
        genotypes is pre-calculated at the beginning of a run and stored in
        metapopulation.mutation_probs.

        """

        if self.abundances.sum() == 0:
            return

        mutated_population = zeros(self.abundances.size,
                                   dtype=self.abundances.dtype)

        # For each extant genotype, get the probability of mutating to each
        # other genotype, and use these probabilities to sample mutants using a
        # multinomial
        for genotype in np.where(self.abundances > 0)[0]:
            mu_probs = self.get_mutation_probabilities(genotype)
            mutated_population += multinomial(self.abundances[genotype],
                                              mu_probs, size=1)[0]

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
        self.delta = zeros(self.abundances.size, dtype=np.int)
        self.set_dirty()


    def construct(self):
        """Change the environment when appropriate

        If the cumulative density has risen above the threshold, the
        environment will be updated at this patch

        """

        if self.enable_construction and \
                self.cumulative_density > self.density_threshold and \
                self.genome_length < self.genome_length_max:

            self.set_genome_length(self.genome_length + 1)
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

        Lmax = self.genome_length_max

        num_producers = self.num_producers()
        num_nonproducers = self.num_nonproducers()

        self.abundances = zeros(self.fitness_landscape.size, dtype=np.int)
        self.abundances[0] = num_nonproducers
        self.abundances[2**Lmax] = num_producers

        self.set_dirty()


    def bottleneck(self, survival_rate):
        """ Pass the population through a bottleneck

        This function passes the population through a bottleneck. The
        probability of survival is specified as the survival_rate parameter
        [0,1].
        """

        self.abundances = np.random.binomial(self.abundances, survival_rate)
        self.set_dirty()


    def size(self):
        """Get the size of the population, which is the number of individuals
        """
        return self.abundances.sum()


    def __len__(self):
        """Get the length of the population, which is the number of
        individuals"""
        return self.abundances.sum()


    def is_empty(self):
        """Return whether or not the population is empty"""
        return self.abundances.sum() == 0


    def num_producers(self):
        """Get the number of producers"""

        L = self.genome_length
        Lmax = self.genome_length_max

        return self.abundances[2**Lmax:2**Lmax+2**L].sum()


    def num_nonproducers(self):
        """Get the number of non-producers"""
        return self.abundances[:2**self.genome_length].sum()


    def prop_producers(self):
        """Get the proportion of producers"""

        try:
            retval = 1.0 * self.num_producers() / self.size()
        except ZeroDivisionError:
            retval = -1

        return retval


    def average_fitness(self):
        """Get the average fitness in the population"""

        try:
            retval = nsum(self.abundances * self.fitness_landscape)/self.abundances.sum()
        except ZeroDivisionError:
            retval = 'NA'

        return retval


    def max_fitnesses(self):
        """Get the maximum fitness among producers and non-producers"""

        L = self.genome_length
        Lmax = self.genome_length_max

        # Get the fitnesses of genomes that are present in the population
        extant_fitnesses = (self.abundances > 0) * self.fitness_landscape

        # Return a tuple containing the maximum fitnesses among extant
        # producers and non-producers
        return (extant_fitnesses[2**Lmax:2**Lmax+2**L].max(),
                extant_fitnesses[:2**L].max())


    def set_dirty(self):
        """Mark the Population as having been changed this cycle"""
        self._dirty = True
        self.metapopulation.set_dirty()


    def clear_dirty(self):
        """Mark the Population as having not been changed this cycle"""
        self._dirty = False


    def is_dirty(self):
        """Return whether or not the Population has been changed this cycle"""
        return self._dirty

