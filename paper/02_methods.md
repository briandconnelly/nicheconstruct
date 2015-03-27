# Materials and Methods

We build upon the model described in @HANKSHAW, in which cooperators and defectors compete and evolve in a metapopulation (a collection of populations). Individuals in each of the populations reproduce, mutate, and migrate to neighboring populations. Importantly, adaptation that is independent of cooperation can occur. In our model here, we further allow populations to modify their local environment, and these modifications feed back to affect selection.

## Model Description

Our simulated environment consists of $N^2$ patches arranged as an $N \times N$ lattice (see [Table 1](#tables) for model parameters and their values), where each patch can support a population. Each individual in a population has a genotype, which is an ordered list of $L+1$ integers (loci). The first $L$ loci are *adaptive loci*, and are each occupied by $0$ or an integer from the set $A \equiv \{1, 2, \ldots, a_{max}\}$, where $a_{max}$ is the number of alleles conferring a selective benefit. Specifically, the presence of a non-zero allele at any of these loci represents an adaptation that confers fitness benefit $\delta$. A binary allele at locus $L+1$ determines whether or not that individual is a cooperator. Individuals with allelic state $1$ at this locus are cooperators, carrying a cost $c$, while individuals with allelic state $0$ are defectors. When $\delta \ge c$, a minimally adapted cooperator recoups the cost of cooperation. Equation @eq:numinds defines function $n(a,l)$, which gives the number of individuals in the population with allelic state $a$ at locus $l$. $I_{x}(y)$ indicates whether the allelic state $y$ matches allelic state $x$ ($1$) or not ($0$), and $\gamma(i)$ is the genotype of individual $i$.

$$ n(a, l) = \sum_{i \in P} I_{a_{g,l}}(a_{\gamma(i), l}) $$ {#eq:numinds}

Organisms also influence their environment, which, in turn, influences selection. We model this as a form of density dependent selection. Specifically, the selective value of adaptive allele $a$ at locus $l$ increases with the number of individuals in the population that have allele $a-1$ at locus $l-1$. We treat both adaptive loci and allelic states as "circular", so the allelic state at locus 1 is affected by the allelic composition of the population at locus $L$, and the selective value of allele 1 at any locus increases with the number of individuals carrying allele $a_{max}$ at the previous locus. To make this circularity mathematically crisp, we define a function giving the integer below $x$ in the set $\{1, 2, \ldots, X\}$ 

$$ \beta(x, X) = \bmod_{X}(x - 2 + X) + 1 $$ {#eq:beta}

Where $\bmod_{Y}(y)$ is the integer remainder after dividing $y$ by $Y$. Thus, the value of adaptive allele $a$ at locus $l$ increases with the number of individuals that have allele $\beta(a,a_{max})$ at locus $\beta(l, L)$. The slope of this increase is $\epsilon$, which specifies the intensity of niche construction. Consider a genotype $g$ with allelic state at locus $l$ given by $a_{g,l}$; its fitness is defined as:

$$ W_{g} = z + \delta \sum_{l=1}^{L} I_{A}(a_{g,l}) + \epsilon \sum_{l=1}^{L} n(\beta(a_{g,l}, a_{max}), \beta(l, L)) - c a_{g,L+1} $$ {#eq:fitness}

where $z$ is a baseline fitness, and $I_{A}(a)$ indicates whether an adaptive allele is non-zero:

$$
I_{A}(a) =
\begin{cases}
    1 & \text{if }a \in A \\
    0 & \text{otherwise}
\end{cases}
$$ {#eq:IA}

As a consequence of this form of density dependent selection, genotypes with sequentially increasing allelic states will tend to evolve. Because mutations are random (see below), each population will evolve different consecutive sequences. These different sequences represent the unique niches constructed by populations.

Cooperators produce a public good that is equally accessible to all members of the population. This public good increases the carrying capacity at that patch, allowing the population to reach greater density. This benefit increases linearly with the proportion of cooperators. Thus, if $p$ is the proportion of cooperators in a population at the beginning of a growth cycle, then that population reaches the following size during the growth phase:

$$ S(p) = S_{min} + p (S_{max} - S_{min}) $$ {#eq:popsize}

The function $S(p)$ reflects the benefit of public good production. A population composed entirely of defectors reaches size $S_{min}$, while one composed entirely of cooperators reaches size $S_{max}$ (with $S_{max} \ge S_{min}$). During growth, individuals compete for inclusion in the resulting population. The composition of population $P$ with cooperator proportion $p$ after growth is multinomial with parameters and $S(p)$ and $\{\pi_1, \pi_2, \ldots, \pi_{|P|}\}$, where:

$$ \pi_i = \frac{W_{\gamma(i)}}{\sum_{j \in P} W_{\gamma(j)}} $$ {#eq:prob_repr}

Here, $W_{\gamma(i)}$ is the fitness of an individual $i$ with genotype $\gamma(i)$ (see Equation @eq:fitness). The value $\pi_i$ therefore reflects an individual's relative reproductive fitness.

For simplicity, we apply mutations after population growth. Mutations occur independently at each locus and cause the allelic state to change. Mutations occur at each adaptive locus at rate $\mu_{a}$, in which a new allele is chosen at random from the set $\{0\} \cup A$. At the binary cooperation locus, mutations occur at rate $\mu_{c}$. These mutations flip the allelic state, causing cooperators to become defectors and vice versa. Therefore, the probability that genotype $g$ mutates into genotype $g'$ is given by:

$$ \tau_{g \rightarrow g'} = \mu_{a}^{H_{a}(g,~g')}(1-\mu_{a})^{\{L-H_{a}(g,~g')\}} \mu_{c}^{H_{c}(g,~g')} (1-\mu_{c})^{\{1-H_{c}(g,~g')\}} $$ {#eq:mutations}

where $H_{a}(g,~g')$ and $H_{c}(g,~g')$ are the Hamming distances between genotypes $g$ and $g'$ at the cooperation locus and adaptive loci, respectively. The Hamming distance is the number of loci at which allelic states differ [@hamming1950bell].

After mutation, individuals emigrate to an adjacent patch at rate $m$. The destination patch is randomly chosen with uniform probability from the source patch's Moore neighborhood, which is composed of the nearest 8 patches on the lattice. Because the metapopulation lattice has boundaries, patches located on an edge have smaller neighborhoods.

Metapopulations are initiated in a state that follows an environmental change. First, populations are seeded at all patches with cooperator proportion $p_{0}$ and grown to density $S(p_{0})$. An environmental challenge is then introduced, which subjects the population to a bottleneck. For each individual, the probability of survival is $\mu_{t}$, which represents the likelihood that a mutation occurs that confers tolerance. Survivors are chosen by binomial sampling. Because individuals have not yet adapted to this new environment, the allelic state of each individual's genotype is set to $0$ at each adaptive locus. Following initialization, simulations are run for $T$ cycles, where each discrete cycle consists of growth, mutation, and migration. At the end of each cycle, populations are thinned to allow for growth in the next cycle. The individuals that remain are chosen by binomial sampling, where each individual persists with probability $d$, regardless of allelic state.


## Source Code and Software Environment

The simulation software and configurations for the experiments reported are available online [@coderef]. Simulations used Python 3.4.0, NumPy 1.9.1, Pandas 0.15.2 [@mckinney2010data], and NetworkX 1.9.1 [@hagberg2008exploring]. Data analyses were performed with R 3.1.3 [@rproject].

