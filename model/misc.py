# -*- coding: utf-8 -*-

"""Miscellaneous functions"""

from numpy import where
from numpy.random import binomial

def bottleneck(population, survival_pct):
    """Submit the population to a bottleneck"""
    assert 0 <= survival_pct <= 1
    return population.drop(population.index[where(binomial(1, survival_pct,
                                                           population.index.shape[0]) == 0)])


def num_cooperators(population):
    """Get the number of cooperators in the population"""
    return population['Coop'].sum()


def pct_cooperators(population):
    """Get the proportion of cooperators in the population"""
    return population['Coop'].sum()/population.shape[0]


def stress_colnames(L=None):
    """TODO"""
    return ["S{0:02d}".format(i) for i in range(1, L + 1)]


