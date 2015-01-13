# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

def create_metapopulation(config):
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

    # TODO
    num_populations = 500

    # TODO: build the data frame
    M = pd.DataFrame({'Population': np.repeat(np.arange(num_populations),
                                              initial_popsize)
                     })

    return M
