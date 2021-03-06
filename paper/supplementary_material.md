---
title: Supplementary Material for "Negative Niche Construction Favors the Evolution of Cooperation"
geometry: margin=1.0in
fontsize: 12pt

# NOTE: can't cross reference within a figure legend.
...

\renewcommand{\thefigure}{S\arabic{figure}}
\renewcommand{\theequation}{S\arabic{equation}}
\setcounter{figure}{0}
\setcounter{equation}{0}

\vspace{-5em}
\begin{center}
Brian D. Connelly\textsuperscript{1,3}, Katherine J. Dickinson\textsuperscript{1}, Sarah P. Hammarlund\textsuperscript{1,2}, and \mbox{Benjamin Kerr\textsuperscript{1,3}}
\vspace{3em}

\textsuperscript{1}Department of Biology and BEACON Center for the Study of Evolution in Action, University of Washington, Seattle, Washington, 98195, USA

\textsuperscript{2}Current Address: Department of Zoology, University of Oxford, Oxford OX1 3PS, \mbox{United Kingdom}

\textsuperscript{3}E-mail: bdcx@uw.edu and kerrb@uw.edu
\end{center}

\vspace{2em}
\begin{shaded}
    \vspace{-1.5em}
    \footnotesize
    \tableofcontents
    \normalsize
    \vspace{0.5em}
\end{shaded}
\clearpage


# Effect of Initial Cooperator Proportion

For most of the simulations described both in the paper and in this supplement, cooperators are at equal abundances as defectors when populations are initiated ($p_0=0.5$).
Here, we perform simulations with different initial cooperator proportions to explore how this parameter affects the evolution of cooperation in our model.
When rare, cooperators do not fare well under baseline conditions (Figure @fig:initial_coop_prop).
As the initial cooperator proportion increases, cooperators dominate in more replicate populations.
Although cooperators continually arise via mutation, they do not invade when initially absent or very rare.

To quantify cooperator success during simulations, we use the area under the cooperator proportion curves.
As cooperators spend more time at high proportions, this *cooperator presence* metric increases.
Figure @fig:initial_coop_prop_int shows that cooperator presence increases as initial cooperator proportions become greater.
Here, we show the proportion of cooperators after the initial populations are thinned ($\sigma_i$).

