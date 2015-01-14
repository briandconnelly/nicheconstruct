# -*- coding: utf-8 -*-

"""Functions for getting metrics about the (meta)population"""

def size(population, popid=None):
    """Get the number of organisms in the (meta)population"""
    if popid:
        return population[population['Population'] == popid].shape[0]
    else:
        return population.shape[0]


def is_empty(population, popid=None):
    """Return whether or not there are no individuals in the (meta)population"""
    if popid:
        return population[population['Population'] == popid].shape[0] == 0
    else:
        return population.shape[0] == 0


def allele_frequencies(population, popid=None):
    """TODO"""
    pass

