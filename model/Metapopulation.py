# -*- coding: utf-8 -*-

"""Functions for working with Metapopulations"""

import numpy as np
from numpy import bitwise_xor, where
from numpy.random import binomial
import pandas as pd

from Topology import random_neighbor
from misc import stress_colnames


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

    stress_columns = stress_colnames(L=genome_length_max)
    data = {'Time': 0,
            'Population': np.repeat(np.arange(size), initial_popsize).tolist(),
            'Coop': (np.random.binomial(1, initial_cooperator_proportion, size * initial_popsize) == 1).tolist(),
            'Fitness': 0}
    data.update({sc: np.zeros(size * initial_popsize, dtype=np.int).tolist() for sc in stress_columns})
    M = pd.DataFrame(data,
                     columns=['Time', 'Population', 'Coop'] + ["S{0:02d}".format(i) for i in np.arange(1,genome_length_max+1)] + ['Fitness'])

    M = assign_fitness(M=M, config=config)
    return M


# TODO: take an argument for number of fitness-encoding loci
def assign_fitness(M, config):
    """Assign fitness for all individuals in the metapopulation"""

    base_fitness = float(config['Population']['base_fitness'])
    cost_cooperation = float(config['Population']['cost_cooperation'])
    delta = float(config['Population']['benefit_nonzero'])
    gamma = float(config['Population']['benefit_ordered'])

    num_stress_alleles = int(config['Population']['stress_alleles'])
    assert num_stress_alleles >= 0

    genome_length_max = int(config['Population']['genome_length_max'])
    assert genome_length_max >= 0

    stress_columns = stress_colnames(L=genome_length_max)
    stress_alleles = M[stress_columns]

    allele_dist = np.apply_along_axis(lambda x: np.bincount(x, minlength=num_stress_alleles+1),
                                      axis=0, arr=stress_alleles)

    M.Fitness = base_fitness
    M.Fitness += np.sum(M[stress_columns] > 0, axis=1) * delta
    M.Fitness -= M.Coop * cost_cooperation

    if num_stress_alleles > 1 and num_stress_loci > 0:
        # Add gamma times the number of individuals with matching first allele
        # TODO: what if it is all zeros? A bunch of zeros would have higher fitness than delta.
        M.Fitness += allele_dist[stress_alleles[stress_columns[0]], 0] * gamma

        # Add gamma times the number of individuals with increasing allele value
        stress_alleles_next = (1 + (stress_alleles % num_stress_alleles)).values[:,:-1]
        allele_dist_next = allele_dist[:,1:]
        M.Fitness += allele_dist_next[stress_alleles_next, range(genome_length_max-1)].sum(axis=1) * gamma

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

    M.Population = np.random.random_integers(low=0, high=len(topology)-1,
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
                                                  size=Mcopy.Coop.shape))

    # Mutations at stress loci
    # Alleles to mutate are chosen from a binomial distrubution, and these
    # alleles are modified by adding a random amount
    s = stress_colnames(L=Lmax)
    if num_stress_alleles == 1:
        Mcopy[s] = bitwise_xor(Mcopy[s], binomial(n=1, p=mu_stress,
                                                  size=Mcopy[s].shape))
    else:
        # Small problem, an allele could mutate to itself.
        Mcopy[s] = (Mcopy[s] + (binomial(n=1, p=mu_stress, size=Mcopy[s].shape) * np.random.random_integers(low=1, high=num_stress_alleles, size=Mcopy[s].shape))) % (num_stress_alleles + 1)

    return Mcopy


def grow(M, genome_lengths, config):
    """Grow the population"""

    base_fitness = float(config['Population']['base_fitness'])
    cost_cooperation = float(config['Population']['cost_cooperation'])
    delta = float(config['Population']['benefit_nonzero'])
    gamma = float(config['Population']['benefit_ordered'])

    smin = float(config['Population']['capacity_min'])
    smax = float(config['Population']['capacity_max'])
    assert 0 <= smin <= smax

    num_stress_alleles = int(config['Population']['stress_alleles'])
    assert num_stress_alleles >= 0

    genome_length_max = int(config['Population']['genome_length_max'])
    mu_stress = float(config['Population']['mutation_rate_stress'])
    mu_cooperation = float(config['Population']['mutation_rate_cooperation'])

    stress_columns = stress_colnames(L=genome_length_max)

    for popid, subpop in M.groupby('Population'):
        num_offspring = smin + round(subpop.Coop.mean() * (smax - smin)) - len(subpop)

        parent_num_offspring = np.random.multinomial(n=num_offspring,
                                                     pvals=subpop.Fitness/subpop.Fitness.sum())

        # parent_num_offspring is an array where each element represents a
        # parent (relative index), and the value contains the number of
        # offspring
        offspring = subpop.iloc[np.repeat(np.arange(len(parent_num_offspring)),
                                          parent_num_offspring)]

        # Mutate the offspring
        mu_offspring = mutate(M=offspring,
                              mu_stress=mu_stress,
                              mu_cooperation=mu_cooperation,
                              Lmax=genome_length_max,
                              num_stress_alleles=num_stress_alleles)
        mu_offspring = assign_fitness(M=mu_offspring, config=config)

        # Merge in the offspring
        M = M.append(mu_offspring)

    # Reindex the metapopulation
    M.index = np.arange(len(M))

    return M

