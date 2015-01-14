# -*- coding: utf-8 -*-

import datetime
import getpass
import platform
import sys

import networkx as nx
import numpy as np
from numpy import where, version
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


def write_configuration(config, filename='configuration.cfg'):
    """Write the configuration to a file"""

    with open(filename, 'w') as configfile:
        infostr = '# Generated: {when} by {whom} on {where}\n'
        configfile.write(infostr.format(when=datetime.datetime.now().isoformat(),
                                        whom=getpass.getuser(),
                                        where=platform.node()))
        configfile.write('# Platform: {p}\n'.format(p=platform.platform()))
        configfile.write('# Python version: {v}\n'.format(v=".".join([str(n) for n in sys.version_info[:3]])))
        configfile.write('# NumPy version: {v}\n'.format(v=np.version.version))
        configfile.write('# NetworkX version: {v}\n'.format(v=nx.__version__))
        configfile.write('# Command: {cmd}\n'.format(cmd=' '.join(sys.argv)))
        configfile.write('# {line}\n\n'.format(line='-'*77))
        config.write(configfile)

