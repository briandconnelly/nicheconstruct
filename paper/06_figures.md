\clearpage

# Figures

## Figure 1 {#fig1}

![**Adaptation to External and Constructed Environments.** (**A**) We start with the case with five loci ($L=5$) and five non-zero alleles ($A=5$). All simulations are initialized with a non-adapted genotype with allele 0 at every locus---the genotype on the far left.  Random mutation will introduce a non-zero allele, which is expected to increase in frequency. For simplicity, we assume that allele 1 arises at the first locus (in the "12 o’clock" position). The rest of this schematic focuses on niche construction. Every non-zero allele at any locus influences selection at the next locus in the clockwise direction. There is a "mismatch" in this genotype (highlighted by the red sector) because the niche constructed by allele 1 at the first locus favors allele 2 (not 0) at its immediate clockwise neighbor (the second locus). Once the appropriate allele arises, it will be selected.  In this case, the genotype [1,2,0,0,0] receives an epsilon effect in addition to the extra delta.  The "match" at the first and second locus is highlighted as a green sector. However, now there is a new mismatch (between the second and third locus), which a new round of mutation and selection corrects, and so on.  The green sector grows as the red sector ticks clockwise.  Importantly, because A divides evenly into L, this genotype can evolve into a perfectly reinforcing sequence [1,2,3,4,5], which enjoys an maximal epsilon increment of fitness of due to its niche construction.  (**B**) The case of negative niche construction is illustrated for the case of five loci ($L=5$) and six non-zero alleles ($A=6$). Here we start with a population fixed for the genotype on the far left [1,2,3,4,5]. There is a single mismatch in this genotype (highlighted by the red sector) because the niche constructed by allele 5 favors allele 6 (not 1) at its immediate clockwise neighbor.  If the fitter mutant [6,2,3,4,5] arises (see next genotype to the right), it will fix. (We note that the strength of selection will drop as its frequency increases).  However, now there is a new mismatch in the genotype (highlighted again with a red sector). Thus, we see that correcting one mismatch generates a new mismatch.  Thus, this system will never escape its mismatches– the red sector just clicks clockwise around the genome.  Indeed, after six (or $A$) rounds of mismatch correction/generation, we have ended back where we started with the original genotype turned clockwise by one locus.  Here, the adaptation to previous niche construction generates further niche construction that leads to novel adaptation.](../figures/Figure1.pdf)

\clearpage

## Figure 2 {#fig2}

![**Adaptation, Hitchhiking, and the Evolution of Cooperation.** The proportion of cooperators present in the population is shown for the duration of simulations. Curves show the average among replicate populations, and shaded areas indicate 95% confidence intervals. Unless otherwise noted, parameter values are listed in [Table 1](#tables). (**A**) Without any opportunity to adapt ($L$, the number of adaptive loci, is zero), cooperation is quickly lost. (**B**) When adaptation can occur ($L=5$), but populations do not alter their environment ($\epsilon$, the intensity of niche construction, is zero), cooperation hitchhikes along with adaptions, allowing cooperators to temporarily rise in abundance before eventually going extinct. (**C**) Niche construction enables cooperation to be maintained indefinitely. In the majority of populations (13/18), cooperation remained the dominant strategy. Individual populations are shown in Figure 3A.](../figures/Figure2.png)

\clearpage


## Figure 3 {#fig3}

![**Niche Construction and the Evolution of Cooperation.** The proportion of cooperators present in each replicate population is shown for the duration of simulations. (**A**) Dispite some oscillations, niche construction enables cooperation to be maintained indefinitely in 14 of 18 populations. (**B**) When niche construction is removed and the fitness benefit of adaptation is increased to compensate ($\epsilon=0$, $\delta=0.6$), adapted defectors arise and drive cooperators to extinction. (**C**) Without negative niche construction, cooperation is not maintained ($A=5$).](../figures/Figure3.png)

\clearpage


## Figure 4 {#fig4}

![**Niche Construction and Invasion.** Curves trace the proportion of cooperators present in the population for the duration of 160 replicate simulations ($T=1000$). These experiments examine whether a rare cooperator or defector strategy can invade when initiated at a single patch in the center of the population lattice ($N^{2}=121$). Unless otherwise noted, mutations ($\mu_{a}=0, \mu_{c}=0$) are disabled in these ecological simulations to highlight the dynamics of invasion. The results from simulations where this limitation is remoed are shown in Figure S1. (**A**) When cooperators and defectors are isogenic (i.e., both types have stress alleles [1,2,3,4,5]) and mutation cannot occur, rare defectors quickly invade and drive cooperators to extinction due to the cost of cooperation. Defectors were stochastically eliminated in 2 replicate populations. (**B**) However, the adaptive opportunities produced by negative niche construction can allow cooperators to resist invasion by isogenic defectors. Here, cooperation persisted in the majority of populations ($\mu_{a}=0.00005$, the base mutation rate). (**C**) We demonstrate that adaptations such as these can enable an cooperator (stress alleles [6,2,3,4,5], see Figure 1) to displace a population of defectors when defectors cannot arise or adapt via mutation.](../figures/Figure4.png)

\clearpage

## Figure 5 {#fig5}

![**Defector Invasion Stopped by Cooperator Adaptation.** Here we depict the distribution of dominant types among populations over time for one representative simulation in which isogenic defectors arise. For clarity, mutations occurred at the adaptive loci, but not at the cooperation locus ($\mu_{c}=0$) during this ecological simulation. A time $t=0$ (leftmost panel), a single matched defector population (red) is placed among cooperator populations (light blue). Because these defectors do not bear the costs of cooperation, they spread ($t=272$, second panel). However, cooperators in a single population gain an adaptation that give them a fitness advantage over defectors (dark blue, lower left). At $t=325$ (third panel), defectors continue to invade cooperator populations. However, the adapted cooperator type, which can invade both defector populations and ancestral cooperator populations, can spread more quickly due to its greater fitness. Eventually, this strategy spreads and fixes in all populations (rightmost panel) until this strategy itself is replaced by the next adaptation.](../figures/Figure5.pdf)

\clearpage

## Figure 6 {#fig6}

**TODO** Yep. Almost ready.


\clearpage

\renewcommand{\thefigure}{S\arabic{figure}}
\setcounter{figure}{0}

## Supplemental Figure 1 {#figS1}

![**Defector Invasion with Mutations.** With mutations occurring both at the adaptive loci and the cooperation locus ($\mu_{a}=\mu{c}=0.00005$), cooperation remains the dominant strategy in 58 replicate simulations. Curves trace the proportion of cooperators present in the population for the duration of 160 replicate simulations ($T=1000$)](../figures/FigureS1.png)

\clearpage

