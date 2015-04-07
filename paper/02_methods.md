
# Methods

Building upon @HANKSHAW, we develop an individual-based model in which cooperators and defectors evolve and compete in a population of subpopulations (i.e., a metapopulation).
Through mutations, individuals gain adaptations to their environment, which increase reproductive fitness, and allow those lineages to rise in abundance.
Migration among neighboring subpopulations allows more successful lineages to spread.

In this expanded model, subpopulations additionally modify their local environment.
As this process occurs, environmental changes feed back to affect selection.
We explore how niche construction affects this process of adaptation and whether cooperation can be maintained because of selective feedbacks.


## Model Description

### Individual Genotypes and Adaptation

Each individual has a haploid genome with $L + 1$ loci (see [Table 1](#tables) for model parameters and their values).
Different alleles at each locus are represented by different integers.
A binary allele at the first locus (here, locus zero) determines whether that individual is a cooperator ($1$), which carries fitness cost $c$, or a defector ($0$).
Cooperation is independent from adaptation to the environment.
The remaining $L$ loci are *adaptive loci*, and are each occupied by $0$ or a value from the set $\{1, 2, \ldots, A\}$.
Allele $0$ represents a lack of adaptation, while a non-zero allele represents one of the $A$ possible adaptations at that locus.
These non-zero alleles signify adaptations to the external environment that are not affected by other individuals or the local niche.
Adaptations confer a fitness benefit $\delta$, regardless of which non-zero allele is present.
We assume $\delta > c$, which allows a minimally adapted cooperator to recoup the cost of cooperation and gain a fitness advantage.


### Niche Construction and Selective Feedbacks

Individual fitness is also affected by the current state of the local environment.
We represent the "niche" implicitly based on the specific allelic states present in the subpopulation.
Here, the specific alleles that are present at each locus matter.
As allelic states change, subpopulations alter aspects of their environment, creating a unique niche.

Niche construction takes the form of density dependent selection, and individuals evolve to better match their niche by a second form of adaptation.
Specifically, the selective value of adaptive allele $a$ at locus $l$ increases with the number of individuals in the subpopulation that have allele $a-1$ at locus $l-1$.
Once allele $a$ has fixed in the subpopulation at locus $l$, allele $a+1$ becomes the only allele that confers fitness benefits at locus $l+1$.
As a consequence, genotypes with sequentially increasing allelic states will tend to evolve.
We treat both adaptive loci and allelic states as "circular": the selective value of an allele at locus 1 is affected by the allelic composition of the subpopulation at locus $L$.
Similarly, the selective value of allele 1 at any locus increases with the number of individuals carrying allele $A$ at the previous locus.
This circularity is represented by the function $\beta(x,X)$, which gives the integer that is below an arbitrary value $x$ in the set $\{1, 2, \ldots, X\}$:

$$ \beta(x, X) = \bmod_{X}(x - 2 + X) + 1 $$ {#eq:beta}

Here, $\bmod_{X}(x)$ is the integer remainder when dividing $x$ by $X$.
The selective value of adaptive allele $a$ at locus $l$ is increased by $\epsilon$ for each individual in the subpopulation that has allele $\beta(a,A)$ at locus $\beta(l, L)$.
Thus, $\epsilon$ specifies the intensity of selection due to niche construction.

Consider a genotype $g$ with the allelic state at locus $l$ given by $a_{g,l}$; the fitness of an individual with this genotype is defined as:

$$ W_{g} = z - \underbrace{c a_{g,0}}_{{\substack{\text{cost of} \\ \text{cooperation}}}} + \underbrace{\delta \sum_{l=1}^{L} I(a_{g,l})}_{\substack{\text{adaptation to} \\ \text{external environment}}} + \underbrace{\epsilon \sum_{l=1}^{L} n(\beta(a_{g,l}, A), \beta(l, L))}_{\substack{\text{adaptation to} \\ \text{constructed environment}}} $$ {#eq:fitness}

where $z$ is a baseline fitness, $n(a,l)$ is the number of individuals with allele $a$ at locus $l$, and $I(a)$ indicates whether a given adaptive allele is non-zero:

$$
I(a) =
\begin{cases}
    1 & \text{if }a \in \{1,2,\ldots,A\} \\
    0 & \text{otherwise}
\end{cases}
$$ {#eq:IA}

Thus, an individual's fitness is determined both by adaptations to the external environment ($\delta$) and adaptations to its constructed environment ($\epsilon$).
[Figure 1](#fig1) illustrates the effects of these two components.


### Population Growth and the Benefit of Cooperation

Cooperation enables a subpopulation to reach a greater density.
This benefit affects all individuals equally and accumulates linearly with the proportion of cooperators in the subpopulation.
If $p$ is the proportion of cooperators present at the beginning of a growth cycle, then that subpopulation reaches the following size:

$$ S(p) = S_{min} + p (S_{max} - S_{min}) $$ {#eq:popsize}

During growth, individuals compete through differential reproduction.
Each individual's probability of success is determined by its fitness.
The composition of a subpopulation with size $P$ and cooperator proportion $p$ after growth is multinomial with parameters $S(p)$ and $\{\pi_1, \pi_2, \ldots, \pi_{P}\}$, where:

$$ \pi_i = \frac{W_{\gamma(i)}}{\sum_{j=1}^{P} W_{\gamma(j)}} $$ {#eq:prob_repr}

Here, $W_{\gamma(i)}$ is the fitness of an individual $i$ with genotype $\gamma(i)$ (see Equation @eq:fitness).
The value $\pi_{i}$ represents an individual's reproductive fitness relative to others in the subpopulation.


### Mutation

For simplicity, we apply mutations after growth.
Mutations occur independently at each locus and cause an allelic state change.
At the binary cooperation locus, mutations occur at rate $\mu_{c}$.
These mutations flip the allelic state, causing cooperators to become defectors and vice versa.
Mutations occur at rate $\mu_{a}$ at each adaptive locus.
These mutations replace the existing allele with a random selection from the set $\{0\} \cup \{1, 2, \ldots, A\}$.
Because mutations are stochastic, the allelic sequences that evolve depend on which allele arises first and at which locus.


### Migration

Populations are composed by $N^2$ patches arranged as an $N \times N$ lattice, where each patch can support a subpopulation.
After mutation, individuals emigrate to an adjacent patch with probability $m$.
During each migration event, a single destination patch is randomly chosen with uniform probability from each source patch's Moore neighborhood, which is composed of the nearest 8 patches on the lattice.
Because the population lattice has boundaries, patches located on the periphery have smaller neighborhoods.


### Population Initialization and Simulation

At the beginning of each simulation, subpopulations are seeded at all patches with cooperator proportion $p_{0}$ and grown to density $S(p_{0})$.
An environmental challenge is then introduced, which subjects all subpopulations to a bottleneck.
For each individual, the probability of survival is $\mu_{t}$, which represents the likelihood that tolerance arises via mutation.
Because individuals have not yet adapted to this new environment, the allelic state of each individual's genotype is $0$ at each adaptive locus.
Following initialization, simulations are run for $T$ cycles, where each discrete cycle consists of subpopulation growth, mutation, migration, and dilution.
Dilution thins the population to support growth in the next cycle.
Each individual remains with probability $d$, regardless of allelic state.


## Simulation Source Code and Software Dependencies

The simulation software and configurations for the experiments reported are available online [^1].
Simulations used Python 3.4, NumPy 1.9.1, Pandas 0.15.2 [@mckinney2010data], and NetworkX 1.9.1 [@hagberg2008exploring].
Data analyses were performed with R 3.1.3 [@rproject].
Reported confidence intervals were estimated by bootstrapping with 1000 resamples.

[^1]: These materials will be made public at the time of publication, and a reference will be placed here.

