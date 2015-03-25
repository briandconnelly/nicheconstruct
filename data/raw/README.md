Raw data from simulations

Each directory contains the output from one replicate simulation of a treatment. The treatment is specified in the prefix (see table below), and the replicate ID is appended.

| Prefix                     | Description                                    |
|:---------------------------|:-----------------------------------------------|
| data_L05_A06_1xDelta_1xEpsilon | Base run                                   |
| data_L05_A06_2xDelta_0xEpsilon | Adaptations, no niche construction (adaptive benefit doubled) |


## Contents

Each directory contains these three files:

* **configuration.cfg**: A configuration file to re-create that simulation (includes random number seed)
* **metapopulation.csv**: Information about the state of the metapopulation (e.g., proportion of cooperators, diversity) during the simulation
* **run_info.txt**: Information about where, when, and how the simulation was run

