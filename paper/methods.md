---
title: "Methods"
csl: evolutionary-ecology-research.csl
output:
  word_document:
    fig_height: 5
    fig_width: 5
  pdf_document:
    number_sections: no
    toc: no
  html_document:
    number_sections: no
    theme: default
    toc: yes
bibliography: references.bib
---

We develop a computational model to observe how the evolution of public goods production is affected as populations modify and adapt to their environment. Each simulation tracks a single metapopulation composed of $N^2$ patches arranged as an $N×N$ bounded lattice, where each patch can hold a population. The genotype of each individual in these populations is a length $L+1$ string of digits, where $L_{min} \le L \le L_{max}$. Values (alleles) in the first $L$ positions (loci) determine the individual’s level of adaptation to the stressful environment. Each of these “stress loci” is occupied by a zero or an element from the set of alleles $A = \{1, \ldots, a_{max}\}$, where $a_{max}$ is the number of possible alleles. An additional binary allele at the $(L+1)$<sup>th</sup> locus determines whether the individual is a producer (allele $1$) or a non-producer (allele $0$) of a public good. We refer to this locus as the “production locus”. Using this represnetation, the number of unique genotypes $G$ is $(A + 1)^{L + 1}$.


## Individual Fitness
A mutation from $0$ to any non-zero allele from $A$ at the $i$<sup>th</sup> stress locus will improve individual fitness by $\delta$ regardless of the allelic states of other loci (i.e., there is no epistasis). For simplicity, all non-zero alleles carry the same fitness benefit. Public good production is costly, reducing individual fitness by $c$. Thus, if the allelic state of the $l$<sup>th</sup> locus in genotype $g$ is denoted $a_{g,l}$ with $a_{g,l} \in (\{0\} \cup A)$, then the fitness of an individual with genotype $g$ is:

$$
W_{g} = z + \delta \sum_{l=1}^{L} 1_{A}(a_{g,l}) - a_{g,L+1} c
$$


where $z$ is a baseline fitness (the fitness of an individual with zeros at every locus), and $1_{A}$ indicates whether the allelic state $a_{g,l}$ is non-zero ($1$) or not ($0$). If there are no stress loci ($L=0$), the fitness of a producer and non-producer is $z-c$ and $z$, respectively.


## Overview of Basic Simulation Cycle

Simulations are run for $T$ cycles, where each cycle consists of population growth, mutation, migration, and dilution at each patch in the metapopulation. During this process, populations can alter the environment as described later. We first detail each stage of this basic cycle.


### Population Growth

If $p$ is the proportion of producers in a population at the beginning of a growth cycle, then that population reaches the following size during the growth phase:

$$
S(p) = S_{min} + p (S_{max} - S_{min})
$$

Therefore, a population composed entirely of non-producers reaches size $S_{min}$, while one composed entirely of producers reaches size $S_{max}$ (with $S_{max} \ge S_{min}$). The function $S(p)$ gauges the benefit of public good production, as population size increases linearly with the proportion of producers. During growth, competition occurs among the $G$ genotypes. Consider an arbitrary genotype $g$. Let $n_g$ be the number of individuals with genotype $g$, and let $W_{g}$ be the fitness of genotype $g$ (see equation [1]). The composition of genotypes after population growth is multinomial with parameters $S(p)$ and $\{\pi_1, \pi_2, \ldots, \pi_{G}\}$, where

$$
\pi_g = \frac{n_g W_g}{\sum_{i=1}^{G} n_i W_i}
$$

Thus, $\pi_g$ is the probability that an individual in the population after growth has genotype $g$ (such that $\sum \pi_g = 1$).


### Mutation

For simplicity, we apply mutation after population growth. For every individual, allelic state changes occur independently at each stress locus with probability $\mu_{s}$, while the production locus changes allelic state with probability $\mu_{p}$. Thus, the probability that genotype $g$ mutates into genotype $g'$ is given by

