# Niche Construction Model

## Dependiencies

* Python 2.7 or 3.4
* [Pandas](http://pandas.pydata.org) 0.15.2
* [NetworkX](https://networkx.github.io/) 1.9.1
* [NumPy](http://www.numpy.org) 1.9.1
* [ConfigObj](https://pypi.python.org/pypi/configobj/) 5.0.6

These dependencies can be installed in a modern Python environment using:

```sh
pip install numpy==1.9.1 pandas==0.15.2 networkx==1.9.1 configobj==5.0.6
```

## Virtual Environment

TODO

## Running the Model

Simulations using this model are run using the `ncsimulate.py` script. To see
what options can be provided to `ncsimulate.py`, run it with the `--help`
argument:

```sh
python ncsimulate.py --help
```
```
usage: ncsimulate.ph [-h] [--config FILE] [--data_dir DIR]
                     [--param SECTION NAME VALUE] [--seed S] [--quiet]
                     [--version]

Run a simluation

optional arguments:
-h, --help            show this help message and exit
--config FILE, -c FILE
Configuration file to use (default: run.cfg)
--data_dir DIR, -d DIR
Directory to store data (default: data)
--param SECTION NAME VALUE, -p SECTION NAME VALUE
Set a parameter value
--seed S, -s S        Set the pseudorandom number generator seed
--quiet, -q           Suppress output messages
--version             show program's version number and exit

```

## Configuring the Model

The parameters for the model are specified in the `run.cfg` file. Alternate
configuration files can be used with the `--config` argument to
`ncsimulate.py`:

```sh
python ncsimulate.py --config other_config.cfg
```

Additionally, parameter values can be set from the command line with the
`--param` argument. For example, to use the configuration `run.cfg`, but
set the simulation to run for 10 cycles:

```sh
python ncsimulate.py --param Simulation num_cycles 10
```

### The Configuration File

TODO

## Result Data

TODO
