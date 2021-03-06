
# Results

Using the model described in the previous section, we perform simulations that follow the evolution of cooperation in a population of subpopulations that are connected by spatially-limited migration.
Individuals increase their competitiveness by gaining adaptations.
While cooperation does not directly affect the fitness benefits that these adaptations confer, it does have indirect effects on the adaptive process.
Specifically, cooperation increases subpopulation density.
As a result, larger subpopulations of cooperators experience more mutational opportunities. 
Cooperation can rise in abundance by hitchhiking along with beneficial mutations, which compensate for the cost of cooperation.
Importantly, subpopulations alter their local environments, which feeds back to influence selection.
Here, we explore how such niche construction affects the evolution of cooperation.


## Cooperation Persists with Niche Construction

Without any opportunity for adaptation ($L=0$), cooperators are swiftly eliminated ([Figure 1A](#fig1)).
Despite an initial lift in cooperator abundance due to increased productivity, the cost of cooperation becomes disadvantageous as migration mixes the initially isolated subpopulations.
When populations can adapt to the external environment ($L > 0$ and $\delta > 0$), but niche construction is absent ($\epsilon=0$), cooperators are maintained only transiently ([Figure 1B](#fig1)).
Here, larger cooperator subpopulations adapt more quickly to their external environment, which allows them to rise in abundance.
As previously described by @HANKSHAW, cooperation is swiftly lost once populations become fully adapted.
This occurs when isogenic defectors (i.e., defectors with identical adaptive loci) arise via mutation and displace cooperators due to their selective advantage.
However, when niche construction feeds back to influence selection ($\epsilon > 0$), cooperation persists in the majority of replicate populations ([Figure 1C](#fig1)).
We see in [Figure 2A](#fig2) that despite some oscillations, cooperation is maintained at high levels in the majority of these populations.


## Fitness Increases Alone do not Support Persisting Cooperation

An individual's fitness is affected in this model by adaptations to both the external environment and to the constructed environment.
Here, we determine whether cooperation is maintained as we see in [Figure 2A](#fig2) solely due to the larger selective values that result from the contributions of niche construction.
We performed simulations in which these selective contributions were transferred to supplement the benefits conferred by adaptation to the external, non-constructed environment (i.e., replacing $S_{max} \times \epsilon=0.3$, $\delta=0.3$ with $\epsilon=0$, $\delta=0.6$).
In doing so, we liberally estimate the selective effects of niche construction.
Nevertheless, we find that simply increasing selective values extends the maintenance of cooperation, but does not enable cooperators to persist ([Figure 2B](#fig2)).
Niche construction, therefore, plays a decisive role here.


## Negative Niche Construction is Critical to Cooperator Persistence

In our model, an adaptation to the constructed environment initiates a new instance of niche construction, leading to sequentially increasing allelic states across the adaptive loci.
Under certain conditions, this construction always makes the constructor sub-optimal for the niche it creates.
This form of negative niche construction occurs when the number of adaptive alleles ($A$) does not divide evenly into the number of adaptive loci ($L$).
In such a case, any sequence of integers on the circular genome will always contain a break in the sequence; that is, one locus will perpetually have an allele that is not one less than the allele at the next locus (see [Box 1, Part D](#box1)).
Given this unavoidable mismatch, types will always construct a niche in which selection for a different type is enhanced.
When negative niche construction is removed (by setting $L=5$, $A=5$; see [Box 1, Part C](#box1)), cooperators are again driven to extinction after an initial lift in abundance ([Figure 2C](#fig2)).
Here, a fully-adapted type constructs a niche that favors itself.
When this occurs, a fully-adapted cooperator is at a selective disadvantage against a fully-adapted defector, which does not incur the cost of cooperation.
These results indicate that the type of niche construction matters.
Specifically, negative niche construction is key for maintaining cooperation by the Hankshaw effect.
Here, cooperators prevent defector invasion by hitchhiking along with adaptations to the constructed environment.


## Selective Feedbacks Limit Defector Invasion

The process of adaptation to the constructed niche can limit invasion by defectors, which arise either through migration from neighboring patches or through mutation at the cooperation locus.
This latter challenge is particularly threatening, as these isogenic defectors are equally adapted, yet do not incur the cost of cooperation.
As demonstrated in [Figure 3A](#fig3), when adaptation to the environment cannot occur, isogenic defectors rapidly invade when introduced as a single subpopulation in the center of a population of otherwise all-cooperator subpopulations.
However, cooperators resist defector invasion in over half of the replicate populations when adaptations can arise through mutation ([Figure 3B](#fig3)).
[Figure 4](#fig4) depicts one such instance.
In that population, isogenic defectors are seeded at a single patch in an otherwise all-cooperator population.
These defectors quickly begin to spread.
However, a neighboring cooperator population gains an adaptation, which increases its fitness above that of the defector.
This type spreads more quickly, stopping the spread of defectors and eventually driving them to extinction.
Because this adaption arises in a cooperator subpopulation, cooperation is able to hitchhike to safety.
Importantly, this new cooperator type is favored because of the niche that its ancestral type---and therefore also the defector---constructed.
Here, cooperators can find safety in numbers: because their larger subpopulations have more mutational opportunities, they are more likely to gain adaptations that rescue them from invasion.
Further, these larger cooperator subpopulations exert greater influence on their niches, which increases selection for an adapted type.
This allows that type to appear and to spread more quickly in the population.
[Figure 3C](#fig3) shows how quickly an adapted cooperator type can invade a population of defectors.


## Negative Niche Construction Promotes Cooperator Invasion

The majority of the results shown above have focused on the maintenance of cooperation.
Specifically, cooperators have started at---and maintained---reasonably high proportions in their populations.
In the previous section, we considered cooperator invasion; however, cooperators began in their own single subpopulation without defectors.
It remains to be seen whether cooperators can invade from extreme rarity.
In a population in which cooperators are initially absent, can cooperators that arise by mutation increase in frequency?
With baseline parameters ([Table 1](#tables)), cooperators tend not to invade over 3000 cycles when the initial cooperator proportion is low (see Supplemental Materials).
However, when the benefits of cooperation are increased ($S_{max}=8000$), cooperators can readily invade and reach high proportions ([Figure 5A](#fig5)).
Despite this large benefit, cooperator success still depends on the presence of niche construction.
Without the selective effects that negative niche construction continually exerts, cooperators cannot invade ([Figure 5B](#fig5)).

