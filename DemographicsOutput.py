# -*- coding: utf-8 -*-

import bz2
import csv

import Population

class DemographicsOutput(object):

    def __init__(self, metapopulation, filename='demographics.csv.bz2', delimiter=','):
        self.metapopulation = metapopulation
        self.writer = csv.writer(bz2.BZ2File(filename, 'wb'), delimiter=delimiter)

        self.writer.writerow(['Time', 'Population', 'Size', 'Producers',
                              'PropProducers', 'NonProducers',
                              'PropNonProducers', 'AvgFitness'])

    def update(self, time):
        for n, d in self.metapopulation.topology.nodes_iter(data=True):
            size = len(d['population'])
            num_producers = d['population'].num_producers()
            num_nonproducers = size - num_producers

            if size == 0:
                prop_producers = 'NA'
                prop_nonproducers = 'NA'
            else:
                prop_producers = 1.0*num_producers/size
                prop_nonproducers = 1.0*num_nonproducers/size

            average_fitness = d['population'].average_fitness()

            self.writer.writerow([time, n, size, num_producers, prop_producers,
                                  num_nonproducers, prop_nonproducers,
                                  average_fitness])

