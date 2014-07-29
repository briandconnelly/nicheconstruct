# -*- coding: utf-8 -*-

import csv

class ProducerOutput(object):

    def __init__(self, metapopulation, filename='popsize.csv', delimiter=','):
        self.metapopulation = metapopulation
        self.writer = csv.writer(open(filename, 'wb'), delimiter=delimiter)
        self.writer.writerow(['Time', 'Population', 'FracProducer'])

    def update(self, time):
        for n, d in self.metapopulation.topology.nodes_iter(data=True):
            self.writer.writerow([time, n, d['population'].prop_producers()])

