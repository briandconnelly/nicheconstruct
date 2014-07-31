# -*- coding: utf-8 -*-

import bz2
import csv

class OutputWriter(object):

    def __init__(self, metapopulation, filename, delimiter=','):
        self.metapopulation = metapopulation
        self.outfile = bz2.BZ2File(filename, 'wb')
        self.writer = csv.writer(self.outfile, delimiter=delimiter)

    def update(self, time):
        pass

    def close(self):
        self.outfile.close()
