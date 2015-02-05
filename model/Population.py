# -*- coding: utf-8 -*-

"""Functions for working with individual populations"""

import numpy as np

from misc import stress_colnames

def assign_fitness(P, config):
    """Assign fitness for all individuals in the population"""

    base_fitness = float(config['Population']['base_fitness'])
    cost_cooperation = float(config['Population']['cost_cooperation'])
    delta = float(config['Population']['benefit_nonzero'])
    gamma = float(config['Population']['benefit_ordered'])

    num_stress_alleles = int(config['Population']['stress_alleles'])
    assert num_stress_alleles >= 0

    genome_length_max = int(config['Population']['genome_length_max'])
    assert genome_length_max >= 0

    stress_columns = stress_colnames(L=genome_length_max)
    stress_alleles = P.loc[:, stress_columns]

    allele_dist = np.apply_along_axis(lambda x: np.bincount(x, minlength=num_stress_alleles+1),
                                      axis=0, arr=stress_alleles)

    P.Fitness = base_fitness
    P.Fitness += np.sum(P[stress_columns] > 0, axis=1) * delta
    P.Fitness -= P.Coop * cost_cooperation

    if num_stress_alleles > 1 and num_stress_loci > 0:
        # Add gamma times the number of individuals with matching first allele
        # TODO: what if it is all zeros? A bunch of zeros would have higher fitness than delta.
        P.Fitness += allele_dist[stress_alleles[stress_columns[0]], 0] * gamma

        # Add gamma times the number of individuals with increasing allele value
        stress_alleles_next = (1 + (stress_alleles % num_stress_alleles)).values[:,:-1]
        allele_dist_next = allele_dist[:,1:]
        P.Fitness += allele_dist_next[stress_alleles_next, range(genome_length_max-1)].sum(axis=1) * gamma

    return P

