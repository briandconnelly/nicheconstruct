# -*- coding: utf-8 -*-

import bz2
import csv

import OutputWriter
import Population


class FitnessOutput(OutputWriter.OutputWriter):

    def __init__(self, metapopulation, filename='max_fitness.csv.bz2', delimiter=','):
        super(FitnessOutput, self).__init__(metapopulation=metapopulation,
                                            filename=filename,
                                            delimiter=delimiter)

        self.writer.writerow(['Time', 'Producers', 'Nonproducers'])

    def update(self, time):
        maxfit = self.metapopulation.max_fitnesses()
        self.writer.writerow([time, max(maxfit[0]), max(maxfit[1])])
