---
#title: Evolution of Cooperation through Feedback from Niche Construction
#author:
#- Brian Connelly (UW)

geometry: margin=0.75in
bibliography: references.bib
csl: nature.csl

output:
    pdf_document:
        number_sections: yes
        toc: yes
    html_document:
        number_sections: no
        theme: default
        toc: yes
    word_document:
        fig_height: 5in
        fig_width: 5in

...

## Evolution of Cooperation through Feedback from Niche Construction

Cooperative behaviors are common across all branches of the tree of life.
Insects divide labor within their colonies, plants and soil bacteria exchange
required nutrients, birds care for others' young, and the trillions of cells in
the human body restrain their growth and coordinate with others to provide
vital functions. Each instance of cooperation presents an evolutionary
challenge: How can individuals that sacrifice their own well-being to help
others avoid subversion by those that do not? Over time, we would expect these
*defectors* to rise in abundance at the expense of others, eventually driving
cooperators---and perhaps the entire population---to extinction.

Several factors can defer this potential *tragedy of the commons*
[@hardin1968tragedy; @hamilton1964geneticalboth; @nowak2006five;
@west2007evolutionary]. For example, it has frequently been demonstrated that
close relatives must be more likely to benefit from the cooperative act than
others. This can occur when cooperators are clustered together in
spatially-structured populations [@kudzalfick2011high; @fletcher2009simple;
@nadell2010emergence] or when cooperators use communication [@darch2012density;
@brown2001cooperation] or other cues [@gardner2010greenbeards;
@sinervo2006selfrecognition; @veelders2010structural] to identify and cooperate
conditionally with kin. Interestingly, cooperation can also be bolstered by
genetic association with self-benefitting traits [@dandekar2012bacterial;
@asfahl2015nonsocial; @foster2004pleiotropy], setting the stage for an
"adaptive race" in which cooperators and defectors vie for the first
highly-beneficial non-social adaptation [@waite2012adaptation;
@morgan2012selection]. Using a computational model inspired by corresponding
microbial experiments, we recently showed that cooperators can gain a
substantial leg up on defectors when the cooperative behavior increases
population density, and thus the likelihood of acquiring beneficial mutations
(in prep.). Nevertheless, this advantage is fleeting (Fig. 1A). Once the
opportunities for adaptation are exhausted, cooperators are once again at a
disadvantage against defectors. As shown in Fig. 1B, however, cooperation can
be maintained indefinitely when frequent environmental changes produce a stream
of adaptive opportunities. While natural organisms typically find themselves in
changing environments, can cooperators bet their success on the environment
providing a sufficient influx of adaptive opportunities?

Our previous study and others have neglected one potentially major determinant
of evolutionary outcomes: environmental change brought about by the organisms
themselves. Through their metabolism, their interactions with others, and even
through their deaths, organisms constantly modify their environment. These
changes can produce evolutionary feedback loops in which environmental change
alters selection, which, in turn, alters phenotypes and their corresponding
effects on the environment. **This research will reveal how endogenous
environmental change, or *niche construction*, [@odling2003niche] affects the
evolution of cooperation.** First, we will explore how selective feedbacks
influence evolution as populations construct their environment. We then widen
our scope to include scenarios where the environment itself is also a target of
selection, such as when symbiont populations modify their host.

