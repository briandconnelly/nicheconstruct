\clearpage

# Figures

## Figure 1 {#fig1}

![**Adaptation to External and Constructed Environments.** (**A**) We begin with the case with five adaptive loci ($L=5$) and five non-zero alleles ($A=5$). All simulations are initialized with a non-adapted genotype with allele 0 at every locus (far left).  Random mutation will introduce a non-zero allele, which will increase in frequency. In this example, allele 1 arises at the first locus (in the "12 o’clock" position). The rest of this schematic focuses on niche construction. Every non-zero allele at any locus influences selection at the next locus in the clockwise direction. There is a "mismatch" in this genotype (highlighted by the red sector), because the niche constructed by allele 1 at the first locus favors allele 2, not 0, at its immediate clockwise neighbor (the second locus). Once the appropriate allele arises, it will be selected.  In this case, the genotype [1,2,0,0,0] receives an epsilon effect in addition to the extra delta.  The "match" at the first and second locus is highlighted as a green sector. However, now there is a new mismatch between the second and third locus, which a new round of mutation and selection corrects, and so on. The green sector grows as the red sector ticks clockwise. Importantly, because $A$ divides evenly into $L$, this genotype can evolve into a perfectly reinforcing sequence [1,2,3,4,5], which enjoys a maximal epsilon increment of fitness due to niche construction. (**B**) The case of negative niche construction is illustrated for the case of five loci ($L=5$) and six non-zero alleles ($A=6$). Here we start with a population fixed for the genotype on the far left [1,2,3,4,5]. There is a single mismatch in this genotype (highlighted by the red sector), because the niche constructed by allele 5 favors allele 6, not 1, at its immediate clockwise neighbor. If the fitter mutant [6,2,3,4,5] arises (see next genotype to the right), it will fix. (We note that the strength of selection will drop as its frequency increases). However, now there is a new mismatch in the genotype (highlighted again with a red sector). We see that correcting one mismatch generates a new mismatch.  Thus, this system will never escape its mismatches–--the red sector just clicks clockwise around the genome.  Indeed, after six (or $A$) rounds of mismatch correction and generation, we have ended back where we started with the original genotype turned clockwise by one locus. Here, the adaptation to previous niche construction generates further niche construction that leads to novel adaptation.](../figures/Figure1.pdf)

\clearpage

## Figure 2 {#fig2}

![**Adaptation, Hitchhiking, and the Evolution of Cooperation.** Curves show the average cooperator proportion among replicate populations for the duration of simulations, and shaded areas indicate 95% confidence intervals. Unless otherwise noted, parameter values are listed in [Table 1](#tables). (**A**) Without any opportunity to adapt ($L=0$), cooperation is quickly lost. (**B**) When adaptation can occur ($L=5$), but niche construction does not affect selection ($\epsilon=0$), cooperators rise in abundance by hitchhiking along with adaptions to the external environment. Nevertheless, this effect is transient, and cooperators eventually become extinct. (**C**) Niche construction enables cooperation to be maintained indefinitely. In the majority of populations, cooperation remained the dominant strategy. The trajectories of individual populations are shown in Figure 3A.](../figures/Figure2.png)

\clearpage


## Figure 3 {#fig3}

![**Niche Construction and the Evolution of Cooperation.** The proportion of cooperators present in each replicate population is shown for the duration of simulations. (**A**) Despite some oscillations, cooperation dominates in 13 of 18 populations when niche construction affects selection. (**B**) When the selective effects of niche construction ($\epsilon$) are removed, and the selective benefit of adaptation to the external environment ($\delta$) is increased to compensate, cooperators are driven to extinction by isogenic defectors that arise by mutation ($\epsilon=0$, $\delta=0.6$). Note that cooperation was not present after initialization in one replicate population. (**C**) Cooperators are also driven to extinction without negative niche construction ($A=5$).](../figures/Figure3.png)

\clearpage


## Figure 4 {#fig4}

![**Niche Construction and Invasion.** Curves trace the proportion of cooperators present in each replicate population for the duration of simulations ($T=1000$). In each simulation, a rare type was initiated at a single patch in the center of the population lattice ($N^{2}=121$). Unless otherwise noted, mutations are disabled in these ecological simulations to highlight the dynamics of invasion ($\mu_{a}=0, \mu_{c}=0$). (**A**) When cooperators and defectors are isogenic (i.e., both types have stress alleles [1,2,3,4,5]), rare defectors quickly invade and drive cooperators to extinction due to the cost of cooperation. Defectors were stochastically eliminated in 2 replicate populations. (**B**) However, negative niche construction creates adaptive opportunities that enable cooperators to resist invasion by isogenic defectors. Here, cooperation remained the dominant in 91 of 160 populations ($\mu_{a}=0.00005$). Results from simulations where mutations also occurred at the cooperaiton locus are shown in Figure S1. (**C**) In fact, an adapted cooperator type (stress alleles [6,2,3,4,5], see Figure 1) can swiftly displace defectors when isogenic defectors cannot arise or adapt via mutation.](../figures/Figure4.png)

\clearpage

## Figure 5 {#fig5}

![**Cooperator Adaptation Prevents Defector Invasion.** Here we depict the distribution of dominant types among subpopulations over time for one representative simulation in which isogenic defectors arise. To highlight the effects of adaptation, mutations did not occur at the cooperation locus ($\mu_{c}=0$). At time $t=0$ (upper left panel), a single isogenic defector population (red) is placed among cooperator populations (light blue). Because these defectors do not bear the costs of cooperation, they spread ($t=272$). However, cooperators in one population gain an adaptation that gives them a fitness advantage over defectors (second panel, dark blue, lower left). At $t=325$, defectors continue to invade cooperator populations. However, the adapted cooperator type spreads more quickly due to its fitness advantage, invading both defector populations and ancestral cooperator populations ($t=390$), until it eventually fixes in the population ($t=500$). At $t=690$, a new cooperator type emerges that is favored due to negative niche construction (orange). This new type spreads rapidly ($t=812$) until reaching fixation ($t=900$). At this point, it becomes susceptible to invasion by the next "adapted" cooperator type, and the cycle continues.](../figures/Figure5.pdf)

\clearpage


\renewcommand{\thefigure}{S\arabic{figure}}
\setcounter{figure}{0}

## Supplemental Figure 1 {#figS1}

![**Defector Invasion with Mutations.** The proportion of cooperators present in each replicate population is shown for the duration of simulations ($T=1000$). When mutations occur both at the adaptive loci and the cooperation locus ($\mu_{a}=\mu{c}=0.00005$), cooperation remains dominant in 58 of 160 replicate populations.](../figures/FigureS1.png)

\clearpage

