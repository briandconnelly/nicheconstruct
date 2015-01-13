# -*- coding: utf-8 -*-

from numpy import where
from numpy.random import binomial

def bottleneck(P, survival_pct):
    """Submit the population to a bottleneck"""
    assert 0 <= survival_pct <= 1
    return P.drop(P.index[where(binomial(1, survival_pct, P.shape[0])==0)])

def num_cooperators(P):
    """Get the number of cooperators in the population"""
    return P['Coop'].sum()

def pct_cooperators(P):
    """Get the proportion of cooperators in the population"""
    return P['Coop'].sum()/P.shape[0]

def size(P):
    """Get the size of the population"""
    return P.shape[0]

