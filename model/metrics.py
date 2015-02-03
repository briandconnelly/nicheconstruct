# -*- coding: utf-8 -*-

"""Functions for getting metrics about the (meta)population"""

def is_empty(population, popid=None):
    """Return whether or not there are no individuals in the (meta)population"""
    if popid:
        return popid in population.Population.values
    else:
        return population.shape[0] == 0


def allele_frequencies(population, popid=None):
    """TODO"""
    pass

