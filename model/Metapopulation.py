# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

def create_metapopulation(config, size):
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

    assert size > 0
    num_populations = size

    M = pd.DataFrame({'Population': np.repeat(np.arange(num_populations),
                                              initial_popsize)
                     })

    for locus in ["S{0:02d}".format(x) for x in range(1,genome_length_max+1)]:
        M[locus] = np.zeros(M.shape[0])

    M['Coop'] = np.random.binomial(1, initial_producer_proportion, M.shape[0])==1

    return M

