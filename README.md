# Genetic Niche Hiking Model

## Dependiencies

* Python 2.7
* [NumPy](http://www.numpy.org) 1.8.0 or later
* [NetworkX](https://networkx.github.io/)


## Running the Model

Simulations using this model are run using the `niche_hike.py` script. To see
what options can be provided to `niche_hike.py`, run it with the `--help`
argument:

```sh
python niche_hike.py --help
```
```
usage: niche_hike.ph [-h] [--config FILE] [--data_dir DIR]
                     [--param SECTION NAME VALUE] [--seed S] [--quiet]
                     [--version]

Run a GNH simluation

optional arguments:
-h, --help            show this help message and exit
--config FILE, -c FILE
Configuration file to use (default: gnh.cfg)
--data_dir DIR, -d DIR
Directory to store data (default: data)
--param SECTION NAME VALUE, -p SECTION NAME VALUE
Set a parameter value
--seed S, -s S        Set the pseudorandom number generator seed
--quiet, -q           Suppress output messages
--version             show program's version number and exit

```

## Configuring the Model

The parameters for the model are specified in the `gnh.cfg` file. Alternate
configuration files can be used with the `--config` argument to
`night_hike.py`:

```sh
python niche_hike.py --config other_config.cfg
```

Additionally, parameter values can be set from the command line with the
`--param` argument. For example, to use the configuration `gnh.cfg`, but
set the simulation to run for 10 cycles:

```sh
python niche_hike.py --param Simulation num_cycles 10
```

### The Configuration File

TODO

## Result Data

### Uncompressing the Data Files

To save space, the resulting data files are compressed. To open these files in Python:

```python
import bz2
import csv

reader = csv.reader(bz2.BZ2File('demographics.csv.bz2', 'r'))
for row in reader:
    print(row)
```

The decompression is done transparently in R:

```r
mydata <- read.csv('demographics.csv.bz2')
```

Otherwise, they can be opened by double clicking on them in Finder (Mac),
running bunzip2 (Mac/Linux), or opening with [7-Zip](http://www.7-zip.org/)
(Windows).
