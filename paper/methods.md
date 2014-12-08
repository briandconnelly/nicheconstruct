# Methods

A computational model was developed to observe how the evolution of public goods production was affected as populations adapted to and modified their environment. Each simulation tracks a single metapopulation comprising $N^2$, arranged as an $N×N$ bounded lattice, where each site on this lattice could potentially hold a population. Populations consist of individuals, where the genotype of each individual is a length $L+1$ string of digits, where $L_{min} \le L \le L_{max}$. Each locus in these genotypes is occupied by one of $A$ possible alleles. Alleles at the first $L$ loci determine the individual’s level of adaptation to the environment. We refer to these loci as “adaptive loci.” The allele at the $(L+1)$<sup>th</sup> locus determines whether the individual is a producer (allele $1$) or a non-producer (allele $0$) of a public good. We refer to this locus as the “production locus.”

## Individual fitness
# TODO: update for non-binary - there can be some epistasis
A mutation from $0$ to a non-zero at the $i$<sup>th</sup> adaptive locus will improve individual fitness by $w_i$ despite the allelic states of other loci (i.e., there is no epistasis). We assume that $\{w_1, w_2, w_3, \ldots, w_L\}$ are independent and identically distributed (i.i.d.) random variables with $w_i \sim unif[w_{min}, w_{max}]$. Public good production is costly, reducing individual fitness by $c$. Thus, if the allelic state of the $i$<sup>th</sup> locus is denoted $a_i$ (with $a_i \in \{0 \ldots A\}$), then the fitness of an individual is:

$$
W = z + \sum_{i=1}^{L} a_i w_i - a_{L+1} c
$$

where $z$ is a baseline fitness (the fitness of an individual with zeros at every locus). If there are no adaptive loci ($L=0$), the fitness of a producer and non-producer is $z-c$ and $z$, respectively.


## Overview of basic simulation cycle

Each simulation is run for $T$ cycles. Each cycle consists of population growth, mutation, migration, and dilution. During this process, populations can alter the environment in the ways described later. We first outline each stage of this basic cycle.

### Population Growth

If $p$ is the proportion of producers in a population at the beginning of a growth cycle, then that population grows to the following size over the growth cycle:

$$
S(p) = S_{min} + (S_{max} - S_{min}) p
$$

Therefore, a population with solely non-producers reaches a size of $S_{min}$, while a population with only producers reaches a size of $S_{max}$ (with $S_{max} \ge S_{min}$). The function $S(p)$ gauges the benefit of public good production, as population size increases linearly with the proportion of producers. During population growth, competition occurs among the $2^{L+1}$ genotypes. Consider an arbitrary genotype $g$ (with $g \in \{1, 2, 3, \ldots, 2^{L+1}\}$). Let $n_g$ be the number of individuals with genotype $g$, and let $W_g$ be the fitness of genotype $g$ (see equation [1]). The composition of genotypes after population growth is multinomial with parameters $S(p)$ and $\{\pi_1, \pi_2, \ldots, \pi_{2^{L+1}}\}$, where

$$
\pi_g = \frac{n_g W_g}{\sum_{i=1}^{2^{L+1}} n_i W_i}
$$

Thus, $\pi_g$ is the probability that an individual in the population after growth is genotype $g$ (such that $\sum \pi_g = 1$). Population growth occurs at each occupied site in the metapopulation.


### Mutation

For simplicity, we apply mutation after population growth. For each individual, every locus mutates independently. Each adaptive locus changes allelic state with probability $\mu_{s}$ while the production locus changes allelic state with probability $\mu_{p}$. Thus, the probability that genotype $g$ mutates into genotype $g'$ is given by

$$
\tau_{g \rightarrow g'} = \mu_{s}^{H_{s}(g,~g')}(1-\mu_{s})^{\{L-H_{s}(g,~g')\}} \mu_{p}^{H_{p}(g,~g')} (1-\mu_{p})^{\{1-H_{p}(g,~g')\}}
$$

where $H_{s}(g,~g')$ and $H_{p}(g,~g')$ are the Hamming distances between genotypes $g$ and $g'$ at the stress loci and production locus, respectively. The Hamming distance between two genotypes in this model is the number of loci at differing allelic states.

TODO describe how one allele can change (0->1 or 1->5)


### Migration

Following mutation, migration of individuals occurs among populations. For each populated site, an adjacent site in its Moore neighborhood (the 8 nearest sites on the lattice) is randomly chosen with uniform probability. Note, the metapopulation lattice has boundaries, thus sites on the edge of the metapopulation have fewer adjacent sites than those in the interior. Every individual in the focal site moves to the selected adjacent site with probability $m$.


### Dilution

Following migration, populations are thinned to allow for growth in the next cycle. Each individual, despite its genotype, survives this bottleneck with probability $d$.


## Adaptation to New Environments

The emergence of an environmental stress subjects populations to an additional bottleneck. Individuals survive this event with probability $\mu_{t}$, which represents the likelihood that a mutation occurs, engendering survival in the new environment. Because individuals are not adapted to this new stress, the allelic state $a_{i}$ is set to $0$ at each adaptive locus. The fitness effects associated with adaptations at each locus $w_{i}$ are also resampled as previously described. Note that this change in environment removes the influence of any previous stress. Simulations begin by applying this process to full populations initiated at each site with producer proportion $p_{0}$. We examined how the emergence of these new environments, when brought about by populations in the different means below, affected the evolution and maintenance of public good production. We examined how these environmental changes, when brought about by populations in the different ways described below, affected the evolution and maintenance of public good production.


### Niche Construction at the Metapopulation Level

First, we examine how the presence of organisms can reveal new avenues for adaptation. When $\tau_{m}$ total individuals have existed in the metapopulation, an environmental change is triggered at each site of the metapopulation as described in the previous section. Because populations containing producers are able to reach greater densities during each cycle, the presence of producers hastens these changes. For these simulations, genome lengths $L$ were held constant. Therefore, the amount of adaptation that could occur between environmental changes was limited. 

TODO: A=1, binary genotypes


### Niche Construction at the Population Level

We also performed simulations in which environmental change was more likely to occur in populations which brought it about. Here, the space of genotypes within populations begins with genome length $L_{min}$. Once $\tau_{p}$ individuals have existed in a particular site, an environmental change occurs that increases the number of fitness-encoding loci in the genotype by one.

TODO: A=1, binary genotypes


### Genotype-Mediated Niche Construction

The previous two methods described environmental change that was brought about simply by the presence of organisms. TODO



## Source Code and Software Versions

The simulation software and all configurations for the experiments reported are available at TODO. Simulations were run using Python 2.7.3, NumPy 1.9.0, and NetworkX 1.9.1. Data analyses were performed using R 3.1.2. Model parameters and their values are listed in [Table X](https://github.com/briandconnelly/nicheconstruct/blob/master/paper/table_of_parameters.md).
