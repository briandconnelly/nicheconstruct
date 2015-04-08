
# Results

Using the model described in the previous section, we perform simulations that follow the evolution of cooperation in a population consisting of subpopulations that are connected by spatially-limited migration.
Individuals increase their competitiveness by gaining a limited number of adaptations.
While cooperation does not directly affect the fitness benefits of these adaptations, cooperation has indirect effects on the adaptive process.
Specifically, cooperation increases subpopulation density. As a result, larger subpopulations of cooperators experience more mutational opportunities to gain adaptations. 
Cooperation can rise in abundance by hitchhiking along with these adaptations, which compensate for the cost of cooperation.
During this process, subpopulations alter their local environments, which feeds back to influence selection.
Here, we explore how niche construction affects the evolution of cooperation in the simulation environment defined by the parameter values listed in [Table 1](#tables).


## Cooperation Persists with Niche Construction

Without any opportunity for adaptation ($L=0$), cooperators are swiftly eliminated in competition with defectors ([Figure 2A](#fig2)).
Despite an initial lift in cooperator abundance due to increased productivity, the cost of cooperation becomes disadvantageous as migration mixes the initially isolated subpopulations.
When populations can adapt to the external environment ($L=5$), but niche construction is absent ($\epsilon=0$), cooperators are maintained only transiently ([Figure 2B](#fig2)).
Here, larger cooperator subpopulations can more quickly adapt to their external environment as before.
However, as previously described by @HANKSHAW, cooperation is subsequently lost once populations become fully adapted to their environment.
This occurs because isogenic defectors (i.e., defectors with identical adaptive loci) arise via mutation and displace cooperation due to their selective advantage.
However, when niche construction creates selective feedbacks, cooperation persists in over 2/3 of the replicate populations ([Figure 2C](#fig2)).
We see in [Figure 3A](#fig3) that despite oscillations, cooperation is maintained at high levels in these populations.


## Fitness Increases Alone do not Support Persisting Cooperation

In the model, adaptations to both the external environment and the constructed environment contribute to an individual's fitness.
To determine whether cooperation is maintained solely due to the larger selective values that result from the contributions of niche construction ($\epsilon$), we performed simulations in which these contributions were removed ($\epsilon=0$), and we instead increased the fitness benefits conferred by adaptation to the external, non-constructed environment ($\delta=0.6)$.
In doing so, we conservatively estimate the selective effects of niche construction by supplementing the selective benefits of adaptations to the external environment by the maximum possible selective benefit that results from niche construction.
Nevertheless, we find that simply increasing selective values does not enable cooperators to persist ([Figure 3B](#fig3)).
Niche construction, therefore, plays a decisive role here.


## Negative Niche Construction is Critical to Cooperator Persistence

Negative niche construction can occur in our model due to the selection for sequentially-increasing allelic states and the circular arrangement of these alleles (see [Figure 1](#fig1)).
This occurs when the number of adaptive alleles ($A$) does not divide evenly into the number of adaptive loci ($L$).
In such a case, any sequence of integers on the circular genome will always contain a break in the sequence; that is, one locus with an allele that is not one less than the allele at the next locus.
Given this unavoidable mismatch, any type that has fixed will always construct a niche that favors selection for a new type.
However, if this negative niche construction is removed (by setting $L=5$, $A=5$), cooperators are again driven extinct after an initial lift in abundance ([Figure 3C](#fig3)).
These results indicate that the type of niche construction matters. Specifically, negative niche construction is crucial for maintaining cooperation.


## Selective Feedbacks Limit Defector Invasion

The adaptation resulting from selective feedbacks can limit invasion by defectors, which arise either through immigration from neighboring patches or through mutation from a cooperator ancestor.
The latter challenge is particularly threatening, as these isogenic defectors are equally adapted, yet do not incur the cost of cooperation.
As demonstrated in [Figure 4A](#fig4), these isogenic defectors rapidly spread when introduced at a single patch in the center of an $11 \times 11$ population of cooperators if mutations do not occur.
However, when resident cooperators can gain adaptations via mutation, cooperators evade defector invasion in over half of the replicate populations ([Figure 4B](#fig4)).
[Figure 5](#fig5) depicts one such instance where cooperation survived.
In that population, defectors quickly began to spread.
However, an adaptation arose in a neighboring cooperator population that was more fit.
This type spread more quickly, halting defectors and eventually driving them to extinction.
Because this adaption occurred in a cooperator population, cooperation was able to hitchhike to safety.
[Figure 4C](#fig4) shows how quickly an adapted cooperator type can invade a population of defectors.


## Negative Niche Construction Must Follow a Path

We have seen that negative niche construction plays a critical role in maintaining cooperation by creating adaptive "escape routes" for cooperators to resist invasion by defectors.
But in some cases, cooperator populations were not able to gain these adaptations quickly enough, which led to extinction ([Figure 3A](#fig3)).
To see whether stronger negative feedbacks from niche construction would increase the rate at which cooperator populations gained the adaptations needed to escape defector invasion, we performed simulations in which niche construction by one type more strongly favored a completely different type.
This was accomplished in the model by removing selection for sequential allelic states.
Instead, the selective value of an allele at each locus increased with the number of individuals in the population that had the next allelic state at that *same* locus.
For example, selection would favor a type with $[2,5,1,4,4]$ in a niche constructed by $[1,4,6,3,3]$ ($L=5$, $A=6$).
However, this strongly negative niche construction does not better enable cooperators to stave off defection. In fact, cooperation is quickly lost under these conditions ([Figure 6A](#fig6)).

We then performed simulations to determine whether it is the rate of adaptation in response to negative niche construction that is important, not the strength of its feedback.
When the mutation rate at adaptive loci is raised 100-fold ($\mu_{a}=0.001$), cooperation is maintained at higher levels and in more replicate populations ([Figure 6B](#fig6)).

