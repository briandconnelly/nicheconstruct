#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Run a niche construction / niche hiking simulation"""

import argparse
import datetime
import os
from warnings import warn

try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser

from Simulation import Simulation

__version__ = '0.2.1'


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
            config.set(section=param[0], option=param[1], value=param[2])

    # If the random number generator seed specified, add it to the config,
    # overwriting any previous value. Otherwise, if it wasn't in the
    # supplied configuration file, create one.
    if args.seed:
        config.set(section='Simulation', option='seed', value=str(args.seed))

    # If the data directory is specified, add it to the config, overwriting any
    # previous value
    if args.data_dir:
        config.set(section='Simulation', option='data_dir',
                   value=args.data_dir)

    # If a directory wasn't listed in the config, use the default ('data')
    if not config.has_option(section='Simulation', option='data_dir'):
        config.set(section='Simulation', option='data_dir', value='data')

    data_dir = config.get(section='Simulation', option='data_dir')

    # If the data_dir already exists, append the current date and time to
    # data_dir, and use that. Afterwards, create the directory.
    if os.path.exists(data_dir):
        newname = '{o}-{d}'.format(o=data_dir,
                                   d=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        msg = '{d} already exists. Using {new} instead.'.format(d=data_dir,
                                                                new=newname)
        warn(msg)
        config.set(section='Simulation', option='data_dir', value=newname)

    # Create the simulation object and iterate through the timesteps
    for step in Simulation(config=config):
        if not args.quiet:
            print(step.statusbar())


if __name__ == "__main__":
    main()

