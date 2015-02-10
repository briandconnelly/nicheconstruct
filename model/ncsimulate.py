#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import datetime
import os
import sys
import uuid
from warnings import warn

from configobj import ConfigObj, ConfigObjError, flatten_errors
from validate import Validator

from Metapopulation import *
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
                        dest='configfile')
    parser.add_argument('--checkconfig', '-C', action='store_true',
                        default=False,
                        help='Check the given configuration file and quit (note: includes parameters specified with --param')
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


def write_metapop_data(writer, metapop, cycle):
    """Write information about the metapopulation to a CSV writer"""
    metapop_data = {'Time': cycle,
                    'PopulationSize': metapop.shape[0],
                    'CooperatorProportion': metapop.Coop.mean(),
                    'MinCooperatorFitness': metapop[metapop.Coop==1].Fitness.min(),
                    'MaxCooperatorFitness': metapop[metapop.Coop==1].Fitness.max(),
                    'MeanCooperatorFitness': metapop[metapop.Coop==1].Fitness.mean(),
                    'MinDefectorFitness': metapop[metapop.Coop==0].Fitness.min(),
                    'MaxDefectorFitness': metapop[metapop.Coop==0].Fitness.max(),
                    'MeanDefectorFitness': metapop[metapop.Coop==0].Fitness.mean()}
    writer.writerow(metapop_data)


