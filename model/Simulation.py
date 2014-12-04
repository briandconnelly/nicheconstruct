"""Represent a Simulation"""

import datetime
import getpass
import os
import platform
import sys

import networkx as nx
import numpy as np

from Metapopulation import Metapopulation


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

        if self.log_population:
            out_population = PopulationDataOutput(metapopulation=self,
                                                  filename=os.path.join(self.data_dir, 'population.csv.bz2'))
            self.log_objects.append(out_population)

        if self.log_genotypes:
            out_genotypes = GenotypesOutput(metapopulation=self,
                                            filename=os.path.join(self.data_dir, 'genotypes.csv.bz2'))
            self.log_objects.append(out_genotypes)

        if self.log_fitness:
            out_fitness = FitnessOutput(metapopulation=self,
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

        self.stop_on_empty = self.config.getboolean(section='Simulation',
                                                    option='stop_on_empty')
        

    def write_logfiles(self):
        """Write any log files"""

        if self.cycle % self.log_frequency == 0:
            for log in self.log_objects:
                # TODO: remove the time argument?
                log.update(time=self.time)

