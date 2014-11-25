# -*- coding: utf-8 -*-

"""Write demographic information about the metapopulation"""

from OutputWriter import OutputWriter


class DemographicsOutput(OutputWriter):
    """Write demographic information about each population in the
    metapopulation

    Data includes:
    * Time
    * Node ID (Population ID)
    * Genome Length
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

        self.writer.writerow(['Time', 'Population', 'GenomeLength', 'Size',
                              'Producers', 'PropProducers', 'NonProducers',
                              'PropNonProducers', 'AvgFitness'])


    def update(self, time):
        for node, data in self.metapopulation.topology.nodes_iter(data=True):
            genomelength = data['population'].genome_length
            size = data['population'].size()
            num_producers = data['population'].num_producers()
            num_nonproducers = size - num_producers
            average_fitness = data['population'].average_fitness()
            prop_producers = data['population'].prop_producers()
            prop_nonproducers = data['population'].prop_nonproducers()

            self.writer.writerow([time, node, genomelength, size,
                                  num_producers, prop_producers,
                                  num_nonproducers, prop_nonproducers,
                                  average_fitness])

