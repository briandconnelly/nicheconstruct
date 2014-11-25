# -*- coding: utf-8 -*-

"""Write information about each population in the metapopulation"""

from OutputWriter import OutputWriter


class PopulationDataOutput(OutputWriter):
    """Write information about each population in the metapopulation

    Data includes:
    * Time
    * Node ID (Population ID)
    * Genome Length
    * Size of Population
    * Average fitness
    * Number of Producers
    * Proportion of producers
    * Max producer fitness
    * Number of producer genotypes
    * Number of nonproducers
    * Proportion of nonproducers
    * Max nonproducer fitness
    * Number of nonproducer genotypes
    * Environment changed (0 or 1)

    """

    def __init__(self, metapopulation, filename='population.csv.bz2',
                 delimiter=','):
        super(PopulationDataOutput, self).__init__(metapopulation=metapopulation,
                                                 filename=filename,
                                                 delimiter=delimiter)

        self.writer.writerow(['Time', 'Population', 'GenomeLength', 'Size',
                              'AvgFitness', 'Producers', 'PropProducers',
                              'MaxProducerFitness', 'ProducerGenotypes',
                              'NonProducers', 'PropNonProducers',
                              'MaxNonProducerFitness', 'NonProducerGenotypes',
                              'EnvironmentChanged'])


    def update(self, time):
        for node, data in self.metapopulation.topology.nodes_iter(data=True):
            genomelength = data['population'].genome_length
            size = data['population'].size()
            num_producers = data['population'].num_producers()
            num_nonproducers = size - num_producers
            average_fitness = data['population'].average_fitness()
            prop_producers = data['population'].prop_producers()
            prop_nonproducers = data['population'].prop_nonproducers()
            maxfitnesses = data['population'].max_fitnesses()
            pgenotypes = data['population'].num_producer_genotypes()
            npgenotypes = data['population'].num_nonproducer_genotypes()
            envchange = int(data['population'].environment_changed)

            self.writer.writerow([time, node, genomelength, size,
                                  average_fitness, num_producers,
                                  prop_producers, maxfitnesses[0],
                                  pgenotypes, num_nonproducers,
                                  prop_nonproducers, maxfitnesses[1],
                                  npgenotypes, envchange])

