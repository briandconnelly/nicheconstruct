# -*- coding: utf-8 -*-

"""Generic class for writing data to a file"""

import bz2
import csv

class OutputWriter(object):
    """Generic class for writing data to a file"""

    def __init__(self, simulation, filename, delimiter=','):
        """Initialize an OutputWriter object"""
        self.simulation = simulation
        self.filename = filename
        self.outfile = bz2.BZ2File(self.filename, 'w')
        self.writer = csv.writer(self.outfile, delimiter=delimiter)

    def update(self):
        """Update an OutputWriter object. This typically means writing a
        record of data to the file"""
        pass

    def close(self):
        """Close the file associated with the OutputWriter object"""
        self.outfile.close()

