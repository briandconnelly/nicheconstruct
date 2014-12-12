---
title: Methods

bibliography: references.bib
csl: evolutionary-ecology-research.csl

output:
  html_document:
    number_sections: no
    theme: default
    toc: yes
  pdf_document:
    number_sections: no
    toc: no
  word_document:
    number_sections: no
    toc: no
    fig_width: 5
    fig_height: 5

---

We develop a computational model to observe how the evolution of public goods production is affected as populations adapt to and modify their environment. Each simulation tracks a single metapopulation comprising $N^2$ sites, arranged as an $N×N$ bounded lattice, where each site can potentially hold a population. The genotype of each individual in these populations is a length $L+1$ string of digits, where $L_{min} \le L \le L_{max}$. Each locus in these genotypes is occupied by one of $A$ possible alleles. In several simulations, $A=1$, which results in genotypes that are binary bit strings. Alleles at the first $L$ loci determine the individual’s level of adaptation to the stressful environment. We refer to these loci as “stress loci”. An additional allele at the $(L+1)$<sup>th</sup> locus determines whether the individual is a producer (allele $1$) or a non-producer (allele $0$) of a public good. We refer to this locus as the “production locus”.


## Individual Fitness
A mutation from $0$ to any non-zero allele at the $i$<sup>th</sup> stress locus will improve individual fitness by $w_i$ despite the allelic states of other loci (i.e., there is no epistasis). We assume that $\{w_1, w_2, w_3, \ldots, w_L\}$ are independent and identically distributed (i.i.d.) random variables with $w_i \sim unif[w_{min}, w_{max}]$. For simplicity, all non-zero alleles carry the same fitness benefit. Public good production is costly, reducing individual fitness by $c$. Thus, if the allelic state of the $i$<sup>th</sup> locus is denoted $a_i$ with $a_i \in \{0, \ldots, A\}$, then the fitness of an individual is:

$$
W = z + \sum_{i=1}^{L} X(a_i) \cdot w_i - a_{L+1} c
$$

where $z$ is a baseline fitness (the fitness of an individual with zeros at every locus), and $X(a_i)$ indicates whether the allelic state $a_i$ is non-zero ($1$) or not ($0$). If there are no stress loci ($L=0$), the fitness of a producer and non-producer is $z-c$ and $z$, respectively.

**TODO: better name for $X()$**

## Overview of Basic Simulation Cycle

After initialization, simulations are run for $T$ cycles, where each cycle consists of population growth, mutation, migration, and dilution at each site in the metapopulation. During this process, populations can alter the environment as described later. We first detail each stage of this basic cycle.


### Population Growth

**TODO: There aren't $2^{L+1}$ genotypes, but $(A+1)^{L+1}$. How can this best be described?**

If $p$ is the proportion of producers in a population at the beginning of a growth cycle, then that population grows to the following size during the growth phase:

$$
S(p) = S_{min} + p (S_{max} - S_{min})
$$

Therefore, a population composed entirely of non-producers reaches a size of $S_{min}$, while a population with only producers reaches a size of $S_{max}$ (with $S_{max} \ge S_{min}$). The function $S(p)$ gauges the benefit of public good production as population size increases linearly with the proportion of producers. During population growth, competition occurs among the $2^{L+1}$ genotypes. Consider an arbitrary genotype $g$ (with $g \in \{1, 2, 3, \ldots, 2^{L+1}\}$). Let $n_g$ be the number of individuals with genotype $g$, and let $W_g$ be the fitness of genotype $g$ (see equation [1]). The composition of genotypes after population growth is multinomial with parameters $S(p)$ and $\{\pi_1, \pi_2, \ldots, \pi_{2^{L+1}}\}$, where

$$
\pi_g = \frac{n_g W_g}{\sum_{i=1}^{2^{L+1}} n_i W_i}
$$

Thus, $\pi_g$ is the probability that an individual in the population after growth has genotype $g$ (such that $\sum \pi_g = 1$).


