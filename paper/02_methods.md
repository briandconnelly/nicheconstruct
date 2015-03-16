# Materials and Methods

We develop a computational model to observe the evolution of public goods cooperation in a spatially-structured metapopulation of populations. As described below, populations grow to carrying capacity, mutate, and migrate to neighboring patches. During this process, populations adapt to their local environments. The environments are, in turn, modified by the presence of these adapted individuals, allowing each population to construct a unique niche along its evolutionary trajectory. Model parameters and their values are listed in [Table 1](#tables).


## Individuals and Fitness

Each individual has a genotype of length $L+1$. A binary allele at the first locus determines whether or not the individual is a cooperator, which carries cost $c$. The remaining $L$ loci are *stress loci*, and are each occupied by a $0$ or an integer from the set $A=\{1, \ldots, a_{max}\}$, where $a_{max}$ is the number of possible alleles. These alleles represent adaptations to the environment, and the number of loci determines the number of possible adaptations. All non-zero alleles carry fitness benefit $\delta$. Organisms also influence their environment, which can feed back to influence selection. We model this as a form of frequency dependent selection. Specifically, the selective value of stress allele $a$ at locus $i$ increases with the proportion of the population that has allele $a-1$ (modulo $a_{max}$) at locus $i-1$. The slope of this increase is $\epsilon$ (which gauges the intensity of niche construction). As a consequence of this form of frequency dependence, genotypes with sequentially increasing allelic states will tend to evolve. Because mutations are random, as described below, each population will evolve sequences that start with different allelic states. These different sequences represent the unique niches constructed by populations. Under this model, the fitness of an individual with genotype $g$ is:

* **TODO**: Update text to describe wraparound.
* **TODO**: Properly typeset the modulo in the text?
* **TODO**: Update equation for wraparound
* **TODO**: Use gamma to represent genotype, so gamma(h), since h represents individual number h

$$
W_{g} = z + a_{g,1} c + \delta \sum_{l=2}^{L+1} I_{A}(a_{g,l}) + \epsilon \sum_{h=1}^{N} I_{a_{h,1}} (a_{g,1}) + \epsilon \sum_{l=2}^{L} n(a_{g,l})
$$

where $a_{g,l}$ represents the allelic state of genotype $g$ at locus $l$, $z$ is a baseline fitness, $L$ is the number of stress loci, $N$ is the population size at that patch, and $c$ is the cost of the cooperative allele. $I_{x} (y)$ indicates whether the allelic state $y$ matches allelic state $x$ ($1$) or not ($0$). $n(a_{g,l})$ is the number of individuals in the population with allelic state at the previous locus equal to one less than that at the focal locus $a_{g,l}$, or:

$$
n(a_{g,l}) = \sum_{h=1}^{N} I_{a_{g,l}} (1 + a_{h,l-1} (\bmod a_{max}))
$$


## Population Growth

If $p$ is the proportion of producers in a population at the beginning of a growth cycle, then that population reaches the following size during the growth phase:

$$
S(p) = S_{min} + p (S_{max} - S_{min})
$$

Therefore, a population composed entirely of non-producers reaches size $S_{min}$, while one composed entirely of producers reaches size $S_{max}$ (with $S_{max} \ge S_{min}$). The function $S(p)$ gauges the benefit of public good production, as population size increases linearly with the proportion of producers. During growth, competition occurs. Consider an arbitrary genotype $g$. Let $n_g$ be the number of individuals with genotype $g$, and let $W_{g}$ be the fitness of genotype $g$ (see equation [1]). The composition of genotypes after population growth is multinomial with parameters $S(p)$ and $\{\pi_1, \pi_2, \ldots, \pi_{|G|}\}$, where:

$$
\pi_g = \frac{n_g W_g}{\sum_{i=1}^{G} n_i W_i}
$$

Thus, $\pi_g$ is the probability that an individual in the population after growth has genotype $g$ (such that $\sum \pi_g = 1$). $G$ represents the set of all $(a_{max} + 1)^{L}$ genotypes.


## Mutation

For simplicity, we apply mutation after population growth. These mutations occur independently at each locus and result in an allelic state change. At the binary cooperation locus, mutations flip the allelic state at rate $\mu_{c}$, causing cooperators to become defectors and vice versa. Mutations at a stress locus cause a new allelic state to be chosen at random from the set $\{0\} \cup A$. These mutation occur at each stress locus at rate $\mu_{s}$. Therefore, the probability that genotype $g$ mutates into genotype $g'$ is given by:

$$
\tau_{g \rightarrow g'} = \mu_{s}^{H_{s}(g,~g')}(1-\mu_{s})^{\{L-H_{s}(g,~g')\}} \mu_{c}^{H_{p}(g,~g')} (1-\mu_{c})^{\{1-H_{p}(g,~g')\}}
$$

where $H_{s}(g,~g')$ and $H_{p}(g,~g')$ are the Hamming distances between genotypes $g$ and $g'$ at the stress loci and production locus, respectively. The Hamming distance is the number of loci at which allelic states differ. Because there is no inherent relationship among alleles, each of the $a_{max} + 1$ alleles is equally likely to arise via mutation at a given locus.


## Migration and Metapopulation Structure

The metapopulation consists of $N^2$ patches arranged in a $N \times N$ lattice. After mutation, individuals emigrate to an adjacent patch with probability $m$. This adjacent patch is randomly chosen with uniform probability from the source patch's Moore neighborhood, which is composed of the nearest 8 patches on the lattice. Because the metapopulation lattice has boundaries, patches located on an edge have smaller neighborhoods.


## Initialization and Simulation

Metapopulations are initiated in a state that follows the onset of an environmental stress. First, populations are seeded at each patch with producer proportion $p_{0}$ and grown to density $S(p_{0})$. Stress is then introduced by subjecting the population to a bottleneck. The number of survivors with each genotype $g$ is sampled from a binomial distribution, where the number of trials is $n_g$. The probability of success is $\mu_{t}$, which represents the likelihood that a mutation occurs that enables survival. Because individuals have not yet adapted to this new stress, the allelic state of each genotype is set to $0$ at each stress locus ($\forall g \in G, l \in \{2, \ldots, L+1\}: a_{g,l} = 0$). Following initialization, simulations are run for $T$ cycles, where each cycle consists of growth, mutation, and migration. After migration, populations are thinned to allow for growth in the next cycle. The number of survivors for each genotype $g$ is sampled from a binomial distribution, where the number of trials is $n_g$ and the probability of success is $d$.


## Source Code

The simulation software and configurations for the experiments reported are available online [@coderef].

