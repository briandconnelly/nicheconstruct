# -*- coding: utf-8 -*-

"""Functions for working with Metapopulations"""

import numpy as np
from numpy import bitwise_xor, where
from numpy.random import binomial
import pandas as pd

from Topology import random_neighbor
from misc import stress_loci


def create_metapopulation(config, topology):
    """Create a metapopulation"""
    size = len(topology)
    assert size > 0

    capacity_min = int(config['Population']['capacity_min'])
    capacity_max = int(config['Population']['capacity_max'])
    assert 0 <= capacity_min <= capacity_max

    initial_cooperator_proportion = float(config['Population']['initial_cooperator_proportion'])
    assert 0 <= initial_cooperator_proportion <= 1

    genome_length_min = int(config['Population']['genome_length_min'])
    genome_length_max = int(config['Population']['genome_length_max'])
    assert 0 <= genome_length_min <= genome_length_max

    initial_popsize = capacity_min + \
                  (initial_cooperator_proportion * (capacity_max - capacity_min))

    stress_columns = stress_loci(Lmax=genome_length_max)
    data = {'Time': 0,
            'Population': np.repeat(np.arange(size), initial_popsize).tolist(),
            'Coop': np.random.binomial(1, initial_cooperator_proportion, size * initial_popsize).tolist(),
            'Fitness': 0}
    data.update({sc: np.zeros(size * initial_popsize, dtype=np.int).tolist() for sc in stress_columns})
    return pd.DataFrame(data,
                        columns=['Time', 'Population', 'Coop'] + ["S{0:02d}".format(i) for i in np.arange(1,genome_length_max+1)] + ['Fitness'])

def reset_stress_loci(M, Lmax):
    """Reset all stress loci in the population
    
    Resetting a stress locus sets its allelic state to 0.
    """

    Mcopy = M.copy(deep=True)
    Mcopy[stress_loci(Lmax)] = 0
    return Mcopy


def mix(M, topology):
    """Mix the metapopulation

    Mixing creates the individuals in a metapopulation to be re-distributed
    evenly among the populations
    """

    Mcopy = M.copy(deep=True)
    Mcopy.Population = np.random.random_integers(low=0, high=len(topology)-1,
                                                 size=Mcopy.shape[0])
    return Mcopy


def migrate(M, topology, rate):
    """Migrate individuals among subpopulations"""
    assert 0 <= rate <= 1

    Mcopy = M.copy(deep=True)

    emigrants_ix = Mcopy.index[where(binomial(n=1, p=rate,
                                              size=Mcopy.index.shape[0]) == 1)]

    if emigrants_ix.shape[0] > 0:
        targets = {p: random_neighbor(p, topology) for p in M.Population.unique()}
        get_target = np.vectorize(lambda t: targets[t])
        Mcopy.loc[emigrants_ix, 'Population'] = get_target(Mcopy.loc[emigrants_ix, 'Population'].values)

    return Mcopy


def grow(M, genome_lengths, config):
    """Grow the population"""

    Mcopy = M.copy(deep=True)

    base_fitness = float(config['Population']['base_fitness'])
    cost_cooperation = float(config['Population']['cost_cooperation'])
    delta = float(config['Population']['benefit_nonzero'])
    gamma = float(config['Population']['benefit_ordered'])

    smin = float(config['Population']['capacity_min'])
    smax = float(config['Population']['capacity_max'])

    stress_alleles = int(config['Population']['stress_alleles'])

    # Add:
    #Mcopy[Mcopy.index.max() + 1] = [NEW_ROW]

    stress_columns = stress_loci(Lmax=int(config['Population']['genome_length_max']))

    for pop in M.Population.unique():
        subpop = M[M.Population==pop]
        visible = subpop[stress_columns[:genome_lengths[pop]]]
        pop_N = np.apply_along_axis(lambda x: np.bincount(x, minlength=stress_alleles+1), axis=0, arr=visible)

        # Calculate the fitness of each individual
        # TODO: get gamma fitness
        fitness = base_fitness + \
                (np.sum(visible > 0, axis=1) * delta) - \
                (subpop.Coop * cost_cooperation)

        # TODO: assign fitness back in Mcopy

        pct_cooperators = subpop.Coop.mean()
        num_offspring = int(smin + (pct_cooperators * (smax - smin)) - subpop.shape[0])
        parent_num_offspring = np.random.multinomial(n=num_offspring,
                                                     pvals=fitness/fitness.sum())

        # parent_num_offspring is an array where each element represents a
        # parent (relative index), and the value contains the number of
        # offspring
        offspring = subpop.iloc[np.repeat(np.arange(parent_num_offspring.shape[0]), parent_num_offspring)]

        # Mutate the offspring
        mu_offspring = mutate(M=offspring,
                              mu_stress=float(config['Population']['mutation_rate_stress']),
                              mu_cooperation=float(config['Population']['mutation_rate_cooperation']),
                              Lmax=int(config['Population']['genome_length_max']),
                              stress_alleles=stress_alleles)

        # Merge in the offspring
        Mcopy = Mcopy.append(mu_offspring)

    # Reindex the metapopulation
    Mcopy.index = np.arange(Mcopy.shape[0])

    return Mcopy


def mutate(M, mu_stress, mu_cooperation, Lmax, stress_alleles):
    """Mutate individuals in the metapopulation"""
    assert 0 <= mu_stress <= 1
    assert 0 <= mu_cooperation <= 1
    assert Lmax >= 0
    assert stress_alleles >= 0

    Mcopy = M.copy(deep=True)

    # Mutations at stress loci
    # Alleles to mutate are chosen from a binomial distrubution, and these
    # alleles are modified by adding a random amount
    s = stress_loci(Lmax)
    if stress_alleles == 1:
        Mcopy[s] = bitwise_xor(Mcopy[s], binomial(n=1, p=mu_stress,
                                                  size=Mcopy[s].shape))
    else:
        # Small problem, an allele could mutate to itself.
        Mcopy[s] = (Mcopy[s] + (binomial(n=1, p=mu_stress, size=Mcopy[s].shape) * np.random.random_integers(low=1, high=stress_alleles, size=Mcopy[s].shape))) % (stress_alleles + 1)

    # Cooperation mutations - flip the cooperation bit 0->1 or 1->0
    Mcopy.Coop = bitwise_xor(Mcopy.Coop, binomial(n=1, p=mu_cooperation,
                                                  size=Mcopy.Coop.shape))

    return Mcopy

