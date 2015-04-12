
# Results

Using the model described in the previous section, we perform simulations that follow the evolution of cooperation in a population of subpopulations that are connected by spatially-limited migration.
Individuals increase their competitiveness by gaining adaptations.
While cooperation does not directly affect the fitness benefits that these adaptations confer, cooperation has indirect effects on the adaptive process.
Specifically, cooperation increases subpopulation density.
As a result, larger subpopulations of cooperators experience more mutational opportunities. 
Cooperation can rise in abundance by hitchhiking along with beneficial mutations, which compensate for the cost of cooperation.
Importantly, subpopulations alter their local environments, which feeds back to influence selection.
Here, we explore how such niche construction affects the evolution of cooperation.


## Cooperation Persists with Niche Construction

Without any opportunity for adaptation ($L=0$), cooperators are swiftly eliminated from populations ([Figure 1A](#fig1)).
Despite an initial lift in cooperator abundance due to increased productivity, the cost of cooperation becomes disadvantageous as migration mixes the initially isolated subpopulations.
When populations can adapt to the external environment ($L > 0$ and $\delta > 0$), but niche construction is absent ($\epsilon=0$), cooperators are maintained only transiently ([Figure 1B](#fig1)).
Here, larger cooperator subpopulations can more quickly adapt to their external environment.
However, as previously described by @HANKSHAW, cooperation is subsequently lost once populations become fully adapted.
This occurs when isogenic defectors (i.e., defectors with identical adaptive loci) arise via mutation and displace cooperators due to their selective advantage.
However, when niche construction feeds back to influence selection ($\epsilon > 0$), cooperation persists in the majority of the replicate populations ([Figure 1C](#fig1)).
We see in [Figure 2A](#fig2) that despite oscillations, cooperation is maintained at high levels in these populations.


## Fitness Increases Alone do not Support Persisting Cooperation

Adaptations to both the external environment and the constructed environment contribute to an individual's fitness in this model.
To determine whether cooperation is maintained solely due to the larger selective values that result from the contributions of niche construction, we performed simulations in which these contributions were removed ($\epsilon=0$).
We instead increased the fitness benefits conferred by adaptation to the external, non-constructed environment ($\delta=0.6)$.
In doing so, we conservatively estimate the selective effects of niche construction by supplementing the selective benefits of adaptations to the external environment by the maximum possible selective benefit that results from niche construction.
Nevertheless, we find that simply increasing selective values does not enable cooperators to persist ([Figure 2B](#fig2)).
Niche construction, therefore, plays a decisive role here.


## Negative Niche Construction is Critical to Cooperator Persistence

In our model, an adaptation to the constructed environment initiates a new instance of niche construction, leading to sequentially increasing allelic states across the adaptive loci.
Under certain conditions, this construction always makes the constructor sub-optimal for the niche it creates (see Box 1).
This negative niche construction occurs when the number of adaptive alleles ($A$) does not divide evenly into the number of adaptive loci ($L$).
In such a case, any sequence of integers on the circular genome will always contain a break in the sequence; that is, one locus will will have an allele that is not one less than the allele at the next locus.
Given this unavoidable mismatch, any type that has fixed will always construct a niche that favors selection for a new type.
When negative niche construction is removed (by setting $L=5$, $A=5$), cooperators are again driven extinct after an initial lift in abundance ([Figure 2C](#fig2)).
These results indicate that the type of niche construction matters. Specifically, negative niche construction is crucial for maintaining cooperation.


## Selective Feedbacks Limit Defector Invasion

The adaptation resulting from selective feedbacks can limit invasion by defectors, which arise either through migration from neighboring patches or through mutation at the cooperation locus.
The latter challenge is particularly threatening, as these isogenic defectors are equally adapted, yet do not incur the cost of cooperation.
As demonstrated in [Figure 3A](#fig3), isogenic defectors rapidly spread when introduced at a single patch in the center of a population of cooperators if mutations do not occur.
However, when cooperators can gain adaptations via mutation, cooperators resist defector invasion in over half of the replicate populations ([Figure 3B](#fig3)).
[Figure 4](#fig4) depicts one such instance.
In that population, isogenic defectors are seeded at a single patch in an otherwise all-cooperator population.
These defectors quickly begin to spread.
However, a neighboring cooperator population gains an adaptation, which increases its fitness above that of the defector.
This type spreads more quickly, stopping the spread of defectors and eventually driving them to extinction.
Because this adaption occurs in a cooperator population, cooperation is able to hitchhike to safety.
Importantly, this new cooperator is favored because of the niche that its ancestral type created.
Here, cooperators can find safety in numbers---because their larger subpopulations have more mutational opportunities, they are more likely to gain adaptations that rescue them from invasion.
Further, these larger cooperator subpopulations exert greater influence on their niches, which increases selection for an adapted type.
This allows that type to appear and to spread more quickly in the population.
[Figure 3C](#fig3) shows how quickly an adapted cooperator type can invade a population of defectors.
Importantly, this cooperator type is adapted to the niche constructed by the defector.

