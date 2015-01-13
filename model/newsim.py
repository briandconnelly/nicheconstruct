#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import SafeConfigParser

from Metapopulation import *
from misc import *
from Population import *
from Topology import *

config = SafeConfigParser()
config.read('run.cfg')

metapop = create_metapopulation(config)
topology = build_topology(config)

print(topology)
print(metapop.shape)
print(num_cooperators(metapop))
print(pct_cooperators(metapop))

print("-"*79)
metapop = bottleneck(metapop, 0.01)
print(metapop.shape)
print(num_cooperators(metapop))
print(pct_cooperators(metapop))

print("-"*79)
pop12 = get_population(metapop, 12)
print(pop12.shape)
print(num_cooperators(pop12))
print(pct_cooperators(pop12))

