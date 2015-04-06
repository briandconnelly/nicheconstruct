
# Results

Using the model described in the previous section, we perform simulations that follow the evolution of cooperation in a metapopulation consisting of populations that are connected by spatially-limited migration.
Individuals compete in these populations by gaining a limited number of adaptations that confer fitness benefits.
While cooperation does not directly affect the selective value of these adaptations, cooperation can have indirect effects on the adaptive process.
Specifically, cooperation increases population density. As a result, larger populations of cooperators experience more mutational opportunities to gain adaptations. 
Cooperation can hitchhike along with these adaptations, which compensate for the cost of cooperation.
During this process, populations alter their local environments, which, in turn, influences selection.
Here, we explore how niche construction affects the evolution of cooperation in the simulation environment defined by the parameter values listed in [Table 1](#tables).


## Cooperation Persists with Niche Construction

Without any opportunity for adaptation ($L=0$), cooperators are swiftly eliminated in competition with defectors ([Figure 2A](#fig2)).
Despite an initial lift in cooperator abundance due to increased productivity, the cost of cooperation becomes disadvantageous as migration mixes the initially isolated populations.
When there are opportunities for adaptation ($L=5$) but no niche construction ($\epsilon=0$), cooperators are maintained transiently ([Figure 2B](#fig2)).
Here, larger cooperator populations can more quickly adapt to their environment as before.
As previously described by @HANKSHAW, however, cooperation is subsequently lost once populations become fully adapted to their environment.
Once this has occurred, adapted defectors that arise via mutation at the cooperation locus have a selective advantage and displace cooperators.
However, when niche construction creates selective feedbacks, cooperation persists in over 2/3 of the replicate populations ([Figure 3A](#fig3)).


## Fitness Increases Alone do not Support Persisting Cooperation

In the model, both adaptation and niche construction contribute to an individual's fitness.
To determine whether cooperation is maintained solely due to the larger selective values that result from the contributions of niche construction ($\epsilon$), we performed simulations in which these contributions were removed ($\epsilon=0$), and we instead increased the fitness benefits conferred by adaptation ($\delta=0.6)$.
In doing so, we conservatively estimate the selective effects of niche construction, as fitness benefits of this magnitude would only be given for sequential allelic states that are fixed in full populations. We find that simply increasing selective values does not enable cooperators to persist ([Figure 3B](#fig3)).
Niche construction therefore plays an important role here.


## Negative Niche Construction is Critical to Cooperator Persistence

Negative niche construction can occur in our model due to the selection for sequentially-increasing allelic states and the circular arrangement of these alleles.
This occurs when the number of adaptive alleles ($A$) does not divide evenly into the number of adaptive loci ($L$).
In such a case, any sequence of integers on the circular genome will always contain a break in the sequence; that is, one locus with an allele that is not one less than the allele at the next locus (see [Figure 1](#fig1)).
Given this unavoidable mismatch, any genotype that has fixed will always favor selection for a new genotype (see Figure).
However, if this negative niche construction is removed (by setting $L=5$, $A=5$), cooperators are again driven extinct after an initial lift in abundance ([Figure 3C](#fig3)).


## Selective Feedbacks Limit Defector Invasion

The adaptation resulting from selective feedbacks can limit invasion by defectors, which arise either through immigration from neighboring patches or through mutation from a cooperator ancestor.
The challenge is particularly threatening, as they are equally adapted, yet do not incur the cost of cooperation.
When homologous defectors (i.e., defectors with identical adaptive loci) are introduced as a single population in the center of an $11 \times 11$ metapopulation of cooperators, they quickly spread if no mutations are allowed ([Figure 4A](#fig4)).
However, when resident cooperators can adapt (mutations occur at adaptive loci), cooperators evade defector invasion in over half of the replicate metapopulations ([Figure 4B](#fig4)).
[Figure 5](#fig5) depicts one such instance where cooperators gained an adaptation that stopped and eliminated invading defectors.
We further highlight this process in [Figure 4C](#fig4), where an adapted cooperator genotype can rapidly invade a population of defectors.


## Diversity Hampers the Evolution of Cooperation

TODO: defector can invade a diverse population of cooperators, while adaptation to a matching defector can't spread to stop invasion.

