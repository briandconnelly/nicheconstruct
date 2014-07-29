#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import ConfigParser
import datetime
import os
import shutil
import sys

import numpy as np

import Metapopulation

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run a GNH simluation')
    parser.add_argument('--config', '-c', metavar='FILE', help='Configuration '\
                        'file to use (default: gnh.cfg)', default='gnh.cfg',
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
    args = parser.parse_args()

    return args


def main():
    # Get the command line arguments
    args = parse_arguments()

    # Read the configuration file
    config = ConfigParser.SafeConfigParser()
    config.readfp(args.configfile)
    args.configfile.close()

    # Add any parameters specified on the command line to the configuration
    if args.param:
        for p in args.param:
            config.set(section=p[0], option=p[1], value=p[2])

    # If the random number generator seed specified, add it to the config,
    # overwriting any previous value. Otherwise, if it wasn't in the 
    # supplied configuration file, create one.
    if args.seed:
        config.set(section='Simulation', option='seed', value=str(args.seed))
    elif config.has_option(section='Simulation', option='seed') is not True:
        seed = np.random.randint(low=0, high=np.iinfo(np.int).max)
        config.set(section='Simulation', option='seed', value=str(seed))

    # Set the seed for the pseudorandom number generator
    if config.has_option(section='Simulation', option='seed'):
        np.random.seed(seed=config.getint(section='Simulation', option='seed'))


    # If the data directory is specified, add it to the config, overwriting any
    # previous value
    if args.data_dir:
        config.set(section='Simulation', option='data_dir', value=args.data_dir)

    if config.has_option(section='Simulation', option='data_dir'):
        data_dir = config.get(section='Simulation', option='data_dir')
    else:
        config.set(section='Simulation', option='data_dir', value='data')
        data_dir = 'data'

    # If the data directory already exists, rename it to data_dir with the
    # current date and time appended to it. Then create the data dir.
    if os.path.exists(data_dir):
        newname = data_dir + '-' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        shutil.move(data_dir, newname)
        print('Moved previous data directory to {d}'.format(d=newname))

    os.mkdir(data_dir)


    # Write the configuration file
    cfg_out = os.path.join(data_dir, 'configuration.cfg')
    with open(cfg_out, 'wb') as configfile:
        info = "# GNH Configuration\n# Generated: {when}\n# Command: "\
                "{cmd}\n\n".format(when=datetime.datetime.now().isoformat(),
                                   cmd=' '.join(sys.argv))

        configfile.write(info)
        config.write(configfile)


    m = Metapopulation.Metapopulation(config=config)

    for t in range(config.getint(section='Simulation', option='num_cycles')):
        m.migrate()
        m.cycle()

        if not args.quiet:
            msg = "[{t}] Size: {s}, Producers: {p:.1%}".format(t=t, s=len(m), p=m.prop_producers())
            print(msg)


if __name__ == "__main__":
    main()