![**Effect of Initial Cooperator Proportion.** Each panel shows the proportion of cooperators present in populations initiated with a different initial cooperator proportion ($p_0$). When cooperators are initially absent ($p_0=0$), they arise, but never reach significant abundances under baseline conditions (here, 100 replicates shown). Cooperation is maintained and dominates in a greater number of replicate populations when the initial cooperator proportion increases (20 replicates each). Here, lines show the trajectories of replicate populations.](../figures/initial_coop_prop.png) {#fig:initial_coop_prop}

![**Effect of Initial Cooperator Proportion on Cooperator Presence.** As the proportion of cooperators present in the population after initial thinning increases, the cooperator presence, or the area under the cooperator proportion curve, increases. Open circles represent the cooperator presence in replicate populations. The initial cooperator proportion is the proportion of cooperators present after the population is initialized and thinned. The solid line is a Loess curve fitted to these values with shaded 95% confidence interval.](../figures/initial_coop_prop-integral.png) {#fig:initial_coop_prop_int}


# Effect of Subpopulation Dilution

In our model, subpopulations are thinned at the end of each time step, which allows for growth during the next cycle.
For the simulations described in the main text, the probability that each individual survived this bottleneck was fixed ($\sigma_d=0.1$).
To explore how this factor affects the evolution of cooperation in our model, we performed simulations with varying dilution survival probabilities.
Importantly, because dilution determines the amount of growth that can occur in the next simulation cycle, it directly affects the number of mutational opportunities that populations have.
When more individuals survive dilution events, growth is reduced, and populations adapt more slowly.
To compensate for this effect and ensure equal adaptive opportunities, we first calculated the average number of births that occur during simulations with baseline parameter values.
Simulations were then run until populations surpassed this number, or approximately $2.8 \times 10^9$ births.
As more individuals survive periodic dilution, cooperation is more likely to be outcompeted (Figures @fig:dilution_births and @fig:dilution_births_int).


![**Effect of Subpopulation Dilution.** Each panel shows the proportion of cooperators present for the duration of simulations with different dilution survival probabilities ($\sigma_d$), shown on the right. Because thinning affects the number of offspring produced during each cycle, and hence the number of mutational opportunities to gain adaptations, simulations proceeded until populations had reached $2.8 \times 10^9$ births, which was the average number of births that occurred in simulations with baseline parameter values over 3000 cycles. As the probability of survival increases, defectors pose a greater threat. Here, lines show the trajectories of replicate populations.](../figures/dilution-births.png) {#fig:dilution_births}

![**Subpopulation Dilution and Cooperator Presence**. Cooperator presence rapidly decreases as the probability of surviving periodic dilution ($\sigma_d$) increases. Here, the integration at each dilution survival probability is done over an equivalent number of births instead of Time, as before. Solid points indicate the average cooperator presence among replicate populations (open circles), and error bars indicate 95% confidence intervals.](../figures/dilution-births-integral.png) {#fig:dilution_births_int}



# Non-Linear Benefits of Cooperation

In our main simulations, the carrying capacity at each patch increased linearly with the proportion of cooperators.
We allow this relationship to be non-linear by expanding Equation 4 in the following way:

$$ S(p) = S_{min} + p^{\gamma} (S_{max} - S_{min}) $$ {#eq:popsizegamma}

The additional parameter $\gamma$ affects the *shape* of the function that defines how the presence of cooperators increases the local carrying capacity.
As illustrated in Figure @fig:nonlinear_benefits_gamma, subpopulation productivity has diminishing returns when $\gamma < 1$ and accelerating returns when $\gamma > 1$.
When $\gamma = 1$, Equation @eq:popsizegamma is equivalent to Equation 4, and carrying capacity increases linearly with cooperator proportion.

![**$\gamma$ and the Shape of Cooperative Benefits**](../figures/nonlinear_benefits-gamma.png) {#fig:nonlinear_benefits_gamma}

Figures @fig:nonlinear_benefits and @fig:nonlinear_benefits_int show how the the shape of the increase in this cooperative benefit affects the evolution of cooperation in our model under baseline conditions (Table 1).
While diminishing returns are detrimental to cooperation, accelerating returns tend to promote cooperation.

![**Effect of Non-Linear Cooperative Benefits.** Cooperators rapidly rise in frequency when the benefits have accelerating returns ($\gamma > 1$). When the increases in subpopulation carrying capacity have diminishing returns ($\gamma < 1$), the proportion of cooperators oscillates more frequently, which can allow defectors to fix. Here, each panel shows cooperator proportion for the duration of simulations in which the relationship between cooperation and increases in carrying capacity were varied ($\gamma$, indicated on the right). Lines show the trajectories of replicate populations.](../figures/nonlinear_benefits.png) {#fig:nonlinear_benefits}

![**Non-Linear Cooperative Benefits and Cooperator Proportion.** As the slope of the curve defining the benefits of cooperation becomes more convex, cooperators are maintained at higher abundances and for longer. Cooperator presence represents the area under the cooperator proportion curves shown in Figure S6. Solid points indicate the average scaled cooperator presence among replicate populations (open circles), and error bars indicate 95% confidence intervals.](../figures/nonlinear_benefits-integral.png) {#fig:nonlinear_benefits_int}

\FloatBarrier

# A Measure of Expected Absolute Fitness within a Subpopulation

For the following description, we ignore mutation and focus on selection in our model. We define fitness of genotype $g$ within a subpopulation to be:

$$ W_g = z - c a_{0,g} + \delta \sum_{l=1}^{L} I(a_{l,g}) + \epsilon \sum_{l=1}^{L} n(\beta(a_{l,g}, A), \beta(l, L)) $$ {#eq:absfitness}

where $a_{l,g}$ is the allelic state at locus $l$ of genotype $g$, and all other terms are described in the main text.
We let $N_g$ be the number of individuals in the subpopulation with genotype $g$.
After selection, the expected fraction of the subpopulation that has genotype $g$ is:

$$ F_{g} = \frac{N_g W_g}{\sum_{i \in \mathbf{G}}^{} N_i W_i} $$

where $\mathbf{G}$ is the set of all genotypes in the subpopulation of interest.
Total subpopulation size after selection is

$$ S = S_{min} + \frac{\sum_{i \in \mathbf{G}}^{} N_i a_{0,i}}{\sum_{i \in \mathbf{G}}^{} N_i} (S_{max} - S_{min}) $$ {#eq:popsize2}

where the proportion of cooperators is $p = (\sum_{i \in \mathbf{G}}^{} N_i a_{0,i})/(\sum_{i \in \mathbf{G}}^{} N_i)$.
Thus, if $X_g$ is a random variable giving the number of individuals after selection with genotype $g$, then

$$ \text{Pr}\{X_g = x\} = \binom{S}{x} (F_g)^x (1-F_g)^{S-x} $$

where $x \in \{0,1,2,\ldots,S\}$. The expected number of individuals of genotype $g$ after selection is:

$$ E[X_g] = F_g S $$

The quantity

$$ \omega_g = \frac{E[X_g]}{N_g} $$

serves as the (expected) absolute fitness of genotype $g$ in the subpopulation of interest.
We note that this absolute fitness value only depends on the genotypic composition of the subpopulation (the members of the set $\mathbf{G}$ and their numbers in the subpopulation) and the parameters of the model ($z$, $c$, $\delta$, $\epsilon$, $S_{min}$, $S_{max}$).
By summing $E[X_g]$ over all the subpopulations (which can differ in genotypic composition), and dividing by the sum of $N_g$ over all subpopulations, we can arrive at the expected absolute fitness of genotype $g$ at the scale of the entire metapopulation.

We note that mutation will complicate this derivation because a fraction of the individuals with genotype $g$ after selection will mutate into another genotype, while a fraction of other genotypes may mutate into genotype $g$.
At a metapopulation scale, migration does not change the absolute fitnesses of genotypes, however, it can alter genotypic composition of subpopulations and therefore affect the absolute fitnesses of genotypes in the next generation.


# Altruism

There have been several different definitions of altruism, with complicated connections between them (see @kerr2004what).
In our model, we have a form of "multilevel altruism", which requires altruists have lower fitness within a subpopulation, but subpopulation productivity increases with altruist proportion.
To see this, consider a subpopulation with only two genotypes $g_c$ and $g_d$, where $a_{0,g_c} = 1$, $a_{0,g_d} = 0$, and $a_{l,g_c} = a_{l,g_d}$ for all $l \in \{1, 2, \ldots, L\}$.
Specifically, genotype $g_c$ refers to a cooperator, genotype $g_d$ refers to a defector, and otherwise the two genotypes are identical.
By Equation @eq:absfitness, $W_{g_{c}} < W_{g_{d}}$, which implies $\omega_{g_{c}} < \omega_{g_{d}}$.
That is, the cooperator always has fewer expected number of offspring than an isogenic defector within its subpopulation.
However, Equation @eq:popsize2 guarantees that the productivity of the subpopulation increases with the proportion of cooperators.
Thus, cooperators qualify as multilevel altruists.
With additional constraints on the parameters, cooperation could also satisfy other definitions of altruism (e.g., "individual-centered altruism" or "focal-complement altruism", see @kerr2004what).
However, to keep things general, we have not assumed these constraints.
To avoid confusion between these different forms of altruism, we have opted to use the more general term “cooperation” in our manuscript.


# Relative Versus Absolute Fitness

Consider a subpopulation fixed for genotype [1,2,3,4,5] where $A=6$ (our "negative niche construction" scheme).
Now, imagine a mutant genotype [6,2,3,4,5] arises.
This mutant has a higher expected absolute fitness than its ancestor (i.e., $W_{[6,2,3,4,5]} > W_{[1,2,3,4,5]}$).
As the mutant increases in proportion, its expected absolute fitness decreases.
However, regardless of the proportions, the relative fitness of the mutant is always greater than its ancestor (i.e., the expected absolute fitness of the mutant is greater than the expected absolute fitness of the ancestor).

Now, as this mutant starts to dominate, a door begins to open for a second mutant genotype, [6,1,3,4,5], to invade.
Importantly, when [6,2,3,4,5] first arises (and [1,2,3,4,5] still dominates), this second mutant [6,1,3,4,5] would perform poorly relative to [6,2,3,4,5].
However, as the genotype [6,2,3,4,5] starts to dominate, the environment it constructs raises the expected absolute fitness of the second mutant [6,1,3,4,5].
Eventually, the relative fitness of this new mutant becomes greater than its ancestor.
In general, as any genotype starts to dominate, it raises the relative fitness of a different genotype.
In this sense, we treat the niche construction as "negative", as the more individuals of a given genotype are constructing the environment, the lower the fitness of these constructors relative to the new favored mutant genotype.


# Defector Invasion with Mutations at the Cooperation Locus

In the main text, Figures 3b and 4 showed that the adaptive opportunities provided by negative niche construction can allow cooperators to resist invasion by defectors.
For simplicity, mutations did not occur at the cooperation locus in these simulations, which eliminated the threat of defectors arising from adapted cooperators.
However, we found that when this challenge is present, and mutations can occur at the cooperation locus ($\mu_{c}=0.00005$), cooperators can still resist invasion ([Figure S8](@fig:dinvade2)).

![**Defector Invasion with Mutations.** The proportion of cooperators present in each replicate population is shown for the duration of simulations ($T=1000$). When mutations occur both at the adaptive loci and the cooperation locus ($\mu_{a}=\mu_{c}=0.00005$), cooperation remains dominant in 58 of 160 replicate populations.](../figures/defector_invasion_mu.png) {#fig:dinvade2}


\clearpage

# References

