# -*- coding: utf-8 -*-

import bz2
import csv

import numpy as np

from OutputWriter import OutputWriter
import genome


class GenotypesOutput(OutputWriter):

    def __init__(self, metapopulation, filename='genotypes.csv.bz2', delimiter=','):

        super(GenotypesOutput, self).__init__(metapopulation=metapopulation,
                                              filename=filename,
                                              delimiter=delimiter)

        self.genome_length = self.metapopulation.config.getint(section='Population',
                                           option='genome_length')

        self.writer.writerow(['Time', 'Genotype', 'AvgAbundance', 'IsProducer'])

    def update(self, time):
        abundances = []
        abundances = np.array([d['population'].abundances for n, d in self.metapopulation.topology.nodes_iter(data=True)])
        av = np.average(abundances, 0)
        
        for i in range(2**(self.genome_length+1)):
            isprod = genome.is_producer(i, self.genome_length)
            genotype = i & 2**(self.genome_length)-1
            self.writer.writerow([time, genotype, av[i], isprod])

