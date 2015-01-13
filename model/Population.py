# -*- coding: utf-8 -*-

def get_population(M, pid):
    """Get data corresponding to the given population (ID)"""
    return M[M['Population']==pid]


# Could this instead take a metapopulation and an optional population ID?
def population_allele_frequencies(P):
    """TODO"""
    pass
