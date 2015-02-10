# -*- coding: utf-8 -*-

"""Functions for working with Metapopulations"""

import numpy as np
from numpy import bitwise_xor, where
from numpy.random import binomial, multinomial, random_integers
import pandas as pd

from Population import assign_fitness
from misc import stress_colnames
from Topology import random_neighbor


def create_metapopulation(config, topology):
    """Create a metapopulation"""
    size = len(topology)
    assert size > 0

    capacity_min = config['Population']['capacity_min']
    capacity_max = config['Population']['capacity_max']
    assert capacity_min <= capacity_max

    initial_cooperator_proportion = config['Population']['initial_cooperator_proportion']

    genome_length_min = config['Population']['genome_length_min']
    genome_length_max = config['Population']['genome_length_max']
    assert genome_length_min <= genome_length_max

    initial_popsize = capacity_min + \
                  (initial_cooperator_proportion * (capacity_max - capacity_min))

    stress_columns = stress_colnames(L=genome_length_max)
    data = {'Time': 0,
            'Population': np.repeat(np.arange(size), initial_popsize).tolist(),
            'Coop': (binomial(1, initial_cooperator_proportion, size * initial_popsize) == 1).tolist(),
            'Fitness': 0}
    data.update({sc: np.zeros(size * initial_popsize, dtype=np.int).tolist() for sc in stress_columns})
    M = pd.DataFrame(data,
                     columns=['Time', 'Population', 'Coop'] + ["S{0:02d}".format(i) for i in np.arange(1,genome_length_max+1)] + ['Fitness'])

    M = assign_fitness(P=M, genome_length=genome_length_min,
                       num_stress_alleles=config['Population']['stress_alleles'],
                       base_fitness=config['Population']['base_fitness'],
                       cost_cooperation=config['Population']['cost_cooperation'],
                       benefit_nonzero=config['Population']['benefit_nonzero'],
                       benefit_ordered=config['Population']['benefit_ordered'])
    return M


def reset_stress_loci(M, Lmax):
    """Reset all stress loci in the population
    
    Resetting a stress locus sets its allelic state to 0.
    """

    M[stress_colnames(L=Lmax)] = 0
    return M


def mix(M, topology):
    """Mix the metapopulation

    Mixing creates the individuals in a metapopulation to be re-distributed
    evenly among the populations
    """

    M.Population = random_integers(low=0, high=len(topology)-1,
                                   size=M.shape[0])
    return M


def migrate(M, topology, rate):
    """Migrate individuals among subpopulations"""
    assert 0 <= rate <= 1

    emigrants_ix = M.index[where(binomial(n=1, p=rate,
                                          size=M.index.shape[0]) == 1)]

    if emigrants_ix.shape[0] > 0:
        targets = {p: random_neighbor(p, topology) for p in M.Population.unique()}
        get_target = np.vectorize(lambda t: targets[t])
        M.loc[emigrants_ix, 'Population'] = get_target(M.loc[emigrants_ix, 'Population'].values)

    return M


def mutate(M, mu_stress, mu_cooperation, Lmax, num_stress_alleles):
    """Mutate individuals in the metapopulation"""
    assert 0 <= mu_stress <= 1
    assert 0 <= mu_cooperation <= 1
    assert Lmax >= 0
    assert num_stress_alleles >= 0

    Mcopy = M.copy(deep=True)

    # Cooperation mutations - flip the cooperation bit 0->1 or 1->0
    Mcopy.Coop = bitwise_xor(Mcopy.Coop, binomial(n=1, p=mu_cooperation,
                                                  size=Mcopy.Coop.shape))==1

    # Mutations at stress loci
    # Alleles to mutate are chosen from a binomial distrubution, and these
    # alleles are modified by adding a random amount
    if Lmax > 0:
        s = stress_colnames(L=Lmax)
        if num_stress_alleles == 1:
            Mcopy[s] = bitwise_xor(Mcopy[s], binomial(n=1, p=mu_stress,
                                                      size=Mcopy[s].shape))
        else:
            # Small problem, an allele could mutate to itself.
            Mcopy[s] = (Mcopy[s] + (binomial(n=1, p=mu_stress, size=Mcopy[s].shape) * random_integers(low=1, high=num_stress_alleles, size=Mcopy[s].shape))) % (num_stress_alleles + 1)

    return Mcopy


def grow(M, genome_lengths, config):
    """Grow the population"""

    smin = config['Population']['capacity_min']
    smax = config['Population']['capacity_max']
    assert smin <= smax

    num_stress_alleles = config['Population']['stress_alleles']
    assert num_stress_alleles >= 0

    genome_length_max = config['Population']['genome_length_max']
    mu_stress = config['Population']['mutation_rate_stress']
    mu_cooperation = config['Population']['mutation_rate_cooperation']

    stress_columns = stress_colnames(L=genome_length_max)

    offspring_ix = np.array([], dtype=np.int)

    # Get a list of parent individual indices
    for popid, subpop in M.groupby('Population'):
        # Get the number of offspring to produce (carrying capacity - current)
        num_offspring = smin + round(subpop.Coop.mean() * (smax - smin)) - len(subpop)

        # Select the number of offspring to produce for each parent
        parent_num_offspring = multinomial(n=num_offspring,
                                           pvals=subpop.Fitness/subpop.Fitness.sum())

        # Get a list of the global index values for each parent
        parent_ix = subpop.iloc[np.repeat(np.arange(len(parent_num_offspring)),
                                          parent_num_offspring)].index.values

        offspring_ix = np.append(offspring_ix, parent_ix)


    # Mutate the offspring
    mu_offspring = mutate(M=M.loc[offspring_ix],
                          mu_stress=mu_stress,
                          mu_cooperation=mu_cooperation,
                          Lmax=genome_length_max,
                          num_stress_alleles=num_stress_alleles)

    mu_offspring = assign_fitness(P=mu_offspring, genome_length=genome_length_max,
                                  num_stress_alleles=config['Population']['stress_alleles'],
                                  base_fitness=config['Population']['base_fitness'],
                                  cost_cooperation=config['Population']['cost_cooperation'],
                                  benefit_nonzero=config['Population']['benefit_nonzero'],
                                  benefit_ordered=config['Population']['benefit_ordered'])

    # Merge in the offspring
    M = M.append(mu_offspring)

    # Reindex the metapopulation
    M.index = np.arange(len(M))

    return M

