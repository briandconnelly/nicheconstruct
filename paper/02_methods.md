# Methods

We develop an individual-based model in which populations of cooperators and defectors evolve and compete in a spatially-structured metapopulation (a collection of populations).
Through mutations, individuals gain adaptations to their environment.
These adaptations increase reproductive fitness, and allow those lineages to rise in abundance.
Migration among neighboring populations allows these more successful lineages to spread.

We expand upon the model described by @HANKSHAW to allow populations to modify their local environment.
As this process occurs, environmental changes feed back to affect selection.
We explore how this niche construction affects evolutionary outcomes.


## Model Description

### Individual Genotypes and Adaptation

Each individual in a population has a genotype, which is an ordered list of $L+1$ integers, or *loci* (see [Table 1](#tables) for model parameters and their values).
Different values at these loci represent different alleles.
A binary allele at the locus ($L+1$) determines whether that individual is a defector ($0$) or a cooperator ($0$), which carries fitness cost $c$.
The first $L$ loci are *adaptive loci*, and are each occupied by $0$ or an integer from the set $\{1, 2, \ldots, A\}$.
Allele $0$ represents a lack of adaptation, while a non-zero allele represents one of the $A$ possible adaptations at that locus.
The presence of any of these adaptations confers a fitness benefit $\delta$.
We choose $\delta > c$, which allows a minimally adapted cooperator to recoup the cost of cooperation and gain a fitness advantage.
The benefits that these adaptations engender are purely endogenous, and are not affected by the other individuals or the state of the environment.


### Niche Construction and Selective Feedbacks

The state of the local environment also affects fitness.
Here, we model the "niche" implicitly based on the allelic states present in the population.
As allelic states change, populations alter their environment in different ways, creating a unique niche.

We use a form of density dependent selection to capture the eco-evolutionary feedbacks that result from niche construction by increasingly favoring individuals that match their niche.
Specifically, the selective value of adaptive allele $a$ at locus $l$ increases with the number of individuals in the population that have allele $a+1$ at locus $l+1$.
As a consequence of this form of density dependent selection, genotypes with sequentially increasing allelic states will tend to evolve.
We treat both adaptive loci and allelic states as "circular", so the allelic state at locus $L$ is affected by the allelic composition of the population at locus 1, and the selective value of allele $A$ at any locus increases with the number of individuals carrying allele $1$ at the next locus.
This circularity is represented by the function $\beta(x,X)$, which gives the integer that follows an arbitrary value $x$ in the set $\{1, 2, \ldots, X\}$:

$$ \beta(x, X) = \bmod_{X}(x) + 1 $$ {#eq:beta}

Here, $\bmod_{X}(x)$ is the integer remainder when dividing $y$ by $X$.
Thus, the selective value of adaptive allele $a$ at locus $l$ increases with the number of individuals that have allele $\beta(a,A)$ at locus $\beta(l, L)$.
The slope of this increase is $\epsilon$, which specifies the intensity of niche construction.
Consider a genotype $g$ with the allelic state at locus $l$ given by $a_{g,l}$; the fitness of an individual with this genotype is defined as:

$$ W_{g} = z + \delta \sum_{l=1}^{L} I(a_{g,l}) + \epsilon \sum_{l=1}^{L} n(\beta(a_{g,l}, A), \beta(l, L)) - c a_{g,L+1} $$ {#eq:fitness}

where $z$ is a baseline fitness and $I(a)$ indicates whether a given adaptive allele is non-zero:

$$
I(a) =
\begin{cases}
    1 & \text{if }a \in \{1,2,\ldots,A\} \\
    0 & \text{otherwise}
\end{cases}
$$ {#eq:IA}

Because mutations occur randomly (see below), each population will evolve different consecutive sequences.
These different sequences represent the unique niches constructed by populations.


### Population Growth and the Benefit of Cooperation

Cooperation allows the population to reach greater density.
If $p$ is the proportion of cooperators in a population at the beginning of a growth cycle, then that population reaches the following size:

$$ S(p) = S_{min} + p (S_{max} - S_{min}) $$ {#eq:popsize}

The function $S(p)$ reflects the benefit of cooperation.
During growth, individuals compete for inclusion in the resulting population.
The composition of a population with size $P$ and cooperator proportion $p$ after growth is multinomial with parameters and $S(p)$ and $\{\pi_1, \pi_2, \ldots, \pi_{P}\}$, where:

$$ \pi_i = \frac{W_{\gamma(i)}}{\sum_{j=1}^{P} W_{\gamma(j)}} $$ {#eq:prob_repr}

Here, $W_{\gamma(i)}$ is the fitness of an individual $i$ with genotype $\gamma(i)$ (see Equation @eq:fitness).
The value $\pi_i$ therefore reflects an individual's reproductive fitness relative to others' in the population.


### Mutation

For simplicity, we apply mutations after population growth.
Mutations occur independently at each locus and cause an allelic state change.
At each adaptive locus, mutations occur at rate $\mu_{a}$.
These mutations replace the current allele with a random selection from the set $\{0\} \cup \{1, 2, \ldots, A\}$.
Note that this allows for the possibility of an allele replacing itself, thus slightly reducing the effective mutation rate.
At the binary cooperation locus, mutations occur at rate $\mu_{c}$.
These mutations flip the allelic state, causing cooperators to become defectors and vice versa.


### Migration

Our simulated environment consists of $N^2$ patches arranged as an $N \times N$ lattice, where each patch can support a population.
After mutation, individuals emigrate to an adjacent patch at rate $m$.
The destination patch is randomly chosen with uniform probability from the source patch's Moore neighborhood, which is composed of the nearest 8 patches on the lattice.
Because the metapopulation lattice has boundaries, patches located on an edge have smaller neighborhoods.


### Metapopulation Initialization and Simulation

Metapopulations are initiated in a state that follows an environmental change, which leaves most patches empty.
First, populations are seeded at all patches with cooperator proportion $p_{0}$ and grown to density $S(p_{0})$.
An environmental challenge is then introduced, which subjects the population to a bottleneck.
For each individual, the probability of survival is $\mu_{t}$, which represents the likelihood that a mutation occurs that confers tolerance.
Because individuals have not yet adapted to this new environment, the allelic state of each individual's genotype is set to $0$ at each adaptive locus.
Following initialization, simulations are run for $T$ cycles, where each discrete cycle consists of population growth, mutation, and migration.
At the end of each cycle, populations are thinned to allow for growth in the next cycle.
Each individual persists with probability $d$, regardless of allelic state.


## Source Code and Software Environment

The simulation software and configurations for the experiments reported are available online.
Simulations used Python 3.4, NumPy 1.9.1, Pandas 0.15.2 [@mckinney2010data], and NetworkX 1.9.1 [@hagberg2008exploring].
Data analyses were performed with R 3.1.3 [@rproject].
Reported confidence intervals were estimated by bootstrapping with 1000 resamples.

