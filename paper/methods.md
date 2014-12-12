---
title: "Methods"
csl: evolutionary-ecology-research.csl
output:
  pdf_document:
    number_sections: no
    toc: no
  html_document:
    number_sections: no
    theme: default
    toc: yes
  word_document:
    fig_height: 5
    fig_width: 5
    number_sections: no
    toc: no
bibliography: references.bib
---

We develop a computational model to observe how the evolution of public goods production is affected as populations adapt to and modify their environment. Each simulation tracks a single metapopulation comprising $N^2$ sites, arranged as an $N×N$ bounded lattice, where each site can potentially hold a population. The genotype of each individual in these populations is a length $L+1$ string of digits, where $L_{min} \le L \le L_{max}$. Each locus in these genotypes is occupied by a zero or one of $A$ possible alleles. In several simulations, $A=1$, which produces genotypes that are binary bit strings. Alleles at the first $L$ loci determine the individual’s level of adaptation to the stressful environment. We refer to these loci as “stress loci”. An additional allele at the $(L+1)$<sup>th</sup> locus determines whether the individual is a producer (allele $1$) or a non-producer (allele $0$) of a public good. We refer to this locus as the “production locus”.


## Individual Fitness
A mutation from $0$ to any non-zero allele at the $i$<sup>th</sup> stress locus will improve individual fitness by $\delta$ despite the allelic states of other loci (i.e., there is no epistasis). For simplicity, all non-zero alleles carry the same fitness benefit. Public good production is costly, reducing individual fitness by $c$. Thus, if the allelic state of the $i$<sup>th</sup> locus is denoted $a_i$ with $a_i \in \{0, \ldots, A\}$, then the fitness of an individual is:

$$
W = z + \sum_{i=1}^{L} \delta \cdot Z(a_i) - a_{L+1} c
$$

where $z$ is a baseline fitness (the fitness of an individual with zeros at every locus), and $Z(a_i)$ indicates whether the allelic state $a_i$ is non-zero ($1$) or not ($0$). If there are no stress loci ($L=0$), the fitness of a producer and non-producer is $z-c$ and $z$, respectively.

**TODO: better name for $Z()$**
**TODO: add epsilon here?**

## Overview of Basic Simulation Cycle

Simulations are run for $T$ cycles, where each cycle consists of population growth, mutation, migration, and dilution at each site in the metapopulation. During this process, populations can alter the environment as described later. We first detail each stage of this basic cycle.


### Population Growth

**TODO: There aren't $2^{L+1}$ genotypes, but $(A+1)^{L+1}$. How can this best be described? Have a variable containing the number of genotypes?**

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

Metapopulations are initiated in a state that follows the onset of an environmental stress. First, populations are seeded at each site with producer proportion $p_{0}$ and grown to density $S(p_{0})$. Each population is then subjected to a bottleneck. Individuals survive this event with probability $\mu_{t}$, which represents the likelihood that a mutation occurs that enables survival. Because individuals have not yet adapted to this new stress, the allelic state $a_{i}$ is set to $0$ at each stress locus. The fitness effects associated with adaptations at each locus $w_{i}$ are also sampled as previously described.


## Changing Environments and Niche Construction

Through growth and adaptation, populations alter their environment. These changes can produce feedbacks that affect selection at the local or metapopulation level. We describe three ways by which populations bring about environmental change.

***TODO: mention that these methods were used separately?***

### Niche Construction at the Metapopulation Level

The sustained presence of organisms can reveal new avenues for adaptation. When $\tau_{m}$ individuals have existed in the metapopulation, an environmental change is triggered at each site. As with metapopulation intialization, this change resets the allelic state at each stress locus and regenerates the fitness effects of each adaptation. For these simulations, genotypes are represented by fixed-length binary strings (i.e., $L = L_{min} = L_{max}$ and $A = 1$).


### Niche Construction at the Population Level

Alternately, change occurs locally at a site when that population reaches cumulative density $\tau_{p}$. In this case, the number of fitness-affecting loci $L$ is increased for that population. When individuals from this population migrate to a neighboring site with smaller $L$, fitness is still based on the smaller $L$, but these indivuals are "pre-adapted" for future change at that site. Populations are initialized with $L = L_{min}$ and can induce environmental change until $L$ reaches $L_{max}$. Genotypes consist of binary strings ($A = 1$) in simulations where this form of construction occurs.


### Genotype-Mediated Niche Construction

Finally, we allow construction to be affected by the genotypes present in a population. Populations are initialized as previously described with genome length $L_{min}$, and each site is given a target allele drawn from the $A$ possible alleles. We expand individual fitness as described in Equation 1 to include additional fitness benefit $\epsilon$ for each allele $a_{i}$ that matches this target:

$$
W = z + \sum_{i=1}^{L} \delta \cdot Z(a_i) + \epsilon \cdot X(a_i) - a_{L+1} c
$$

Where $X(a_i)$ indicates whether allele $a_{i}$ matches the target ($1$) or not ($0$).

As with the population-level construction method, the presence of individuals over time expands a population's genome length. At the beginning of the simulation, an ordering is defined that specifies the sequence of revealed target alleles. 


TODO: how next alleles are chosen

TODO: Primacy, recency parameter


## Source Code and Software Versions

The simulation software and configurations for the experiments reported are available at [TODO](TODO). Simulations were run using Python 2.7.3, NumPy 1.9.0, and NetworkX 1.9.1. Data analyses were performed using R 3.1.2 [@rproject]. Model parameters and their values are listed in [Table X](https://github.com/briandconnelly/nicheconstruct/blob/master/paper/table_of_parameters.md).

# References
