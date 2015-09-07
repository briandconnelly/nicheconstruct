#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import datetime
import os
import signal
import sys
from time import time
import uuid
from warnings import warn

from configobj import ConfigObj, ConfigObjError, flatten_errors
from validate import Validator

from logfile import write_metapop_data, write_population_data, write_population_genotypes
from Metapopulation import *
from misc import *
from Topology import *

__version__ = '1.0.3'


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


def ncsimulate():
    """Run a simulation"""

    start_time = time()

    # Print a status message when SIGINFO (ctrl-T) is received on BSD or
    # OS X systems or SIGUSR1 is received on POSIX systems
    def handle_siginfo(signum, frame):
        try:
            print("Cycle {c}".format(c=cycle))
        except NameError:
            print("Simulation has not yet begun")

    signal.signal(signal.SIGUSR1, handle_siginfo)
    if hasattr(signal, 'SIGINFO'):
        signal.signal(signal.SIGINFO, handle_siginfo)

    # Some scheduling systems send SIGTERM before killing a job. If SIGTERM
    # is received, flush all of the log files
    def handle_sigterm(signum, frame):
        try:
            if log_metapopulation:
                outfilemp.flush()
            if log_population:
                outfilep.flush()
            if log_genotypes:
                outfileg.flush()
        except NameError:
            pass
    signal.signal(signal.SIGTERM, handle_sigterm)


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
        print("No errors found in configuration file {f}".format(f=args.configfile))
        sys.exit(0)

    # If the random number generator seed specified, add it to the config,
    # overwriting any previous value. Otherwise, if it wasn't in the
    # supplied configuration file, create one.
    if args.seed:
        config['Simulation']['seed'] = args.seed
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
                      'MaxDefectorFitness', 'MeanDefectorFitness',
                      'ShannonIndex', 'SimpsonIndex']

        outfilemp = open(os.path.join(config['Simulation']['data_dir'],
                         config['MetapopulationLog']['filename']), 'w')
        writermp = csv.DictWriter(outfilemp, fieldnames=fieldnames)
        writermp.writeheader()


    # Create the log file of population-level data if enabled
    log_population = config['PopulationLog']['enabled']
    if log_population:
        log_population_freq = config['PopulationLog']['frequency']

        # Config options for logging population. Name, frequency, etc.
        fieldnames = ['Time', 'Population', 'X', 'Y', 'PopulationSize',
                      'CooperatorProportion', 'MinCooperatorFitness',
                      'MaxCooperatorFitness', 'MeanCooperatorFitness',
                      'MinDefectorFitness', 'MaxDefectorFitness',
                      'MeanDefectorFitness', 'ShannonIndex', 'SimpsonIndex']

        outfilep = open(os.path.join(config['Simulation']['data_dir'],
                        config['PopulationLog']['filename']), 'w')
        writerp = csv.DictWriter(outfilep, fieldnames=fieldnames)
        writerp.writeheader()

    log_genotypes = config['GenotypeLog']['enabled']
    if log_genotypes:
        log_genotypes_freq = config['GenotypeLog']['frequency']
        fieldnames = ['Time', 'Population', 'X', 'Y', 'Genotype']

        outfileg = open(os.path.join(config['Simulation']['data_dir'],
                        config['GenotypeLog']['filename']), 'w')
        writerg = csv.DictWriter(outfileg, fieldnames=fieldnames)
        writerg.writeheader()


    # Create the migration topology. This is a graph where each population is a
    # node, and the edges between nodes represent potential paths for migration
    topology = build_topology(config=config)

    if config['Simulation']['export_topology']:
        fn = os.path.join(config['Simulation']['data_dir'], 'topology.gml')
        export_topology(topology=topology, filename=fn)


    # Create the metapopulation and apply the initial stress bottleneck
    metapop = create_metapopulation(config=config, topology=topology,
                                    initial_state=config['Metapopulation']['initial_state'])

    stress_tolerance = config['Population']['mutation_rate_tolerance']
    if stress_tolerance < 1:
        metapop = bottleneck(population=metapop,
                             survival_pct=config['Population']['mutation_rate_tolerance'])
    else:
        metapop = bottleneck(population=metapop,
                             survival_pct=config['Population']['dilution_factor'])


    # Keep track of how often the metapopulation should be mixed
    mix_frequency = config['Metapopulation']['mix_frequency']

    adaptive_columns = adaptive_colnames(L=config['Population']['genome_length'])

    # Iterate through each cycle of the simulation
    for cycle in range(config['Simulation']['num_cycles']):
        if not args.quiet:
            if len(adaptive_columns) > 0:
                c1 = (metapop.loc[metapop.Coop==1, adaptive_columns] > 0).sum(axis=1).max()
                d1 = (metapop.loc[metapop.Coop==0, adaptive_columns] > 0).sum(axis=1).max()
            else:
                c1 = d1 = 'NA'

            print("Cycle {c}: Size {ps}, Populations {pops}, {pc:.0%} cooperators, Fitness: {f:.02}, C1: {c1}, D1: {d1} ]".format(c=cycle, ps=metapop.shape[0], pops=metapop.Population.unique().shape[0], pc=metapop.Coop.mean(), f=metapop.Fitness.mean(), c1=c1, d1=d1))

        if log_metapopulation and cycle % log_metapopulation_freq == 0:
            write_metapop_data(writer=writermp, metapop=metapop,
                               topology=topology, cycle=cycle, config=config)

        if log_population and cycle % log_population_freq == 0:
            write_population_data(writer=writerp, metapop=metapop,
                                  topology=topology, cycle=cycle, config=config)

        if log_genotypes and cycle % log_genotypes_freq == 0:
            write_population_genotypes(writer=writerg, metapop=metapop,
                                       topology=topology, cycle=cycle,
                                       config=config)


        # Grow the population to carrying capacity, potentially mutating
        # offspring
        metapop = grow(M=metapop, config=config)

        # Migrate individuals among subpopulations
        metapop = migrate(M=metapop, topology=topology,
                          rate=config['Metapopulation']['migration_rate'])

        # Mix the metapopulation (if configured)
        if mix_frequency > 0 and cycle > 0 and (cycle % mix_frequency == 0):
            metapop = mix(M=metapop, topology=topology)

        # Dilution
        metapop = bottleneck(population=metapop,
                             survival_pct=config['Population']['dilution_factor'])

        if config['Simulation']['stop_when_empty'] and \
                metapop.shape[0] == 0:
            break


    if log_metapopulation:
        write_metapop_data(writer=writermp, metapop=metapop, topology=topology,
                           cycle=cycle+1, config=config)
    if log_population:
        write_population_data(writer=writerp, metapop=metapop,
                              topology=topology, cycle=cycle, config=config)

    rt_string = 'Run Time: {t}'.format(t=datetime.timedelta(seconds=time()-start_time))
    append_run_information(filename=infofile, string=rt_string)

#-------------------------------------------------------------------------

if __name__ == "__main__":
    ncsimulate()

