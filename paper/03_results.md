# Results

We use the model described earlier to follow the evolution of cooperation in a metapopulation of populations that are connected by spatially-limited migration.
Individuals in these populations gain a limited number of adaptations that confer selective benefits.
Adaptation is independent of cooperation.
However, because cooperation increases population density, these populations experience more mutational opportunities to gain adaptations.
Cooperation can hitchhike along with these adaptations, which compensate for the cost of public good production.
During this process, populations alter their environment.
This niche construction process can be either positive or negative, depending on its effects on fitness.
Here, we explore how niche construction can favor the evolution of cooperation.
Our simulation environment is defined by the parameter values listed in [Table 1](#tables).
Unless otherwise noted, 10 replicate simulations were performed for each experiment.



## Niche Construction Maintains Cooperation

Without any opportunity for adaptation ($L=0$), cooperators are swiftly eliminated in competition with defectors (Figure 1). Despite an initial lift due to increased productivity, the cost of cooperation becomes disadvantageous as migration mixes the initially isolated populations. When there are opportunties for adaptation ($L=5$, $\epsilon=0$), cooperators are maintained transiently (Figure 1B). Here, the additional mutational abilities provided by their larger sizes allows cooperator populations to more quickly adapt to their environment. As previously described by @HANKSHAW, however, cooperation is subsequently lost as defector populations become equally adapted. When populations affect their environment and these changes feed back on selection, cooperation persists (Figure 1C, 3A). In these environments, cooperators maintain higher fitness than cooperators, which enables their survival (Figure 3A).


## Fitness Increases do not Support Cooperation

In our model, niche construction introduces additional selective benefits. To determine how these selective effects influence evolutionary outcomes, we performed simulations in which the selective effects of niche construction were removed ($\epsilon=0$). As compensation, we increased the fitness benefits conferred by adaptation ($\delta=0.6)$. Here, the selective effects of niche construction are exaggerated, as a fitness benefit of 0.3 (our increase in $\delta$) is the maximum value possible (see @eq:fitness). To quantify cooperator success and permit comparison, we use the area under the cooperator proportion curve. This measure of *cooperator presence* increases as cooperators rise in abundance or remain in the population longer.

We find that higher selective values do not provide a significant increase in cooperator presence (Figure 2, column C). As shown in Figure 3, cooperators gain adaptations more quickly than defectors, which provides a fitness advantage. However, the cost of cooperation puts defectors at an advantage once these populations become fully adapted.


## Positive Niche Construction Prolongs Cooperation

Negative niche construction occurs in our model due to selection for sequentially-increasing allelic states and the circular arrangement of these alleles. When the genome length ($L$) is not evenly divided by the number of adaptive alleles ($A$), a conflict arises when the allelic state at locus $1$ is not 1 larger than the allelic state at locus $L$. For example, consider genotype $(1,2)$ when $L=2$ and $A=3$. Here, allelic state $2$ at locus 2 will be be beneficial, because it follows allelic state $1$ at locus 1. However, due to the circular effects, allelic state $1$ at locus 1 will be deleterious, because it does not follow $2$.

We first focus on the effects of positive niche construction by removing the allelic conflict that leads to negative niche construction ($L=5$, $A=5$).
In the absence of this conflict, cooperator presence is significantly increased (Figure 2, column D).
Within these environments, we find that positive niche construction prolongs the fitness advantage that cooperators have over defectors (Figure 3C).
Nevertheless, cooperators are eventually driven to extinction once defectors gain the fitness advantage. 


## Negative Niche Construction is not Sufficient

To determine how negative niche construction influences the evolution of cooperation, we maximize the allelic conflict ($L=1$, $A=6$).
Here, selection for increasing allelic states among the stress loci means that any allelic state will not be greater than at the previous allele (itself), and thus there will always be opportunity for adaptation.
Despite this constant opportunity, niche construction does not increase cooperator presence (Figure 2, column E). Here, defectors rapidly gain the fitness advantage.


## NC Enables Cooperator Spread

Figure 4
- if not, could be why thinning is a must.


## NC Prevents Defector Invasion

Figure 5


## How Public Good Fuels all of this

To directly explore how the increase in population size affects evolutionary outcomes, we vary the maximum size that a population can reach ($S_{max}$, see Equation @eq:popsize). Figure 6A shows the result of these simulations. (**TODO** description of results)

To address how migration affects the evolutionary process in this system, we vary the rate at which migration occurs ($m$). As seen in Figure 6B, cooperation decreases as migration rate increases. This is likely because migration defines the spatial structuring in this system. As migration increases, the population becomes more like a well-mixed system, where defectors are better able to exploit the benefits of cooperation [@griffin2004cooperation; @kummerli2009viscous].
