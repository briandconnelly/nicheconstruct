# -*- coding: utf-8 -*-

"""Miscellaneous functions"""

import datetime
import getpass
import platform
import sys

import networkx as nx
import numpy as np
from numpy import where
from numpy.random import binomial
import pandas as pd


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


def write_run_information(filename, config):
    """ Write information about the run and software environment """

    with open(filename, 'w') as infofile:
        infostr = 'Generated by {whom} at {when}\n'
        infofile.write(infostr.format(when=datetime.datetime.now().isoformat(),
                                        whom=getpass.getuser()))
        infofile.write('Host: {p}\n'.format(p=platform.node()))
        infofile.write('Platform: {p}\n'.format(p=platform.platform()))
        infofile.write('Python Version: {v}\n'.format(v=".".join([str(n) for n in sys.version_info[:3]])))
        infofile.write('Pandas Version: {v}\n'.format(v=pd.version.version))
        infofile.write('NumPy Version: {v}\n'.format(v=np.version.version))
        infofile.write('NetworkX Version: {v}\n'.format(v=nx.__version__))
        infofile.write('Command: {cmd}\n'.format(cmd=' '.join(sys.argv)))
        infofile.write('Random Seed: {seed}\n'.format(seed=config['Simulation']['seed']))
        infofile.write('UUID: {uuid}\n'.format(uuid=config['Simulation']['UUID']))

