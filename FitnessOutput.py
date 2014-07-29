# -*- coding: utf-8 -*-

import csv

class FitnessOutput(object):

    def __init__(self, metapopulation, filename='fitness.csv', delimiter=','):
        self.metapopulation = metapopulation
        self.writer = csv.writer(open(filename, 'wb'), delimiter=delimiter)
        self.writer.writerow(['Time', 'Population', 'AvgFitness'])

    def update(self, time):
        for n, d in self.metapopulation.topology.nodes_iter(data=True):
            # TODO: get the average fitness of the population
            # TODO: make this a function in Population
            self.writer.writerow([time, n, 'TODO'])

