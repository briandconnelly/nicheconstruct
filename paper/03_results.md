# Results

Using the model described in the previous section, we perform simulations that follow the evolution of cooperation in a metapopulation consisting of populations connected by spatially-limited migration.
Individuals compete in these populations by gaining a limited number of adaptations that confer fitness benefits.
While cooperation does not directly affect the selective value of these adaptations, cooperation can have indirect effects on the adaptive process.
Specifically, cooperation increases population density. As a result, larger populations of cooperators experience more mutational opportunities to gain adaptations. 
Cooperation can hitchhike along with these adaptations, which compensate for the cost of cooperation.
During this process, populations alter their local environments, which, in turn, affects selection.
Here, we explore how niche construction influences the evolution of cooperation in the simulation environment defined by the parameter values listed in [Table 1](#tables).


## Niche Construction Maintains Cooperation

Without any opportunity for adaptation ($L=0$), cooperators are swiftly eliminated in competition with defectors (Figure 1A).
Despite an initial lift due to increased productivity, the cost of cooperation becomes disadvantageous as migration mixes the initially isolated populations.
When there are opportunties for adaptation ($L=5$) but no niche construction ($\epsilon=0$), cooperators are maintained transiently (Figure 1B).
Here, larger cooperator populations can more quickly adapt to their environment.
As previously described by @HANKSHAW, however, cooperation is subsequently lost once populations become fully adapted to their environment.
Once this has occurred, adapted defectors that arise via mutation at the cooperation locus have a selective advantage and drive cooperators from the population.
However, when niche construction creates selective feedbacks, cooperation persists in 13 of 18 replicate populations (Figure 2A).


## Fitness Increases Alone do not Support Persisting Cooperation

In our model, niche construction introduces additional selective benefits.
To determine how these selective effects influence evolutionary outcomes, we performed simulations in which the selective effects of niche construction were removed ($\epsilon=0$), and we instead increased the fitness benefits conferred by adaptation ($\delta=0.6)$.
Here, we are consevative by lifting the selective value of exogenous adaptation by the maximum value possible from niche construction.

We find that higher selective values do not provide a significant increase in cooperator presence (Figure 2B).
As shown in Figure 3, cooperators gain adaptations more quickly than defectors, which provides a fitness advantage.
However, the cost of cooperation puts defectors at an advantage once these populations become fully adapted.


## Negative Niche Construction is Critical to Cooperator Persistence

Negative niche construction occurs in our model due to selection for sequentially-increasing allelic states and the circular arrangement of these alleles.
When the genome length ($L$) is not evenly divided by the number of adaptive alleles ($A$), then it is not possible for the population to be fixed for a genotype that is perfectly adapted to the constructed environment.
Technically (in terms of the model) this is because the equality: 

$$
\beta(a_{g,l}, A) = a_{g,\beta(l,L)}
$$

cannot simultaneously hold for all $l$.

For example, consider genotype $(1,2)$ when $L=2$ and $A=3$. Here, allelic state 2 at locus 2 will be be beneficial, because it follows allelic state 1 at locus 1.
However, due to the circular effects, allelic state 1 at locus 1 will be deleterious relative to allelic state 3 at locus 1.
Yet, fixation for genotype $(3,2)$ does not solve the problem, because a mutant $(3,1)$ is fitter, and so on. 

We first focus on the effects of positive niche construction by removing the allelic conflict that leads to negative niche construction ($L=5$, $A=5$).
In the absence of this conflict, cooperator presence is significantly increased (Figure 2C).
Within these environments, we find that positive niche construction prolongs the fitness advantage that cooperators have over defectors (Figure 3C).


## Positive niche construction is important to cooperator persistence

To determine how negative niche construction influences the evolution of cooperation, we maximize the allelic conflict ($L=1$, $A=6$).
Here, selection for increasing allelic states among the adaptive loci means that any allelic state will not be greater than at the previous allele (itself), and thus there will always be opportunity for adaptation.
Despite this constant opportunity, niche construction does not increase cooperator presence (Figure 2D).


## NC Enables Cooperator Spread

Figure 4
- if not, could be why thinning is a must.


## NC Prevents Defector Invasion

Figure 5


## How Cooperation Fuels all of this

To directly explore how the increase in population size affects evolutionary outcomes, we vary the maximum size that a population can reach ($S_{max}$, see Equation @eq:popsize). Figure 6A shows the result of these simulations. (**TODO** description of results)

To address how migration affects the evolutionary process in this system, we vary the rate at which migration occurs ($m$). As seen in Figure 6B, cooperation decreases as migration rate increases. This is likely because migration defines the spatial structuring in this system. As migration increases, the population becomes more like a well-mixed system, where defectors are better able to exploit the benefits of cooperation [@griffin2004cooperation; @kummerli2009viscous].
