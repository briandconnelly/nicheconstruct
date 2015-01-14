# -*- coding: utf-8 -*-

"""Functions for working with individual populations"""


# Currently unused. Probably not needed.
def get_population(M, popid):
    """Get data corresponding to the given population (ID)"""
    return M[M.Population == popid]


# Could this instead take a metapopulation and an optional population ID?
def population_allele_frequencies(P):
    """TODO"""
    pass

