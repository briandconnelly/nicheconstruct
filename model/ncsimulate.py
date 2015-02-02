#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import SafeConfigParser
import argparse
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

    # TODO: open up the data files for logging and write headers


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

    # Keep track of the cumulative densities of each population
    densities = pd.DataFrame(columns=['Cycle', 'Population', 'Density'])

    # Keep track of how often the metapopulation should be mixed
    mix_frequency = int(config['Metapopulation']['mix_frequency'])

    # Keep track of the number of stress loci that affect fitness for each
    # population
    genome_lengths = np.repeat(int(config['Population']['genome_length_min']),
                               len(topology))


    # Iterate through each cycle of the simulation
    for cycle in range(int(config['Simulation']['num_cycles'])):
        if not args.quiet:
            print("Cycle",cycle)

        # TODO: write data

        env_changed = False

        # Grow the population to carrying capacity, potentially mutating
        # offspring
        metapop = grow(M=metapop, genome_lengths=genome_lengths, config=config)

        # Mutate individuals in the population - do this if all individuals can acquire mutations
        #metapop = mutate(M=metapop,
        #                 mu_stress=float(config['Population']['mutation_rate_stress']),
        #                 mu_cooperation=float(config['Population']['mutation_rate_cooperation']),
        #                 Lmax=int(config['Population']['genome_length_max']),
        #                 stress_alleles=float(config['Population']['stress_alleles']))

        # Migrate individuals among subpopulations
        metapop = migrate(M=metapop, topology=topology,
                          rate=float(config['Metapopulation']['migration_rate']))

        # Mix the metapopulation (if configured)
        if mix_frequency > 0 and cycle > 0 and (cycle % mix_frequency == 0):
            metapop = mix(M=metapop, topology=topology)

        # TODO: update the count of densities.
            # - DataFrame with per-population densities (metapop info is the sum)
        # TODO:   environmental change (metapop or pop level)

        # Dilution
        if not env_changed:
            metapop = bottleneck(population=metapop,
                                 survival_pct=float(config['Population']['dilution_factor']))

        if config['Simulation'].getboolean('stop_when_empty') and \
                metapop.shape[0] == 0:
            break


    # TODO: write final data
    # TODO: close up

#-------------------------------------------------------------------------

if __name__ == "__main__":
    main()
