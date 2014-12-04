"""Represent a Simulation"""

import datetime
import getpass
import os
import platform
import sys

import networkx as nx
import numpy as np

from Metapopulation import Metapopulation
from FitnessOutput import FitnessOutput
from GenotypesOutput import GenotypesOutput
from PopulationDataOutput import PopulationDataOutput


class Simulation(object):
    def __init__(self, config):
        """Initialize a Simulation object"""
        self.config = config
        self.cycle = 0

        # Set the seed for the pseudorandom number generator
        # If one does not already exist in the config, generate one
        if not self.config.has_option(section='Simulation', option='seed'):
            seed = np.random.randint(low=0, high=np.iinfo(np.uint32).max)
            self.config.set(section='Simulation', option='seed',
                            value=str(seed))

        np.random.seed(seed=self.config.getint(section='Simulation',
                                               option='seed'))


        # Create the data directory
        self.data_dir = self.config.get(section='Simulation',
                                        option='data_dir')
        os.mkdir(self.data_dir)


        # Set up logging
        self.log_frequency = self.config.getint(section='Simulation',
                                                option='log_frequency')
        assert self.log_frequency > 0

        self.log_objects = []

        log_population = self.config.getboolean(section='Simulation',
                                                option='log_population')
        log_fitness = self.config.getboolean(section='Simulation',
                                             option='log_fitness')
        log_genotypes = self.config.getboolean(section='Simulation',
                                               option='log_genotypes')

        if log_population:
            out_population = PopulationDataOutput(simulation=self,
                                                  filename=os.path.join(self.data_dir, 'population.csv.bz2'))
            self.log_objects.append(out_population)

        if log_genotypes:
            out_genotypes = GenotypesOutput(simulation=self,
                                            filename=os.path.join(self.data_dir, 'genotypes.csv.bz2'))
            self.log_objects.append(out_genotypes)

        if log_fitness:
            out_fitness = FitnessOutput(simulation=self,
                                        filename=os.path.join(self.data_dir, 'fitness.csv.bz2'))
            self.log_objects.append(out_fitness)


        # Write the configuration file and some additional information
        cfg_out = os.path.join(self.data_dir, 'configuration.cfg')
        with open(cfg_out, 'w') as configfile:
            configfile.write('# Generated: {when} by {whom} on {where}\n'.format(when=datetime.datetime.now().isoformat(),
                                                                                 whom=getpass.getuser(),
                                                                                 where=platform.node()))
            configfile.write('# Platform: {p}\n'.format(p=platform.platform()))
            configfile.write('# Python version: {v}\n'.format(v=".".join([str(n) for n in sys.version_info[:3]])))
            configfile.write('# NumPy version: {v}\n'.format(v=np.version.version))
            configfile.write('# NetworkX version: {v}\n'.format(v=nx.__version__))
            configfile.write('# Command: {cmd}\n'.format(cmd=' '.join(sys.argv)))
            configfile.write('# {line}\n\n'.format(line='-'*77))
            config.write(configfile)


        # Create the metapopulation
        self.metapopulation = Metapopulation(config=self.config)

        # Export the metapopulation topology
        export_topology = self.config.getboolean(section='Simulation',
                                                 option='export_topology')

        if export_topology:
            nx.write_gml(self.metapopulation.topology,
                         os.path.join(self.data_dir, 'topology.gml'))


        # Simulation parameters
        self.num_cycles = self.config.getint(section='Simulation',
                                             option='num_cycles')
        assert self.num_cycles > 0

        self.cycle = 0
        self.proceed = self.cycle < self.num_cycles

        self.stop_on_empty = self.config.getboolean(section='Simulation',
                                                    option='stop_on_empty')


    def __iter__(self):
        """Create an iterator for Simulation objects"""
        return self


    def __next__(self):
        """Run the Simulation for one time step and return (Python 3)"""
        return self.next()


    def next(self):
        """Run the Simulation for one time step and return (Python 2)"""

        if not self.proceed:
            self.write_logfiles()
            self.cleanup()
            raise StopIteration

        self.write_logfiles()
        self.metapopulation.cycle()

        self.cycle += 1
        self.proceed = self.cycle < self.num_cycles

        # Stop iterating if the metapopulation is empty
        if self.stop_on_empty and self.metapopulation.size() == 0:
            self.proceed = False

        return self


    def write_logfiles(self):
        """Write any log files"""

        if self.cycle % self.log_frequency == 0:
            for log in self.log_objects:
                log.update()


    def cleanup(self):
        """Perform cleanup tasks when the object is cleaned up"""
        for log in self.log_objects:
            log.close()


    def statusbar(self):
        """Create a representation of the Simulation to use as a status bar
        """

        num_ticks = 5
        prop_producers = self.metapopulation.prop_producers()

        if prop_producers == 'NA':
            return "[Empty Metapopulation]"

        symbol = '='

        if self.metapopulation._prev_prop_producers == 'NA':
            delta = ' '
        elif self.metapopulation._prev_prop_producers > prop_producers:
            delta = u'\u2193'.encode('utf-8')
        elif self.metapopulation._prev_prop_producers < prop_producers:
            delta = u'\u2191'.encode('utf-8')
        else:
            delta = '-'

        (pfr, nfr) = self.metapopulation.max_fitnesses()
        pf = max(pfr)
        nf = max(nfr)

        plabel = 'P'
        nlabel = 'N'

        if pf > nf:
            plabel = '\033[1m' + 'P' + '\033[0m'
        elif nf > pf:
            nlabel = '\033[1m' + 'N' + '\033[0m'

        pbars = int(round(num_ticks * max(0, prop_producers - 0.5) / 0.5))
        nbars = int(round(num_ticks * max(0, 1 - prop_producers - 0.5) / 0.5))
        bar_layout = "Cycle {c}: {N} [{sn}{bn}|{bp}{sp}] {P} ({d}{p:.1%}), Size: {s}"
        return bar_layout.format(c=str(self.cycle).rjust(len(str(self.num_cycles))),
                                 bn=nbars*symbol, bp=pbars*symbol,
                                 sn=(num_ticks-nbars)*' ',
                                 sp=(num_ticks-pbars)*' ', p=prop_producers,
                                 s=self.metapopulation.size(),
                                 N=nlabel,
                                 P=plabel,
                                 d=delta)

