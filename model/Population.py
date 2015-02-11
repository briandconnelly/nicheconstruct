# -*- coding: utf-8 -*-

"""Functions for working with individual populations"""

import numpy as np

from misc import stress_colnames


def assign_fitness(P, genome_length, num_stress_alleles, base_fitness,
                   cost_cooperation, benefit_nonzero, benefit_ordered):
    """Assign fitness for all individuals in the population"""

    assert genome_length >= 0
    assert num_stress_alleles > 0

    P.Fitness = base_fitness - (P.Coop * cost_cooperation)

    if genome_length > 0:
        stress_columns = stress_colnames(L=genome_length)
        stress_alleles = P.loc[:, stress_columns]

        P.Fitness += np.sum(P[stress_columns] > 0, axis=1) * benefit_nonzero

        if num_stress_alleles > 1:
            # Fitness is proportional to the number of individuals in the 
            # population with the same allele at each locus. Get the
            # distribution of alleles in the population (per locus). Since
            # the 0 allele is the absence of adaptation, it does not contribute
            # to fitness.
            allele_dist = np.apply_along_axis(lambda x: np.bincount(x, minlength=num_stress_alleles+1),
                                              axis=0, arr=stress_alleles)
            allele_dist[0] = np.zeros(allele_dist.shape[1])

            # Add gamma times the number of individuals with matching first allele
            P.Fitness += allele_dist[stress_alleles[stress_columns[0]], 0] * benefit_ordered

            # Add gamma times the number of individuals with increasing allele value
            stress_alleles_next = (1 + (stress_alleles % num_stress_alleles)).values[:,:-1]
            allele_dist_next = allele_dist[:,1:]
            P.Fitness += allele_dist_next[stress_alleles_next, range(genome_length-1)].sum(axis=1) * benefit_ordered

    return P