def main():
    """Run a simulation"""

    # Get the command line arguments
    args = parse_arguments()

    # Read the configuration file
    try:
        config = ConfigObj(infile=args.configfile, configspec='configspec.ini',
                           file_error=True)
    except (ConfigObjError, OSError) as e:
        print("Error: {e}".format(e=e))
        sys.exit(1)

    # Add any parameters specified on the command line to the configuration
    if args.param:
        for param in args.param:
            config[param[0]][param[1]] = param[2]

    # Validate the configuration
    validation = config.validate(Validator(), copy=True)

    if validation != True:
        errors = flatten_errors(config, validation)
        print("Found {n} error(s) in configuration:".format(n=len(errors)))
        for (section_list, key, _) in errors:
            if key is not None:
                print("\t* Invalid value for '{k}' in Section '{s}'".format(k=key, s=section_list[0]))
            else:
                print("\t* Missing required section '{s}'".format(s=section_list[0]))

        sys.exit(2)


    if args.checkconfig:
        print("No errors found in configuration file {f}".format(f=args.configfile.name))
        sys.exit(0)

    # If the random number generator seed specified, add it to the config,
    # overwriting any previous value. Otherwise, if it wasn't in the
    # supplied configuration file, create one.
    if args.seed:
        config['Simulation']['seed'] = args.seed
    #elif not config.has_option(section='Simulation', option='seed'):
    elif 'seed' not in config['Simulation'] or config['Simulation']['seed']==None:
        seed = np.random.randint(low=0, high=np.iinfo(np.uint32).max)           
        config['Simulation']['seed'] = seed

    np.random.seed(seed=config['Simulation']['seed'])

    # Generate a universally unique identifier (UUID) for this run
    config['Simulation']['UUID'] = str(uuid.uuid4())

    # If the data directory is specified, add it to the config, overwriting any
    # previous value
    if args.data_dir:
        config['Simulation']['data_dir'] = args.data_dir


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

    # Write information about the run
    infofile = os.path.join(config['Simulation']['data_dir'], 'run_info.txt')
    write_run_information(filename=infofile, config=config)


    # Write the configuration file
    config.filename = os.path.join(config['Simulation']['data_dir'],
                                   'configuration.cfg')
    config.write()


    # Create the log file of metapopulation-level data if enabled
    log_metapopulation = config['MetapopulationLog']['enabled']
    if log_metapopulation:
        log_metapopulation_freq = config['MetapopulationLog']['frequency']

        # Config options for logging metapopulation. Name, frequency, etc.
        fieldnames = ['Time', 'PopulationSize', 'CooperatorProportion',
                      'MinCooperatorFitness', 'MaxCooperatorFitness',
                      'MeanCooperatorFitness', 'MinDefectorFitness',
                      'MaxDefectorFitness', 'MeanDefectorFitness']
        writermp = csv.DictWriter(open(os.path.join(config['Simulation']['data_dir'],
                                       'metapopulation.csv'), 'w'),
                                       fieldnames=fieldnames)
        writermp.writeheader()


    # Create the migration topology. This is a graph where each population is a
    # node, and the edges between nodes represent potential paths for migration
    topology = build_topology(config=config)

    if config['Simulation']['export_topology']:
        fn = os.path.join(config['Simulation']['data_dir'], 'topology.gml')
        export_topology(topology=topology, filename=fn)


    # Create the metapopulation and apply the initial stress bottleneck
    metapop = create_metapopulation(config=config, topology=topology)
    metapop = bottleneck(population=metapop,
                         survival_pct=config['Population']['mutation_rate_tolerance'])

    # Keep track of the cumulative densities of each population
    densities = np.zeros(len(topology), dtype=np.int)

    try:
        environment_change = config['Simulation']['environment_change']
    except KeyError:
        environment_change = None


    # Keep track of how often the metapopulation should be mixed
    mix_frequency = config['Metapopulation']['mix_frequency']

    # Keep track of the number of stress loci that affect fitness for each
    # population
    genome_lengths = np.repeat(config['Population']['genome_length_min'],
                               len(topology))

    stress_columns = stress_colnames(L=config['Population']['genome_length_max'])

    # Iterate through each cycle of the simulation
    for cycle in range(config['Simulation']['num_cycles']):
        if not args.quiet:
            if len(stress_columns) > 0:
                c1 = (metapop.loc[metapop.Coop==1, stress_columns] > 0).sum(axis=1).max()
                d1 = (metapop.loc[metapop.Coop==0, stress_columns] > 0).sum(axis=1).max()
            else:
                c1 = d1 = 'NA'

            print("Cycle {c}: Size {ps}, Populations {pops}, {pc:.0%} cooperators, Fitness: {f:.02}, C1: {c1}, D1: {d1} ]".format(c=cycle, ps=metapop.shape[0], pops=metapop.Population.unique().shape[0], pc=metapop.Coop.mean(), f=metapop.Fitness.mean(), c1=c1, d1=d1))

        if log_metapopulation and cycle % log_metapopulation_freq == 0:
            write_metapop_data(writer=writermp, metapop=metapop, cycle=cycle)

        env_changed = False

        # Grow the population to carrying capacity, potentially mutating
        # offspring
        metapop = grow(M=metapop, genome_lengths=genome_lengths, config=config)

        # Migrate individuals among subpopulations
        metapop = migrate(M=metapop, topology=topology,
                          rate=config['Metapopulation']['migration_rate'])

        # Mix the metapopulation (if configured)
        if mix_frequency > 0 and cycle > 0 and (cycle % mix_frequency == 0):
            metapop = mix(M=metapop, topology=topology)

        # Handle density based environmental change
        for popid, groupfitness in metapop.groupby('Population').Fitness:
            densities[popid] += groupfitness.count()

        if environment_change == 'Metapopulation':
            if densities.sum() >= config['Metapopulation']['density_threshold']:
                metapop = reset_stress_loci(M=metapop, Lmax=config['Population']['genome_length_max'])
                metapop = assign_fitness(P=metapop, config=config)
                densities = np.zeros(len(topology), dtype=np.int)
                env_changed = True

        elif environment_change == 'Population':
            for p in np.where(densities > config['Population']['density_threshold']):
                genome_lengths[p] = min(config['Population']['genome_length_max'],
                                        genome_lengths[p] + 1)
                densities[p] = 0

        # Dilution
        if not env_changed:
            metapop = bottleneck(population=metapop,
                                 survival_pct=config['Population']['dilution_factor'])

        if config['Simulation']['stop_when_empty'] and \
                metapop.shape[0] == 0:
            break


    if log_metapopulation:
        write_metapop_data(writer=writermp, metapop=metapop, cycle=cycle+1)

#-------------------------------------------------------------------------

if __name__ == "__main__":
    main()
