# Base Values

| Symbol | Parameter Description                 | Base Value    |
|--------|:--------------------------------------|:--------------|
| L<sub>min</sub> | Minimum Number of Adaptive Loci | 3             |
| L<sub>max</sub> | Maximum Number of Adaptive Loci | 8             |
| &epsilon; | Niche construction effect          | x             |
| &delta; | Effect of non-zero allele (TODO)     | x             |
| a<sub>max</sub> | Potential alleles per locus  | x             |
| c      | Production Cost                       | 0.1           |
| z      | Baseline fitness                      | 1             |
| S<sub>min</sub>  | Minimum Population Size     | 800           |
| S<sub>max</sub>  | Maximum Population Size     | 2000          |
| w<sub>min</sub> | Minimum Fitness Effect Per Locus | 0.45          |
| w<sub>max</sub> | Maximum Fitness Effect Per Locus | 0.55          |
| T      | Number of Simulation Cycles           | 3000          |
| μ<sub>s</sub> | Mutation Rate (Stress)         | 10<sup>-5</sup> |
| μ<sub>p</sub>    | Mutation Rate (Production)  | 10<sup>-5</sup> |
| μ<sub>t</sub> | Mutation Rate (Tolerance to New Stress)  | 10<sup>-5</sup> |
| d      | Dilution Factor                       | 0.1           |
| N<sup>2</sup> | Number of Metapopulation Sites | 625           |
| m      | Migration Rate                        | 0.05          |
| p<sub>0</sub> | Initial Producer Proportion    | 0.5           |
| T      | Length of simulation                  | 3000          |

# TODO:
* Rate of new stress (for periodic)?
* Metapopulation density threshold
* Population density threshold
