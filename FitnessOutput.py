# -*- coding: utf-8 -*-

import csv

class FitnessOutput(object):

    def __init__(self, metapopulation, filename='fitness.csv'):
        self.metapopulation = metapopulation
        self.writer = csv.writer(open(filename, 'wb'))
        self.writer.writerow(['Time', 'Population', 'AvgFitness'])

    def update(self, time):
        for n, d in self.metapopulation.topology.nodes_iter(data=True):
#            self.writer.writerow([time, n, d['population'].size()])
            self.writer.writerow([time, 'TODO', 'TODO'])

