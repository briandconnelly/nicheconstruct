#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from configparser import SafeConfigParser
import csv
import datetime
import os
from warnings import warn

from Metapopulation import *
from metrics import *
from misc import *
from Population import *
from Topology import *

__version__ = '0.2.0'


def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(prog='ncsimulate.py',
                                     description='Run a simluation')
    parser.add_argument('--config', '-c', metavar='FILE', help='Configuration '\
                        'file to use (default: run.cfg)', default='run.cfg',
                        dest='configfile', type=argparse.FileType('r'))
    parser.add_argument('--data_dir', '-d', metavar='DIR',
                        help='Directory to store data (default: data)')
    parser.add_argument('--param', '-p', nargs=3, metavar=('SECTION', 'NAME',
                                                           'VALUE'),
                        action='append', help='Set a parameter value')
    parser.add_argument('--seed', '-s', metavar='S', help='Set the '\
                        'pseudorandom number generator seed', type=int)
    parser.add_argument('--quiet', '-q', action='store_true', default=False,
                        help='Suppress output messages')
    parser.add_argument('--version', action='version', version=__version__)

    return parser.parse_args()


def main():
    """Run a simulation"""

    # Get the command line arguments
    args = parse_arguments()

    # Read the configuration file
    config = SafeConfigParser()
    config.readfp(args.configfile)
    args.configfile.close()

    # Add any parameters specified on the command line to the configuration
    if args.param:
        for param in args.param:
            config[param[0]][param[1]] = param[2]


    # If the random number generator seed specified, add it to the config,
    # overwriting any previous value. Otherwise, if it wasn't in the
    # supplied configuration file, create one.
    if args.seed:
        config['Simulation']['seed'] = str(args.seed)
    elif not config.has_option(section='Simulation', option='seed'):
        seed = np.random.randint(low=0, high=np.iinfo(np.uint32).max)           
        config['Simulation']['seed'] = str(seed)

    np.random.seed(seed=int(config['Simulation']['seed']))


    # If the data directory is specified, add it to the config, overwriting any
    # previous value
    if args.data_dir:
        config['Simulation']['data_dir'] = args.data_dir
    # If a directory wasn't listed in the config, use the default ('data')
    if not config.has_option(section='Simulation', option='data_dir'):
        config['Simulation']['data_dir'] = 'data'


    # If the data_dir already exists, append the current date and time to
    # data_dir, and use that. Afterwards, create the directory.
    if os.path.exists(config['Simulation']['data_dir']):
        newname = '{o}-{d}'.format(o=config['Simulation']['data_dir'],
                                   d=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        msg = '{d} already exists. Using {new} instead.'.format(d=config['Simulation']['data_dir'],
                                                                new=newname)
        warn(msg)
        config['Simulation']['data_dir'] = newname

    os.mkdir(config['Simulation']['data_dir'])


    # Write the configuration file
    configfile = os.path.join(config['Simulation']['data_dir'],
                              'configuration.cfg')
    write_configuration(config=config, filename=configfile)

    # TODO: use DictWriter
    writer = csv.writer(open(os.path.join(config['Simulation']['data_dir'], 'metapop.csv'), 'w'))
    writer.writerow(['Time', 'PopulationSize', 'ProducerProportion', 'MaxCooperatorFitness', 'MaxDefectorFitness'])

    # Create the migration topology. This is a graph where each population is a
    # node, and the edges between nodes represent potential paths for migration
    topology = build_topology(config=config)

    if config['Simulation'].getboolean('export_topology'):
        fn = os.path.join(config['Simulation']['data_dir'], 'topology.gml')
        export_topology(topology=topology, filename=fn)


    # Create the metapopulation and apply the initial stress bottleneck
    metapop = create_metapopulation(config=config, topology=topology)
    metapop = bottleneck(population=metapop,
                         survival_pct=float(config['Population']['mutation_rate_tolerance']))
    metapop = assign_fitness(M=metapop, config=config)

    # Keep track of the cumulative densities of each population
    densities = np.zeros(len(topology), dtype=np.int)

    try:
        environment_change = config['Simulation']['environment_change']
    except KeyError:
        environment_change = None


    # Keep track of how often the metapopulation should be mixed
    mix_frequency = int(config['Metapopulation']['mix_frequency'])

    # Keep track of the number of stress loci that affect fitness for each
    # population
    genome_lengths = np.repeat(int(config['Population']['genome_length_min']),
                               len(topology))

    stress_columns = stress_colnames(L=int(config['Population']['genome_length_max']))

    # Iterate through each cycle of the simulation
    for cycle in range(int(config['Simulation']['num_cycles'])):
        if not args.quiet:
            c1 = (metapop.loc[metapop.Coop==1, stress_columns] > 0).sum(axis=1).max()
            d1 = (metapop.loc[metapop.Coop==0, stress_columns] > 0).sum(axis=1).max()
            print("Cycle {c}: Size {ps}, Populations {pops}, {pc:.0%} cooperators, Fitness: {f:.02}, C1: {c1}, D1: {d1} ]".format(c=cycle, ps=metapop.shape[0], pops=metapop.Population.unique().shape[0], pc=metapop.Coop.mean(), f=metapop.Fitness.mean(), c1=c1, d1=d1))

        writer.writerow([cycle, metapop.shape[0], metapop.Coop.mean(), metapop[metapop.Coop==1].Fitness.max(), metapop[metapop.Coop==0].Fitness.max()])
        # Num cooperator 1s (P3.loc[P3.Coop==1, stress_columns] > 0).sum(axis=1)

        env_changed = False

        # Grow the population to carrying capacity, potentially mutating
        # offspring
        metapop = grow(M=metapop, genome_lengths=genome_lengths, config=config)

        # Migrate individuals among subpopulations
        metapop = migrate(M=metapop, topology=topology,
                          rate=float(config['Metapopulation']['migration_rate']))

        # Mix the metapopulation (if configured)
        if mix_frequency > 0 and cycle > 0 and (cycle % mix_frequency == 0):
            metapop = mix(M=metapop, topology=topology)

        densities += [metapop[metapop.Population==i].shape[0] for i in range(len(topology))]

        # Handle density based environmental change
        if environment_change == 'Metapopulation':
            if densities.sum() >= int(config['Metapopulation']['density_threshold']):
                metapop = reset_stress_loci(M=metapop, Lmax=int(config['Population']['genome_length_max']))
                metapop = assign_fitness(M=metapop, config=config)
                densities = np.zeros(len(topology), dtype=np.int)
                env_changed = True

        elif environment_change == 'Population':
            for p in np.where(densities > int(config['Population']['density_threshold'])):
                genome_lengths[p] = min(int(config['Population']['genome_length_max']),
                                        genome_lengths[p] + 1)
                densities[p] = 0

        # Dilution
        if not env_changed:
            metapop = bottleneck(population=metapop,
                                 survival_pct=float(config['Population']['dilution_factor']))

        if config['Simulation'].getboolean('stop_when_empty') and \
                metapop.shape[0] == 0:
            break


    # TODO: close up data files
    writer.writerow([cycle, metapop.shape[0], metapop.Coop.mean(),
                     metapop[metapop.Coop==1].Fitness.max(),
                     metapop[metapop.Coop==0].Fitness.max()])

#-------------------------------------------------------------------------

if __name__ == "__main__":
    main()