$$
\tau_{g \rightarrow g'} = \mu_{s}^{H_{s}(g,~g')}(1-\mu_{s})^{\{L-H_{s}(g,~g')\}} \mu_{p}^{H_{p}(g,~g')} (1-\mu_{p})^{\{1-H_{p}(g,~g')\}}
$$

where $H_{s}(g,~g')$ and $H_{p}(g,~g')$ are the Hamming distances between genotypes $g$ and $g'$ at the stress loci and production locus, respectively. The Hamming distance is the number of loci at which allelic states differ. Because there is no inherent relationship among alleles, each of the $A + 1$ alleles is equally likely to arise via mutation at a given locus.


### Migration

Following mutation, migration occurs among populations. For each populated patch, individuals move to an adjacent patch with probability $m$. This adjacent patch is randomly chosen with uniform probability from the source patch's Moore neighborhood, which is composed of the nearest 8 patches on the lattice. Because the metapopulation lattice has boundaries, patches located on an edge have smaller neighborhoods.


### Dilution

After migration, populations are thinned to allow for growth in the next cycle. Each individual, despite its genotype, survives this bottleneck with probability $d$. The number of survivors for each genotype $g$ is sampled from a binomial distribution, where the number of trials is $n_g$ and the probability of success is $d$.


### Initialization

Metapopulations are initiated in a state that follows the onset of an environmental stress. First, populations are seeded at each patch with producer proportion $p_{0}$ and grown to density $S(p_{0})$. Stress is then introduced by subjecting the population to a bottleneck. The number of survivors with each genotype $g$ is sampled from a binomial distribution, where the number of trials is $n_g$. The probability of success is $\mu_{t}$, which represents the likelihood that a mutation occurs that enables survival. Because individuals have not yet adapted to this new stress, the allelic state is set to $0$ at each stress locus ($\forall g \in \{1, \ldots, G\}, l \in \{1, \ldots, L\}: a_{g,l} = 0$).


## Changing Environments and Niche Construction

Through growth and adaptation, populations alter their environment in one of three ways. These changes can produce feedbacks that affect selection at the local or metapopulation level.


### Niche Construction at the Metapopulation Level

The sustained presence of organisms can reveal new avenues for adaptation. When $\tau_{m}$ individuals have existed in the metapopulation, an environmental change is triggered at each patch. As with metapopulation intialization, this change resets the allelic state at each stress locus and subjects individuals to a bottleneck that is survived with probability $\mu_{t}$. For these simulations, genotypes are represented by fixed-length binary strings (i.e., $L = L_{min} = L_{max}$ and $A = 1$).


### Niche Construction at the Population Level

Alternately, change occurs locally at a patch when its population reaches cumulative density $\tau_{p}$. In this case, the number of fitness-affecting loci $L$ is increased at that patch. Fitness is patch-specific, so the state at alleles greater than $L$ will have no fitness effects in individuals that immigrate from patches with larger $L$. Patches are initialized with $L = L_{min}$ and populations can increase $L$ through this process until it reaches $L_{max}$. For simulations using this form of niche construction, binary string genotypes are used ($A = 1$).

### Genotype-Mediated Niche Construction

**Note: This section is under heavy construction.**
**TODO: describe ordering of alleles**

Finally, we allow construction to be affected by the genotypes present in a population. Populations are initialized as previously described with genome length $L_{min}$, and each patch is given a target allele drawn from the $A$ possible alleles. We expand individual fitness as described in Equation 1 to include additional fitness benefit $\epsilon$ for each allele $a_{g,l}$ that matches this target:

$$
W_{g} = z + \delta \sum_{l=1}^{L} 1_{A}(a_{g,l}) + \epsilon OtherLoci + \epsilon SelfLocus - a_{g,L+1} c
$$

Where $X(a_l)$ indicates whether allele $a_{l}$ matches the target ($1$) or not ($0$).

As with the population-level construction method, the presence of individuals over time expands a population's genome length. At the beginning of the simulation, an ordering is defined that specifies the sequence of revealed target alleles. 

To allow population growth and niche construction to occur on different timescales, we also retain the distribution of genotypes in each population for $n$ cycles. Following [@laland1996evolutionary], these $n$ states can equally affect the allele to be revealed next or be affected more by earlier or later population states.

* Can we handle weighting of the values over time with a single parameter? [@laland1996evolutionary] kind of does, but they use separate equations for the primacy, recency, and equal weight cases. Hill function?





## Source Code and Software Environment

The simulation software and configurations for the experiments reported are available at [TODO](TODO). Simulations used Python 2.7.3, NumPy 1.9.1, and NetworkX 1.9.1. Data analyses were performed with R 3.1.2 [@rproject]. Model parameters and their values are listed in [Table X](https://github.com/briandconnelly/nicheconstruct/blob/master/paper/table_of_parameters.md).

# References
