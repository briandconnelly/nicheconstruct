# Discussion

Despite their negative effects, deleterious traits can rise in abundance through genetic linkage with other traits that are strongly favored by selection [@maynardsmith1974hitch].
In a process termed the "Hankshaw effect", @HANKSHAW recently demonstrated that traits such as cooperation and spite can actively prolong their existence by increasing their likelihood of hitchhiking with a beneficial trait.
In that work and here, subpopulations of cooperators grow to a higher density than those of defectors.
These larger cooperator subpopulations therefore experience more mutations and are consequently more likely to gain adaptations.
Although this process favors cooperation in the short term, it eventually reaches a dead end: When the opportunities for adaptation are exhausted, and cooperators can no longer hitchhike, they face extinction.
Here, we have investigated whether niche construction might serve to perpetually generate new adaptive opportunities and thus favor cooperation.

When niche construction occurs, cooperation can indeed persist (Figures [1C](#fig1) and [2A](#fig2)).
In our model, niche construction introduces additional selective effects that influence the evolutionary process, leading to a more pronounced Hankshaw effect.
However, these fitness benefits alone do not maintain cooperation ([Figure 2B](#fig2)).
Niche construction and the selective feedbacks that it produces play a crucial role.

We find that it is specifically *negative* niche construction that maintains cooperation ([Figure 2C](#fig2)) and even can promote its invasion ([Figure 5A](#fig5)).
As cooperator and defector types gain adaptations, they alter their environment in ways that favor other types.
Thus, negative niche construction serves as a perpetual source of adaptation.
Here we observe another facet of the Hankshaw effect: Because subpopulations of cooperators are larger, they are better able to respond to the adaptive opportunities that are created by negative niche construction.
By gaining adaptations more quickly, cooperators resist invasion by defectors ([Figure 3B](#fig3)).
Even in the presence of an isogenic defector type, cooperator subpopulations are more likely to produce the mutant most adapted to the current constructed niche, which can then displace the slower-adapting defectors.
These recurring cycles of defector invasion and cooperator adaptation underlie the oscillations in cooperator proportion seen in [Figure 2A](#fig2).
When mutations do not confer these adaptations, cooperators lose the adaptive race and are driven to extinction.
This is something that we see occur stochastically in Figures [2A](#fig2) and [3B](#fig3).
However, under other parameter settings within our model, it is possible for cooperaors at extremely low abundances to later re-emerge and invade ([Figure 5A](#fig5)).
In these instances, negitive niche construction provides continual opportunities for cooperators to dominate.


## Cooperation as Niche Construction

In our model, niche construction and adaptation are independent of cooperation, which allows us to focus on hitchhiking.
However, individuals often cooperate in ways that alter the environment.
These cooperative behaviors, therefore, can themselves be seen as niche construction.
For example, bacteria produce a host of extracellular products that scavenge soluble iron [@griffin2004cooperation], digest large proteins [@darch2012density; @diggle2007cooperation], and reduce the risk of predation [@cosson2002pseudomonas], among many others [@west2007social].
As in our model, these forms of cooperation are likely to increase local subpopulation density.
While many studies have focused on how the environment affects the evolution of these cooperative traits, relatively few have addressed how the environmental changes created by these products feed back to influence evolution.

Perhaps most similar to this study, @vandyken2012origins demonstrated that when two negative niche constructing, cooperative behaviors co-evolve, selection can increasingly favor these traits, which are otherwise disfavored when alone. 
In that model, "reciprocal niche construction" occurred when the negative feedback resulting from one strategy positively influenced selection for the other, creating a perpetually oscillating cycle that maintained both forms of cooperation.
Arguably, this can be seen as an instance of hitchhiking: the currently-maladaptive form of cooperation is maintained by association with the adaptive form.

When dispersal is limited, competition among kin can undermine cooperation. 
To separate kin competition from kin selection, @lehmann2007evolution developed a model in which a cooperative, niche-constructing behavior only benefitted future generations.
Kin competition was thereby reduced, and cooperation instead benefitted descendants.
This work highlights an important aspect of niche construction: Often, the rate of selective feedback from niche construction is different from the rate at which populations grow.


## Evolution at Multiple Timescales

In our work, the niche is modeled implicitly by the composition of the subpopulation.
Any changes in the subpopulation, therefore, produce immediate effects on the constructed environment and the resulting selective feedbacks.
However, timescales in our model could be de-coupled in two ways.
First, cooperators modify their niche by enabling their subpopulation to reach larger density (Equation 4).
These increased subpopulation sizes play a critical role by effectively increasing the rate of evolution in these subpopulations.
Because of the importance of this process, it would be very informative to explore how sensitive our results are to the rate at which cooperators increase subpopulation sizes and the rate at which this benefit decays in the absence of cooperators.
Similarly, our results could be substantially affected by alterations in the rate at which the constructed environment changes in response to changes in the subpopulation.

Other studies, while not focused on cooperation, have similarly shown that the timescales at which niche construction feedbacks occur can strongly influence evolutionary outcomes [@laland1999evolutionary; @laland1996evolutionary].
This perspective may be crucial for understanding the evolution of cooperative behaviors like the production of public goods.
In these instances, environmental changes are likely to occur on different timescales than growth, which can have profound effects.
For example, a multitude of factors, including protein durability [@brown2007durability; @kummerli2010molecular], diffusion [@driscoll2010theory; @allison2005cheaters], and resource availability [@zhang2013exploring; @ghoul2014experimental] influence both the rate and the degree to which public goods alter the environment.
While @lehmann2007evolution showed that cooperation was favored when selective feedbacks act over longer timescales, niche construction may in fact hinder cooperation when selection is more quickly altered.
For example, when public goods accumulate in the environment, cooperators must decrease production to remain competitive [@kummerli2010molecular; @dumas2012cost].
This favors cooperation that occurs facultatively, perhaps by sensing the abiotic [@koestler2014bile; @bernier2011modulation] or biotic environment [@darch2012density; @brown2001cooperation].
To study how regulatory traits such as these evolve, we could instead represent the niche explicitly, allowing it to have its own dynamics.
A representation in which the "niche" is simultaneously influenced by external forces and the actions of organisms would more closely resemble many natural systems.


## Cooperation and Niche Construction in Host-Symbiont Co-Evolution

In many biological systems, the environments modified by organisms are themselves other organisms.
In these instances, the "niche" becomes a biological entity with its own evolutionary process.
A logical extension to our model would be to treat the environment as an organism.
Such a model could be used to explore the evolution of cooperation in host-symbiont systems, where cooperation among symbionts affects host fitness.
As the host population changes, either in response to symbiont cooperation or other factors, so too does selection on their symbiont populations.
In our model, each patch could become hosts with their own genotypes, and death and reproduction at the host level could be defined in ways that are sensitive to both host and symbiont genotypes.
Here, evolutionary outcomes depend greatly on the degree of shared interest between the host and symbiont.

Of particular importance are cases where the interests of host and symbiont are in conflict.
By selecting for new, more resistant host genotypes or by provoking a specific immune response, pathogens make their host environment less hospitable and can therefore be seen as potent negative niche constructors.
The results that we have presented here suggest that such negative niche construction can favor cooperative behavior among these symbiont pathogens.
This may be especially relevant when infection is mediated by cooperative behaviors.
For example, the cooperative production of several public goods by *P. aeruginosa* facilitate infection in hosts with cystic fibrosis [@harrison2007microbial].
Models such as what we have described may permit exploration into how cooperation and niche construction intersect here and in other medically-relevant instances.

More generally, it was recently argued that incorporating the effects of niche construction is critical for improving our understanding of viral evolution [@hamblin2014viral] and evolution in co-infecting parasites [@hafer2015when].
Incorporating host dynamics, transmission, co-evolution, and the feedbacks that they produce is likely to be equally important for gaining a greater understanding of how cooperative behaviors evolve in these host-symbiont settings.

