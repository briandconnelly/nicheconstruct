# -*- coding: utf-8 -*-

"""Functions for getting metrics about the (meta)population"""

def size(P, popid=None):
    """Get the number of organisms in the (meta)population"""
    if popid:
        return P[P['Population'] == popid].shape[0]
    else:
        return P.shape[0]


def is_empty(P, popid=None):
    """Return whether or not there are no individuals in the (meta)population"""
    if popid:
        return P[P['Population'] == popid].shape[0] == 0
    else:
        return P.shape[0] == 0


def allele_frequencies(P, popid=None):
    """TODO"""
    pass

