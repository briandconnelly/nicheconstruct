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
    * Max number of ones in producer genotypes
    * Max producer fitness
    * Number of producer genotypes
    * Number of nonproducers
    * Proportion of nonproducers
    * Max number of ones in nonproducer genotypes
    * Max nonproducer fitness
    * Number of nonproducer genotypes
    * Environment changed (0 or 1)

    """

    def __init__(self, simulation, filename='population.csv.bz2',
                 delimiter=','):
        super(PopulationDataOutput, self).__init__(simulation=simulation,
                                                 filename=filename,
                                                 delimiter=delimiter)

        self.writer.writerow(['Time', 'Population', 'GenomeLength', 'Size',
                              'AvgFitness', 'Producers', 'PropProducers',
                              'MaxProducerOnes', 'MaxProducerFitness',
                              'ProducerGenotypes', 'NonProducers',
                              'PropNonProducers', 'MaxNonProducerOnes',
                              'MaxNonProducerFitness', 'NonProducerGenotypes',
                              'EnvironmentChanged'])


    def update(self):
        for node, data in self.simulation.metapopulation.topology.nodes_iter(data=True):
            pop = data['population']
            genomelength = pop.genome_length
            size = pop.size()
            num_producers = pop.num_producers()
            num_nonproducers = size - num_producers
            average_fitness = pop.average_fitness()
            prop_producers = pop.prop_producers()
            prop_nonproducers = pop.prop_nonproducers()
            maxones = pop.max_ones()
            maxfitnesses = pop.max_fitnesses()
            pgenotypes = pop.num_producer_genotypes()
            npgenotypes = pop.num_nonproducer_genotypes()
            envchange = int(pop.environment_changed)

            self.writer.writerow([self.simulation.cycle, node, genomelength,
                                  size, average_fitness, num_producers,
                                  prop_producers, maxones[0], maxfitnesses[0],
                                  pgenotypes, num_nonproducers,
                                  prop_nonproducers, maxones[1],
                                  maxfitnesses[1], npgenotypes, envchange])

