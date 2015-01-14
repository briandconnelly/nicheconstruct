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

    initial_producer_proportion = float(config['Population']['initial_producer_proportion'])
    assert 0 <= initial_producer_proportion <= 1

    genome_length_min = int(config['Population']['genome_length_min'])
    genome_length_max = int(config['Population']['genome_length_max'])
    assert 0 <= genome_length_min <= genome_length_max

    initial_popsize = capacity_min + \
                  (initial_producer_proportion * (capacity_max - capacity_min))

    cols = {'Population': np.repeat(np.arange(size), initial_popsize),
            'Coop': binomial(1, initial_producer_proportion,
                             size*initial_popsize) == 1}
    cols.update({"S{0:02d}".format(i): np.zeros(size*initial_popsize, dtype=np.int) for i in range(1, genome_length_max + 1)})

    return pd.DataFrame(cols)


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


def grow(M, config):
    """Grow the population"""
    # Mcopy.loc[Mcopy.shape[0]] = [NEW_ROW]
    pass


# Separate into two functions, one for stress and one for coop? Makes sense since bit flip on coop is easier.
def mutate(M, mu_stress, mu_cooperation, Lmax, stress_alleles):
    assert 0 <= mu_stress <= 1
    assert 0 <= mu_cooperation <= 1
    assert Lmax > 0
    assert stress_alleles >= 0

    Mcopy = M.copy(deep=True)

    # Mutations at stress loci
    # Alleles to mutate are chosen from a binomial distrubution, and these
    # alleles are modified by adding a random amount
    s = stress_loci(Lmax)
    Mcopy[s] = (Mcopy[s] + (binomial(n=1, p=mu_stress, size=Mcopy[s].shape) * np.random.random_integers(1,2*stress_alleles, Mcopy[s].shape))) % stress_alleles

    # Cooperation mutations - flip the cooperation bit 0->1 or 1->0
    Mcopy['Coop'] = bitwise_xor(Mcopy['Coop'], binomial(n=1, p=mu_cooperation,
                                                        size=Mcopy.shape[0]))

    return Mcopy

