# -*- coding: utf-8 -*-

"""Write information about metapopulation fitness to a file"""

import OutputWriter


class FitnessOutput(OutputWriter.OutputWriter):
    """Write information about the distribution of fitness within the
    metapopulation

    Data includes:
    * Time
    * Maximum fitness of producers
    * Maximum fitness of non-producers

    """

    def __init__(self, simulation, filename='max_fitness.csv.bz2',
                 delimiter=','):
        super(FitnessOutput, self).__init__(simulation=simulation,
                                            filename=filename,
                                            delimiter=delimiter)

        self.writer.writerow(['Time', 'Producers', 'Nonproducers'])

    def update(self, time):
        maxfit = self.simulation.metapopulation.max_fitnesses()
        self.writer.writerow([time, max(maxfit[0]), max(maxfit[1])])
