# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


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


    M = pd.DataFrame({'Population': np.repeat(np.arange(size),
                                              initial_popsize),
                      'Coop': np.random.binomial(1,
                                                 initial_producer_proportion,
                                                 size*initial_popsize) == 1
                     })

    for locus in ["S{0:02d}".format(x) for x in range(1, genome_length_max+1)]:
        M[locus] = np.zeros(M.shape[0])

    return M


def mix(M, topology):
    """Mix the metapopulation

    Mixing creates the individuals in a metapopulation to be re-distributed
    evenly among the populations
    """

    Mcopy = M.copy(deep=True)
    Mcopy['Population'] = np.random.random_integers(low=0,
                                                    high=len(topology)-1,
                                                    size=Mcopy.shape[0])
    return Mcopy

