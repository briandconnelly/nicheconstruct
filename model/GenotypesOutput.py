# -*- coding: utf-8 -*-

"""Write information about each population in the metapopulation"""

import sys

from genome import is_producer
from OutputWriter import OutputWriter

if sys.version_info[0] == 3:
    xrange = range

class GenotypesOutput(OutputWriter):
    """Write information about each population in the metapopulation

    Note: THIS PRODUCES A LOT OF DATA!!!!!

    Data includes:
    * Time
    * Population
    * Genome length
    * Genotype (fitness encoding portion)
    * IsProducer (0 or 1)
    * Abundance

    """

    def __init__(self, metapopulation, filename='genotypes.csv.bz2',
                 delimiter=','):
        super(GenotypesOutput, self).__init__(metapopulation=metapopulation,
                                              filename=filename,
                                              delimiter=delimiter)

        self.writer.writerow(['Time', 'Population', 'GenomeLength', 
                              'Genotype', 'IsProducer', 'Abundance'])


    def update(self, time):
        for node, data in self.metapopulation.topology.nodes_iter(data=True):

            L = data['population'].genome_length
            Lmax = data['population'].genome_length_max

            for genotype in xrange(data['population'].abundances.size):
                self.writer.writerow([time, node, L, genotype,
                                      is_producer(genotype, Lmax),
                                      data['population'].abundances[genotype]])

