# -*- coding: utf-8 -*-

"""Write information about each population in the metapopulation"""

import sys

from genome import is_producer, num_ones
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
    * Genotype
    * IsProducer (0 or 1)
    * Non-social portion of genotype
    * Number of Ones
    * Visible portion of genotype (not including social locus)
    * Visible number of ones
    * Abundance
    * Fitness

    """

    def __init__(self, simulation, filename='genotypes.csv.bz2',
                 delimiter=','):
        super(GenotypesOutput, self).__init__(simulation=simulation,
                                              filename=filename,
                                              delimiter=delimiter)

        self.writer.writerow(['Time', 'Population', 'GenomeLength', 
                              'Genotype', 'IsProducer', 'NonsocialGenotype',
                              'NumOnes', 'VisibleGenotype', 'VisibleNumOnes',
                              'Abundance', 'Fitness'])


    def update(self, time):
        for node, data in self.simulation.metapopulation.topology.nodes_iter(data=True):
            pop = data['population']
            L = pop.genome_length
            Lmax = pop.genome_length_max

            for genotype in xrange(pop.abundances.size):
                visible = genotype & ((2**L) - 1)
                nonsocial = genotype & (2**Lmax - 1)

                self.writer.writerow([time, node, L, genotype,
                                      is_producer(genotype, Lmax),
                                      nonsocial, num_ones(nonsocial), visible,
                                      num_ones(visible),
                                      pop.abundances[genotype],
                                      pop.fitness_landscape[genotype]])

