# The Model

## Dependiencies

The following software versions were used for this work:

* Python 3.4
* [Pandas](http://pandas.pydata.org) 0.15.2
* [NetworkX](https://networkx.github.io/) 1.9.1
* [NumPy](http://www.numpy.org) 1.9.1
* [ConfigObj](https://pypi.python.org/pypi/configobj/) 5.0.6

These dependencies can be installed in a modern Python environment using:

```sh
pip3 install numpy==1.9.1 pandas==0.15.2 networkx==1.9.1 configobj==5.0.6
```

Or using the included [requirements.txt](requirements.txt) file:

```sh
pip3 install -r requirements.txt
```

The model also must be run on a machine with a 64-bit processor and operating system.


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

By default, the model uses the configuration specified in `run.cfg`. Alternate
configuration files can be specified with the `--config` option.

In the configuration file, parameters are separated into sections based on what
they affect.

| Section        | Description                                                                            |
|:---------------|:---------------------------------------------------------------------------------------|
| Simulation     | Properties of the simulation (e.g., length, data directory)                            |
| Metapopulation | Metapopulation properties including how patches are arranged and migration rate        |
| Population     | Population-level properties including mutation rates, patch sizes, and fitness effects |

Aside from these three main sections, additional sections contain parameters
for the specific metapopulation topology used and output files.

| Section            | Description                                                                            |
|:-------------------|:---------------------------------------------------------------------------------------|
| MooreTopology      | Configuration for lattice topologies with 8 neighboring patches                        |
| VonNeumannTopology | Configuration for lattice topologies with 4 neighboring patches                        |
| SmallWorldTopology | Configuration for topologies arranged as a small world network                         |
| CompleteTopology   | Configuration for topologies arranged as a complete graph (all patches connected)      |
| RegularTopology    | Configuration for topologies arranged as an R-regular graph (all patches have R neighbors) |


| Section            | Description                                                                            |
|:-------------------|:---------------------------------------------------------------------------------------|
| MetapopulationLog  | Configure how metapopulation-level data are recorded                                   |
| PopulationLog      | Configure how population-level data are recorded                                       |
| GenotypeLog        | Configure how data about the dominant genotypes in each population are recorded        |


## Result Data

Unless otherwise specified using the `--data_dir` argument or in the configuration file, data are written in the `data` directory.


| Data File            | Description                                             | Configuration              | 
|:---------------------|:--------------------------------------------------------|---------------------------:| 
| `run_info.txt`       | Information about where and when the simulation was run | Always Created             | 
| `configuration.cfg`  | A configuration file allowing this run to be reproduced | Always Created             | 
| `topology.gml`       | The topology of the metapopulation                      | Simulation/export_topology |
| `metapopulation.csv` | Metapopulation-level information (e.g., fitness)        | MetapopulationLog Section  |
| `population.csv`     | Population-level information                            | PopulationLog Section      |
| `genotypes.csv`      | Dominant genotypes in each population                   | GenotypeLog section        |

