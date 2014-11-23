# -*- coding: utf-8 -*-

"""Write demographic information about the metapopulation"""

from OutputWriter import OutputWriter


class DemographicsOutput(OutputWriter):
    """Write demographic information about each population in the
    metapopulation

    Data includes:
    * Time
    * Node ID (Population ID)
    * Size of Population
    * Number of Producers
    * Proportion of producers
    * Number of nonproducers
    * Proportion of nonproducers
    * Average fitness

    """

    def __init__(self, metapopulation, filename='demographics.csv.bz2',
                 delimiter=','):
        super(DemographicsOutput, self).__init__(metapopulation=metapopulation,
                                                 filename=filename,
                                                 delimiter=delimiter)

        self.writer.writerow(['Time', 'Population', 'Size', 'Producers',
                              'PropProducers', 'NonProducers',
                              'PropNonProducers', 'AvgFitness'])

    def update(self, time):
        for node, data in self.metapopulation.topology.nodes_iter(data=True):
            size = len(data['population'])

            if size == 0:
                num_producers = 0
                num_nonproducers = 0
                prop_producers = 'NA'
                prop_nonproducers = 'NA'
                average_fitness = 'NA'
            else:
                num_producers = data['population'].num_producers()
                num_nonproducers = size - num_producers
                prop_producers = 1.0*num_producers/size
                prop_nonproducers = 1.0*num_nonproducers/size
                average_fitness = data['population'].average_fitness()

            self.writer.writerow([time, node, size, num_producers,
                                  prop_producers, num_nonproducers,
                                  prop_nonproducers, average_fitness])