### Mutation

For simplicity, we apply mutation after population growth. For every individual, allelic state changes occur independently at each stress locus with probability $\mu_{s}$, while the production locus changes allelic state with probability $\mu_{p}$. Thus, the probability that genotype $g$ mutates into genotype $g'$ is given by

$$
\tau_{g \rightarrow g'} = \mu_{s}^{H_{s}(g,~g')}(1-\mu_{s})^{\{L-H_{s}(g,~g')\}} \mu_{p}^{H_{p}(g,~g')} (1-\mu_{p})^{\{1-H_{p}(g,~g')\}}
$$

where $H_{s}(g,~g')$ and $H_{p}(g,~g')$ are the Hamming distances between genotypes $g$ and $g'$ at the stress loci and production locus, respectively. The Hamming distance is the number of loci at which allelic states differ. Because there is no inherent relationship among alleles, each of the $A + 1$ alleles is equally likely to arise via mutation at a given locus.


### Migration

Following mutation, migration occurs among populations. For each populated site, individuals move to an adjacent site with probability $m$. This adjacent site is randomly chosen with uniform probability from the source site's Moore neighborhood, which is composed of the nearest 8 sites on the lattice. Because the metapopulation lattice has boundaries, sites located on an edge have smaller neighborhoods.


### Dilution

After migration, populations are thinned to allow for growth in the next cycle. Each individual, despite its genotype, survives this bottleneck with probability $d$. The number of survivors for each genotype $g$ is sampled from a binomial distribution, where the number of trials is $n_g$ and the probability of success is $d$.


### Initialization

Metapopulations are initiated in a state that follows the onset of an environmental stress. First, populations are seeded at each site with producer proportion $p_{0}$ and grown to density $S(p_{0})$\. Each population is then subjected to a bottleneck. Individuals survive this event with probability $\mu_{t}$, which represents the likelihood that a mutation occurs that enables survival. Because individuals have not yet adapted to this new stress, the allelic state $a_{i}$ is set to $0$ at each stress locus. The fitness effects associated with adaptations at each locus $w_{i}$ are also sampled as previously described.


## Changing Environments and Niche Construction

Through growth and adaptation, populations can alter their environment. These changes can produce feedbacks that affect selection at the local or metapopulation level. We describe three ways in which populations are able to bring about environmental change.


### Niche Construction at the Metapopulation Level

First, we examine how the presence of organisms can reveal new avenues for adaptation. When $\tau_{m}$ total individuals have existed in the metapopulation, an environmental change is triggered at each site of the metapopulation as described in the previous section. Because populations containing producers are able to reach greater densities during each cycle, the presence of producers hastens these changes. For these simulations, genome lengths $L$ were held constant. Therefore, the amount of adaptation that could occur between environmental changes was limited. 

TODO: A=1, binary genotypes. Fixed genome length.


### Niche Construction at the Population Level

We also performed simulations in which environmental change was more likely to occur in populations which brought it about. Here, the space of genotypes within populations begins with genome length $L_{min}$. Once $\tau_{p}$ individuals have existed in a particular site, an environmental change occurs that increases the number of fitness-encoding loci in the genotype by one.

TODO: A=1, binary genotypes, varying genome length.


### Genotype-Mediated Niche Construction

The previous two methods described environmental change that was brought about simply by the presence of organisms. TODO



## Source Code and Software Versions

The simulation software and all configurations for the experiments reported are available at [https://github.com/briandconnelly/nicheconstruct/](https://github.com/briandconnelly/nicheconstruct/). Simulations were run using Python 2.7.3, NumPy 1.9.0, and NetworkX 1.9.1. Data analyses were performed using R 3.1.2 [@rproject]. Model parameters and their values are listed in [Table X](https://github.com/briandconnelly/nicheconstruct/blob/master/paper/table_of_parameters.md).

# References
