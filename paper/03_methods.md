
# Methods

Building upon @HANKSHAW, we describe an individual-based model in which cooperators and defectors evolve and compete in a population of subpopulations (i.e., a metapopulation).
Through mutation, individuals gain adaptations to their environment, which increase reproductive fitness and allow those lineages to rise in abundance.
Adapted lineages then spread throughout the population by migration to neighboring subpopulations.

In the expanded model described here, subpopulations also continually modify their local environment.
These environmental changes feed back to affect selection.
We use this model to explore how niche construction affects the evolution of cooperation; specifically, how cooperative behavior can hitchhike along with adaptations to modified environments.


## Model Description

### Individual Genotypes and Adaptation

Each individual has a haploid genome with $L + 1$ loci, where integers represent different alleles at each locus ([Table 1](#tables) lists all model parameters and their values).
An allele at the *cooperation locus* (locus zero) determines whether that individual is a cooperator (allele $1$), which carries fitness cost $c$, or a defector (allele $0$).
The remaining $L$ loci are *adaptive loci*, and are each occupied by a value from the set $\{0, 1, 2, \ldots, A\}$, where $A$ is the number of different adaptive alleles possible at each locus.

Allele $0$ represents a lack of adaptation, while non-zero alleles signify two types of adaptations, both of which increase fitness.
First, adaptations to the *external environment* confer a fitness benefit $\delta$.
This selective value is the same regardless of which non-zero allele is present.
We assume $\delta > c$, which allows a minimally adapted cooperator to recoup the cost of cooperation and gain a fitness advantage.


### Niche Construction and Selective Feedbacks

Individual fitness is also affected by aspects of the local environment that are modified by organisms.
This constructed "niche" depends on the specific allelic states present in the subpopulation.
As allelic states change, the subpopulation alters its environment in new ways, creating a unique niche.
As described below, the specific alleles at each locus become important.

In our model, the feedback that results from niche construction takes the form of density dependent selection, and populations evolve to better match the constructed niche.
We do not represent this niche explicitly, but rather allow the allelic composition of the subpopulation to feed back to affect selection.
Specifically, the selective value of non-zero allele $a$ at adaptive locus $l$---and consequently the fitness of an individual carrying that allele---increases with the number of individuals in the subpopulation that have allele $a-1$ at locus $l-1$.
For example, if $L=5$, $A=6$, and allele $4$ has fixed at locus $2$, then selection favors genotypes with allele $5$ at locus $3$.
And as allele $5$ becomes more abundant at locus $3$, the niche that this population constructs will increasingly favor allele $6$ at locus $4$ (see [Box 1](#box1)).
As a consequence, genotypes with sequentially increasing allelic states will tend to evolve.

We treat both adaptive loci and their non-zero allelic states as "circular": the selective value of an allele at locus 1 is affected by the allelic composition of the subpopulation at locus $L$.
Similarly, the selective value of allele 1 at any locus increases with the number of individuals carrying allele $A$ at the previous locus.
This circularity is represented by the function $\beta(x,X)$, which gives the integer that is below an arbitrary value $x$ in the set $\{1, 2, \ldots, X\}$:

$$ \beta(x, X) = \bmod_{X}(x - 2 + X) + 1 $$ {#eq:beta}

Here, $\bmod_{X}(x)$ is the integer remainder when dividing $x$ by $X$.
For example, $\beta(3, 5)$ is 2, while $\beta(1, 5)$ is 5.
Using this function, the selective value of allele $a$ at adaptive locus $l$ increases by $\epsilon$ for each individual in the subpopulation that has allele $\beta(a,A)$ at locus $\beta(l, L)$.
Thus, $\epsilon$ specifies the intensity of selection due to niche construction.


### Individual Fitness

For an individual with allelic state $a_{l}$ at locus $l$, fitness is defined as:

$$ W = z - \underbrace{c a_{0}}_{{\substack{\text{cost of} \\ \text{cooperation}}}} + \underbrace{\delta \sum_{l=1}^{L} I(a_{l})}_{\substack{\text{adaptation to} \\ \text{external environment}}} + \underbrace{\epsilon \sum_{l=1}^{L} n(\beta(a_{l}, A), \beta(l, L))}_{\substack{\text{adaptation to} \\ \text{constructed environment}}} $$ {#eq:fitness}

where $z$ is a baseline fitness, $n(a,l)$ is the number of individuals in the subpopulation with allele $a$ at locus $l$, and $I(a)$ indicates whether a given allele is non-zero:

$$
I(a) =
\begin{cases}
    1 & \text{if }a \in \{1,2,\ldots,A\} \\
    0 & \text{otherwise}
\end{cases}
$$ {#eq:IA}

Thus, an individual's fitness is determined both by adaptations to the external environment and by adaptations to its constructed environment.
[Box 1](#box1) illustrates the process of adaptation to the constructed environment.
While the separation between exogenous and endogenous environmental change may not always be as clearly differentiated in natural systems, it allows us to directly explore the effects of niche construction.


### Subpopulation Growth and the Benefit of Cooperation

The effects of cooperation are independent of the external and constructed components of the environment and do not provide direct fitness benefits (Equation @eq:fitness).
Instead, cooperation enables a subpopulation to reach a greater density.
If $p$ is the proportion of cooperators present at the beginning of a growth cycle, then that subpopulation reaches size $S(p)$, where:

$$ S(p) = S_{min} + p (S_{max} - S_{min}) $$ {#eq:popsize}

$S_{min}$ and $S_{max}$ define the sizes reached by all-defector and all-cooperator subpopulations, respectively.
This benefit affects all individuals equally and accumulates linearly with the proportion of cooperators in the subpopulation.
We also explore non-linear benefit accumulation in the Supplementary Material.
Because cooperators improve group productivity (Equation @eq:popsize) but decrease in proportion within mixed groups (Equation @eq:fitness), this form of cooperation would also qualify as "multi-level altruism" (see Supplementary Material and @kerr2004what).

Individuals compete as subpopulations grow.
Each individual's probability of reproductive success is proportional to its fitness.
The composition of a subpopulation with size $P$ and cooperator proportion $p$ after growth is multinomial with parameters $S(p)$ and $\{\pi_1, \pi_2, \ldots, \pi_{P}\}$, where $\pi_{i}$ represents the reproductive fitness of individual $i$ relative to others in its subpopulation (Equation @eq:fitness).


### Mutation

For simplicity, we apply mutations to new offspring after subpopulation growth.
Mutations occur independently at each locus and cause an allelic state change.
At the binary cooperation locus, mutations occur at rate $\mu_{c}$.
These mutations flip the allelic state, causing cooperators to become defectors and vice versa.
Mutations occur at rate $\mu_{a}$ at each adaptive locus.
These mutations replace the existing allele with a value randomly sampled from the set $\{0, 1, \ldots, A\}$.


### Migration

Populations consist of $N^2$ patches arranged as an $N \times N$ lattice, where each patch can support a subpopulation.
After mutation, individuals emigrate to an adjacent patch.
This process is unaffected by fitness.
For each source subpopulation, a single destination patch is randomly chosen from the source patch's Moore neighborhood, which encompasses the nearest 8 patches on the lattice.
Because the population lattice has boundaries, patches located on the periphery have smaller neighborhoods.
Individuals emigrate with probability $m$, which means larger subpopulations produce more emigrants.
Through immigration, subpopulations can exceed $S_{max}$ individuals.
As described below, however, this increase in subpopulation size is temporary.


### Population Initialization, Dilution, and Simulation Cycle

Following @HANKSHAW, we begin simulations with sparse populations.
Subpopulations are first seeded at all patches with cooperator proportion $p_{0}$ and size $S(p_{0})$.
The population is then thinned.
Each individual survives this bottleneck with probability $\sigma_{i}$.
Starting from this initial state, simulations then proceed for $T$ cycles, where each discrete cycle consists of subpopulation growth, mutation, migration, and dilution.
Dilution reduces each subpopulation to support growth in the next cycle.
Each individual survives dilution with probability $\sigma_{d}$, regardless of its genotype.
Dilution remains the same for each of the simulations described, however we further explore its effects in the Supplementary Material.


## Simulation Source Code and Software Dependencies

The simulation software and configurations for the experiments reported are available online [@connelly2015nicheconstruct].
Simulations used Python 3.4, NumPy 1.9.1, Pandas 0.15.2 [@mckinney2010data], and NetworkX 1.9.1 [@hagberg2008exploring].
Data analyses were performed with R 3.2.2 [@rproject].
Reported 95\% confidence intervals were estimated by bootstrapping with 1000 resamples.

