# Materials and Methods

We build upon the model described in @HANKSHAW, in which cooperators and defectors compete and evolve in a spatially-structured metapopulation of populations. Each of these populations grows to carrying capacity, mutates, and migrates to neighboring patches. During this process, populations adapt to their local environments. In our extended model, we allow the presence of these individuals to modify their local environment, and these modifications feed back to affect selection.

## Model Description

Our simulated environment consists of $N^2$ patches arranged as an $N \times N$ lattice (see [Table 1](#tables) for model parameters and their values), where each patch supports a population of zero or more individuals. Each individual in the population has a genotype, which is an ordered list of $L+1$ integers (loci). The first $L$ loci are *adaptive loci*, and are each occupied by a $0$ or an integer from the set $A=\{1, \ldots, a_{max}\}$, where $a_{max}$ is the number of potential alleles. These alleles represent adaptations to the environment, and the number of loci determines the number of adaptations that are possible. All non-zero alleles confer fitness benefit $\delta$. A binary allele at locus $L+1$ determines whether or not that individual is a cooperator. Individuals with allelic state $1$ at this locus are cooperators, carrying a cost $c$, while individuals with allelic state $0$ are defectors. When $\delta \ge c$, an adapted cooperator recoups the cost of cooperation.

Organisms also influence their environment, which can feed back to influence selection. We model this as a form of frequency dependent selection. Specifically, the selective value of adaptive allele $a$ at locus $l$ increases with the proportion of the population that has allele $a-1$ (modulo $a_{max}$) at locus $l-1$ (and the first adaptive locus is affected by the last). The slope of this increase is $\epsilon$, which specifies the intensity of niche construction. As a consequence of this form of frequency dependence, genotypes with sequentially increasing allelic states will tend to evolve. Because mutations are random, as described later, each population will evolve sequences that start with different allelic states. These different sequences represent the unique niches constructed by populations. Under this model, the fitness of an individual with genotype $g$ in population $P$ is:

$$ W_{g} = z + \delta \sum_{l=1}^{L} I_{A}(a_{g,l}) + \epsilon \sum_{l=1}^{L} n(a_{g,l}) + c a_{g,L+1} $$ {#eq:fitness}

where $z$ is a baseline fitness, $c$ is the cost of the cooperative allele, $a_{g,l}$ represents the allelic state of genotype $g$ at locus $l$, $L$ is the number of adaptive loci, and $\gamma(j)$ is the genotype of individual $j$. The function $I_{A}$ indicates whether allelic state $y$ is in $A$ (i.e., it is non-zero). The function $n(a_{g,l})$ gives the number of individuals in the population with allelic state at the previous locus equal to one less than that at the focal locus $a_{g,l}$, or:

$$ n(a_{g,l}) = \sum_{h=1}^{N} I_{a_{g,l}} (1 + a_{h,l-1} (\bmod a_{max})) $$ {#eq:numepsilon}

Here, $I_{x} (y)$ indicates whether the allelic state $y$ matches allelic state $x$ ($1$) or not ($0$). 

Cooperators produce a public good that is equally accessible to all members of the population. This public good increases the carrying capacity at that patch, allowing the population to reach greater density. This benefit increases linearly with the proportion of cooperators. Thus, if $p$ is the proportion of cooperators in a population at the beginning of a growth cycle, then that population reaches the following size during the growth phase:

$$ S(p) = S_{min} + p (S_{max} - S_{min}) $$ {#eq:popsize}

The function $S(p)$ reflects the benefit of public good production. A population composed entirely of defectors reaches size $S_{min}$, while one composed entirely of cooperators reaches size $S_{max}$ (with $S_{max} \ge S_{min}$). During growth, individuals compete for inclusion in the resulting population. The composition of population $P$ with cooperator proportion $p$ after growth is multinomial with parameters and $S(p)$ and $\{\pi_1, \pi_2, \ldots, \pi_{|P|}\}$, where:

$$ \pi_i = \frac{W_{\gamma(i)}}{\sum_{j \in P} W_{\gamma(j)}} $$ {#eq:prob_repr}

Here, $\gamma(i)$ is the genotype of individual $i$, and $W_{\gamma(i)}$ is its fitness (see Equation @eq:fitness). $\pi_i$ therefore reflects that an individual's ability to persist is proportional to its fitness relative to others'.

For simplicity, we apply mutations after population growth. Mutations occur independently at each locus and cause the allelic state to change. At the binary cooperation locus, mutations occur at rate $\mu_{c}$. These mutations flip the allelic state, causing cooperators to become defectors and vice versa. Mutations occur at each adaptive locus at rate $\mu_{a}$, and cause a new allelic state to be chosen at random from the set $\{0\} \cup A$. Therefore, the probability that genotype $g$ mutates into genotype $g'$ is given by:

$$ \tau_{g \rightarrow g'} = \mu_{a}^{H_{a}(g,~g')}(1-\mu_{a})^{\{L-H_{a}(g,~g')\}} \mu_{c}^{H_{c}(g,~g')} (1-\mu_{c})^{\{1-H_{c}(g,~g')\}} $$ {#eq:mutations}

where $H_{a}(g,~g')$ and $H_{c}(g,~g')$ are the Hamming distances between genotypes $g$ and $g'$ at the cooperation locus and adaptive loci, respectively. The Hamming distance is the number of loci at which allelic states differ [@hamming1950bell]. Because we define no inherent relationship among alleles, each of the $a_{max} + 1$ allelic states is equally likely to arise via mutation at a given locus.

After mutation, individuals emigrate to an adjacent patch at rate $m$. The destination patch is randomly chosen with uniform probability from the source patch's Moore neighborhood, which is composed of the nearest 8 patches on the lattice. Because the metapopulation lattice has boundaries, patches located on an edge have smaller neighborhoods.

Metapopulations are initiated in a state that follows the onset of an environmental stress. First, populations are seeded at all patches with cooperator proportion $p_{0}$ and grown to density $S(p_{0})$. Stress is then introduced, which subjects the population to a bottleneck. For each individual, the probability of survival is $\mu_{t}$, which represents the likelihood that a mutation occurs that confers tolerance. Survivors are chosen by binomial sampling. Because individuals have not yet adapted to this new stress, the allelic state of each individual's genotype is set to $0$ at each adaptive locus ($\forall i \in P, l \in \{1, \ldots, L\}: a_{\gamma(i),l} = 0$). Following initialization, simulations are run for $T$ cycles, where each discrete cycle consists of growth, mutation, and migration. At the end of each cycle, populations are thinned to allow for growth in the next cycle. The individuals that remain are chosen by binomial sampling, where each individual persists with probability $d$, regardless of allelic state.


## Source Code and Software Environment

The simulation software and configurations for the experiments reported are available online [@coderef]. Simulations used Python 3.4.0, NumPy 1.9.1, Pandas 0.15.2 [@mckinney2010data], NetworkX 1.9.1 [@hagberg2008exploring]. Data analyses were performed with R 3.1.3 [@rproject].