Because this research requires a level of control over both population and
environment that would be difficult to attain even with well-characterized
systems, we employ computational modeling for these initial studies. However,
we expect that the results and experiences gained through this project will be
instrumental in designing future microbial experiments. As detailed in the
[Model Description](#model), we will develop an agent-based model in which
feedbacks from niche construction affect the evolution of cooperation in a
metapopulation of populations connected by limited migration. The following
sections describe how this model will be used in the context of this research.


### Phenotype-Driven Niche Construction

We first address the role of selective feedbacks in the context of public goods
cooperation, where cooperators produce a resource that is available to all. In
our model, the costly production of public good allows populations to reach
larger densities. This increase in growth provides larger populations with more
mutational opportunities to gain non-social adaptations. Importantly, as
populations adapt to their environment, they alter selection at that patch. In
our model, individuals are favored that more closely match the unique state of
their patch. Through this niche construction process, populations of
cooperators may ensure survival by rendering their environment inhospitable to
immigrant defectors. Of course, these cooperators remain susceptible to
invasion from within by defectors that arise via mutation. By controlling how
uniquely each population can construct its niche via the number of possible
adaptations as well as the benefit of doing so, our model will allow us to
observe how the strength of the resulting feedbacks affect evolutionary
outcomes.

Natural organisms display a great diversity of social behaviors. Along with
public goods, bacteria also commonly produce toxins that inhibit or kill
competing strains [@riley2002bacteriocins]. These *public bads* benefit the
immune cooperator strain both by reducing competition for resources and by
limiting their competitors' mutational opportunities. To identify general
principles about how niche construction influences the evolution of social
behaviors, we will extend our model to capture additional forms of social
interaction. For example, we can model spiteful behaviors
[@hamilton1970selfish] by allowing populations to reach the same carrying
capacity, but having mutations occur at a rate proportional to the number of
cooperators.


### Feedbacks in Host-Symbiont Co-Evolution

In the studies described above, the state of the environment was implicit,
depending entirely on the composition of the population. However, the
environment itself is often a target of selection, which can produce additional
evolutionary feedbacks. These feedbacks certainly play a role in populations
such as the human microbiome or infections, where bacterial behaviors affect
their host's fitness. As the host population changes, so too will selection on
their microbial symbiont populations.  Here, evolutionary outcomes depend
greatly on the degree of shared interests between the host and symbiont. For
example, the cooperative production of virulence factors by the pathogen *P.
aeruginosa* in lung infections is harmful to those with cystic fibrosis.
Conversely, digestive enzymes produced in the gut microbiome are vital to host
health.

By extending our model to include selection at the host level and defining how
changes in host fitness affect changes in symbiont fitness (and vice versa), we
will address how the different types of interactions that hosts and their
symbionts have, such as mutualisms and parasitisms, affect the evolutionary
process. It was recently suggested that this niche construction perspective
will be critical for improving our understanding of viral evolution
[@hamblin2014viral] and evolution in co-infecting parasites [@hafer2015when].


#### Model Description {#model}

In our proposed model, each individual has a length $L+1$ genotype. The first
$L$ loci are *stress loci*, and are each occupied by a $0$ or an integer from
the set $A=\{1, \ldots, a_{max}\}$, where $a_{max}$ is the number of possible
alleles.  These alleles represent adaptations to the environment, and the
number of loci determines the number of possible adaptations. All non-zero
alleles carry fitness benefit $\delta$. Although we define no inherent
differences among the alleles, we reward genotypes with sequential stress
alleles, providing fitness benefit $\epsilon$ for each allele whose value is 1
greater than the previous allele (modulo $A$). The timescales of population
growth and niche construction can be de-coupled by factoring previous allelic
states into these fitness calculations [@laland1996evolutionary]. Because
mutations are random, as described below, each population will evolve sequences
that start with different allelic states. Importantly, these different
sequences represent the unique niches constructed at each patch.  An additional
binary allele at locus $L + 1$ determines whether or not the individual is a
cooperator, which carries cost $c$. Each of the $N$ populations in the
metapopulation is initiated with non-adapted individuals and cooperator
proportion $p_0$.

Each population grows to capacity $S_{min} + p (S_{max} - S_{min})$, where $p$
is the proportion of cooperators in that population. Mutations alter the
allelic state at stress loci and the cooperation locus with probability
$\mu_{s}$ and $\mu_{p}$, respectively. After growth, individuals migrate to a
randomly chosen neighbor patch at rate $m$. These migrational neighborhoods
consist of adjacent population nodes on a lattice or other graph. Finally,
populations are thinned to allow for growth in the next cycle. Individuals
survive this thinning with probability $d$.


\newpage

\renewcommand{\figurename}{Fig.}
![(**A**) Through "genetic niche hiking", cooperators outrun defectors by association with non-social adaptations that compensate for the cost of cooperation. Once defectors become equally adapted, however, they quickly drive cooperators to extinction. (**B**) When environmental change is frequent (here every 1,000 cycles), the continual potential for adaptation allows cooperators to persist indefinitely.](figures/Figure1all-scaled.png)

\newpage

## Criterion One: Scientific Strength of the Proposed Project

## Criterion Two: Centrality of Project to BEACON’s Mission

## Criterion Three: Quality of Plan for Obtaining External Funding

## Criterion Four: Degree of Multidisciplinarity of Project

## Criterion Five: Impact on Education and Human Resource Development

## Criterion Six: Knowledge Transfer to Industry

## Criterion Seven: Impact on Achieving the Diversity Goals of BEACON

## Criterion Eight: Multi-Institutionality

## Criterion Nine: Budget Appropriateness

## Criterion Ten: Overall Quality


\newpage

# References

