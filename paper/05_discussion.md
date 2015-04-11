# Discussion

Despite their negative effects, deleterious traits can rise in abundance due to genetic linkage with other traits that are strongly favored by selection [@maynardsmith1974hitch].
In a process termed the "Hankshaw effect", @HANKSHAW recently demonstrated that cooperation can actively prolong its existence by increasing its likelihood of hitchhiking with a beneficial trait.
In that work and in ours, populations of cooperators grow to a higher density than those of defectors.
Because of this, these cooperator populations experience more mutations and are therefore more likely to gain adaptations.
While this process does favor cooperation in the short term, it eventually reaches a dead end; when the opportunities for adaptation are exhausted, and cooperators can no longer hitchhike, they face extinction.
Here, we have considered whether niche construction might serve to perpetually generate new adaptive opportunities and thus favor cooperation indefinitely.

When niche construction occurs, cooperation can indeed persist (Figures [1C](#fig1) and [2A](#fig2)).
In our model, niche construction introduces additional selective effects that influence the evolutionary process, leading to a more pronounced Hankshaw effect.
However, these fitness benefits alone do not maintain cooperation ([Figure 2B](#fig2)).
Niche construction and the selective feedbacks that it produces play a crucial role.

We find that it is specifically *negative* niche construction that maintains cooperation ([Figure 2C](#fig2)).
As cooperator and defector types gain adaptations, they alter their environment ways that favor other types.
Because of this, negative niche construction serves as a perpetual source of adaptation.
Here we observe another facet of the Hankshaw effect: because populations of cooperators are larger, they are better able to respond to the adaptive opportunities that follow from negative niche construction.
By gaining adaptations more quickly, cooperators resist invasion by defectors ([Figure 3B](#fig3)).
Although defectors initially have an advantage by saving on the cost of cooperation, subpopulations of cooperators can quickly gain an advantage because they are larger.
Even in the presence of an equally-adapted defector type, cooperator subpopulations are more likely to produce the next adapted mutant, which can then displace the slower evolving defectors.
These recurring cycles of defector invasion and cooperator adaptation underlie the oscillations in cooperator proportion seen in [Figure 2A](#fig2).
When cooperators do not gain these adaptations, they are driven to extinction by the defector.
This is something that we see occur stochastically in Figures [2A](#fig2) and [3B](#fig3).


## Cooperation as Niche Construction

In our model, niche construction and adaptation are independent of cooperation, which allows us to focus on hitchhiking.
However, by increasing the size of the subpopulation, this form of cooperation can itself be seen niche construction.
Cooperative benefits often take similar forms in natural systems.
For example, bacteria produce a host of extracellular products that scavenge soluble iron [@griffin2004cooperation], digest large proteins [@darch2012density; @diggle2007cooperation], and reduce the risk of predation [@cosson2002pseudomonas], among many others [@west2007social].
As in our model, these forms of cooperation are likely to increase local population density.
While many studies have focused on how the environment affects the evolution of these cooperative traits, relatively few have addressed how the environmental changes created by these products feed back to influence evolution.

Perhaps most similar to this study, @vandyken2012origins demonstrated that when two negative niche constructing, cooperative behaviors co-evolve, selection can increasingly favor these traits, which are disfavored when alone. 
In that model, "reciprocal niche construction" occurred when the negative feedback resulting from one strategy positively influenced selection for the other, creating a perpetual cycle that maintained both forms of cooperation.
Arguably, this can be seen as an instance of hitchhiking: the currently-maladaptive form of cooperation is maintained by association with the adaptive form.

When dispersal is limited, competition among kin can undermine cooperation. 
To separate kin competition from kin selection, @lehmann2007evolution developed a model in which a cooperative, niche-constructing behavior only benefitted future generations.
Kin competition was thereby reduced, and cooperation instead benefitted descendants.
This work highlights an important aspect of niche construction---often, the rate of selective feedback from niche construction is different from the rate at which populations grow.


## Evolution at Multiple Timescales

In our work, the niche is modeled implicitly by the composition of the population.
Any changes in the population, therefore, produce immediate effects on the constructed environment and the resulting selective feedbacks.
However, timescales in our model could be de-coupled in two ways.
First, cooperators modify their niche by enabling their population to reach larger density (Equation 4).
These increased population sizes play a critical role by effectively increasing the rate of evolution in these populations.
Because of the importance of this process, it would be very informative to explore how sensitive our results are to changes in how quickly population sizes increase and for how long they are upheld.
Similarly, changes in the rate at which a niche changes in response to subpopulation changes could substantially alter our results.
Not only would such changes in timescale affect the selective values of alleles as the population changed, but they could also influence whether or not populations were able to evolve adapted types and if so, how well those adapted types can propagate through the population to address the threat of a defector.

Other studies, while not focused on cooperation, have similarly shown that the timescales at which niche construction feedbacks occur can strongly influence evolutionary outcomes [@laland1999evolutionary; @laland1996evolutionary].
This perspective is likely to be crucial for understanding the evolution of cooperative behaviors like the production of public goods.
In these instances, environmental changes are likely to occur on different timescales than growth, which can have profound effects.
For example, a multitude of factors including protein durability [@brown2007durability; @kummerli2010molecular], diffusion [@driscoll2010theory; @allison2005cheaters], and resource availability [@zhang2013exploring; @ghoul2014experimental] influence both the rate and the degree to which public goods alter the environment.
While @lehmann2007evolution showed that cooperation was favored when selective feedbacks act over longer timescales, niche construction may in fact hinder cooperation when selection is more quickly altered.
For example, when public goods accumulate in the environment, cooperators must decrease production to remain competitive [@kummerli2010molecular; @dumas2012cost].
This favors cooperation that occurs facultatively, perhaps by sensing the abiotic [@koestler2014bile; @bernier2011modulation] or biotic environment [@darch2012density; @brown2001cooperation].
To allow our model to more fully address how traits such as these evolve, we would first need to de-couple the niche from the composition of the population and represent the niche explicitly.


## Cooperation and Niche Construction in Host-Symbiont Co-Evolution

As the niche becomes more independent from the population, it develops its own state and dynamics.
A logical next step, then, could be to treat the environment as a biological entity itself, which could introduce additional evolutionary feedbacks.
Such a model could be used to explore the evolution of cooperation in host-symbiont systems, where cooperation among symbiont populations affects host fitness.
As the host population changes, either in response to symbiont cooperation or other factors, so too does selection on their symbiont populations.
Here, evolutionary outcomes depend greatly on the degree of shared interest between the host and symbiont.
Future models could explicitly capture the environment as a biological entity to explore the rich coevolutionary dynamics that these systems might offer.

For example, the cooperative production of virulence factors by the human pathogen *P. aeruginosa* is harmful to hosts with cystic fibrosis [@harrison2007microbial].
Following what we have shown in this work, these antagonistic, negative niche constructing behaviors might actually work to maintain these infections.
If these populations do indeed perpetually benefit from adaptations that are created by niche construction as we have shown, case could perhaps be made for developing treatments that target the selective feedback loop that provides adaptive opportunities in these spatial environments.
While the idea of removing negative selective feedbacks and supporting stability may seem counterintuitive, if it leaves the infecting population more susceptible, then perhaps pairing such a treatment with ones in which mutants are introduced (see e.g., @rumbaugh2009quorum), could significantly improve host fitness.
Expanding models such as ours to address the additional dynamics present in host-symbiont systems such as these could be quite productive.

Or conversely, cooperative light production by *A. fischeri* is vital for the survival of its host, the Hawaiian bobtail squid [@ruby1996lessons].
While our current model and that of @vandyken2012origins have showed that negative niche construction can play a decisive role in the evolution of cooperation, this instance of positive niche construction is a textbook example of where cooperation and mutualism are maintained. Therefore, a greater understanding of the additional feedbacks created in symbioses such as these could be gained from modeling. Similar to our model, these host-symbiont systems likely have many other traits that are orthogonal to cooperation. Perhaps combinations of certain types of behaviors are important for maintaining cooperation, similar to what was shown by @vandyken2012origins.

It was recently argued that incorporating the effects of niche construction is critical for improving our understanding of viral evolution [@hamblin2014viral] and evolution in co-infecting parasites [@hafer2015when].
Incorporating host dynamics, co-evolution, and the feedbacks that they produce into models is likely to be equally important for gaining an understanding of how cooperative behaviors, both positive and negative, evolve in these host-symbiont settings.

