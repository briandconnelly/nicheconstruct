# Results

## Niche Construction Maintains Cooperation

Despite being able to form larger populations, cooperators are swiftly eliminated in competition with defectors, despite spatial structuring in the metapopulation (Figure 1A). As demonstrated by @HANKSHAW, cooperators are temporarily bolstered by the ability to hitchhike along with non-social adaptations (Figure 1B). As shown in Figure 1C, we find that niche hiking can prolong cooperation, perhaps indefinitely (see [Table 1](#tables) for model parameters). (**TODO** describe the oscillations). We now explore this process further to identify the factors underlying this effect.


## Not Just Because of Additional Fitness from Epsilon (TODO title)

In our model, an individual's fitness is the product of two processes. First, mutations can engender environmental adaptations, which are represented by non-zero alleles. These adaptations create the transient lift in cooperation seen in Figure 1B. The second process that contributes to fitness is niche construction. Selection favors individuals with sequentially-increasing alleles. Because larger populations will have a greater effect on their environment, this benefit is density dependent. In our experiments, this positive niche construction contributed equally to fitness when all individuals shared the same allele in a population at maximum carrying capacity. To determine whether cooperation was maintained simply due to the higher selective values made possible by this second source of fitness, we compared our results against the results of experiments in which the ordering of alleles did not matter, and the fitness benefit provided by adaptation was doubled ($\epsilon=0$, $\delta=0.6$). That this doubling is an over estimate of the magnitude of fitness contributions that arise from niche construction, since these values would only occur in populations at maximum carrying capacity, which does not occur in the presence of defectors. Nevertheless, Figure 2 shows that higher selective values have little effect (columns A and C) and do not explain the maintenance of cooperation that we observe when niche construction occurs (column B).

Although we have seen that maximum fitness does not substantially effect the maintenance of cooperation, perhaps the rate at which fitness accumulates in cooperator and defector populations matters. When we compare the accumulation of fitness via adaptation in the presence of niche construction (Figure 3A) against simulations in which selective values are doubled (Figure 3B), two features emerge. In both scenarios, cooperators gain adaptations more quickly than defectors due to their size. When niche construction is not present, cooperator fitness is eventually surpassed by that of defectors (Figure 3B). As described by @HANKSHAW, this leads to the demise of cooperators. In contrast, cooperator fitness is never surpassed when niche construction is present (Figure 3A), which allows cooperation to persist.

**TODO: discuss time at which fitness plateaus?**

**TODO: describe how maximum fitness is calculated?**


## Negative Niche Construction Plays a Key Role (TODO title)

Figure 3A also shows that niche-constructing populations never reach maximum fitness. One major contributer to this is the density dependence of the benefit provided by niche construction. Because defectors remain present (Figure 1C), the smaller populations that result are unable to unlock the full benefit of niche construction. The second contributer to the reduced fitness that we observe is negative niche construction. This occurs in our model due to selection for sequentially-increasing allelic states and the circular arrangement of these alleles. When the genome length ($L$) is not evenly divided by the number of non-zero alleles ($a_{max}$), a conflict arises when the allelic state at locus $1$ is not 1 larger than the allelic state at locus $L$. For example, consider genotype $(1,2)$ when $L=2$ and $a_{max}=3$. Here, allelic state $2$ at locus 2 will be be beneficial, because it follows allelic state $1$ at locus 1. However, due to the circular effects, allelic state $1$ at locus 1 will be deleterious, because it does not follow $2$.

To isolate the effect of negative niche construction, we compare our results against those from simulations in which this allelic conflict was absent ($L=5$, $a_{max}=5$). Figure 2 shows that although positive niche construction still led to an increase in cooperation (column D), these populations were not able to maintain the same level of cooperation seen in the presence of negative niche construction (column B). We find that because this lack of conflict allows populations to reach a fully-adapted state, cooperators once again acquire these adaptations more quickly but are eventually driven from the population (Figures 3C and 1X). These results indicate that both positive and negative niche construction is required to maintain cooperation.

(**TODO: explain why defector fitness doesn't reach 4 (density dependent fitness)** maybe better in figure caption?)

To further explore the influence of negative niche construction, we performed experiments in which the positive effects of niche construction were removed. Here, individuals had a single adaptive locus that was constantly in conflict ($L=1$, $a_{max}=6$). As seen in Figures 2 (column E) and 3D, the constant source of adaptation that is provided by negative niche construction is not sufficient to maintain cooperation via hitchhiking, and cooperators are quickly purged from the population. This provides further evidence that feedbacks from both positive and negative niche construction are required for cooperation to persist.


## NC Enables Cooperator Spread

Figure 4

## NC Prevents Defector Invasion

Figure 5

## How Public Good Fuels all of this

Figure 6 A: effect of Smax-Smin, B: effect of migration rate

