---
title: This is the name of my document
author: Brian D. Connelly
csl: /Users/bdc/Downloads/evolution.csl
latex_engine: xelatex
fontsize: 12pt
geometry: margin=1in
toc: true

references:
- id: fenner2012a
  title: One-click science marketing
  author:
  - family: Fenner
    given: Martin
  container-title: Nature Materials
  volume: 11
  DOI: 10.1038/nmat3283
  issue: 4
  publisher: Nature Publishing Group
  page: 261-263
  type: article-journal
  issued:
    year: 2012
    month: 3
...

hello there [@fenner2012a]

# Base Values

| Symbol | Parameter Description                   | Base Value    |
|--------|:----------------------------------------|:--------------|
| N^2^   | Number of Sites                         | 625           |
| L      | Number of Stress Loci                   | 8             |
| w~min~ | Minimum Fitness Effect Per Locus        | 0.45          |
| w~max~ | Maximum Fitness Effect Per Locus        | 0.55          |
| c      | Production Cost                         | 0.1           |
| z      | Baseline fitness                        | 1             |
| T      | Number of Simulation Cycles             | 3000          |
| S~min~ | Minimum Population Size                 | 800           |
| S~max~ | Maximum Population Size                 | 2000          |
| μ~s~   | Mutation Rate (Stress)                  | 10^-5^        |
| μ~p~   | Mutation Rate (Production)              | 10^-5^        |
| μ~t~   | Mutation Rate (Tolerance to New Stress) | 10^-5^        |
| m      | Migration Rate                          | 0.05          |
| d      | Dilution Factor                         | 0.1           |
| p~0~   | Initial Producer Proportion             | 0.5           |


# References
