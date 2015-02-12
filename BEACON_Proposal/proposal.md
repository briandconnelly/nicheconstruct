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
challenge---how can individuals that sacrifice their own well-being to help
others avoid subversion by those that do not? Over time, we would expect these
*defectors* to rise in abundance at the expense of others, eventually driving
cooperators (and perhaps the entire population) to extinction.

A number of factors can defer this potential *tragedy of the commons*
[@hardin1968tragedy; @hamilton1964geneticalboth; @nowak2006five;
@west2007evolutionary]. For example, it has frequently been demonstrated that
close relatives must be more likely to benefit from the cooperative act than
others. This can occur when cooperators are clustered together in
spatially-structured populations [@kudzalfick2011high; @fletcher2009simple;
@nadell2010emergence] or when cooperators use communication [@darch2012density;
@brown2001cooperation] or other cues [@gardner2010greenbeards] to identify and
cooperate conditionally with kin. Interestingly, cooperation can also be
bolstered by genetic association with vital self-benefitting traits
[@dandekar2012bacterial; @asfahl2015nonsocial; @foster2004pleiotropy], setting
the stage for an "adaptive race" in which cooperators and defectors vie for the
first highly-beneficial non-social adaptation [@waite2012adaptation;
@morgan2012selection]. Using a computational model inspired by corresponding
microbial experiments, we have recently shown that cooperators can have a
substantial leg up on defectors when the cooperative behavior increases
population density and thus the likelihood of acquiring beneficial mutations
(in prep.). However, this advantage is fleeting (Fig. 1A, TODO). Once the
opportunities for adaptation are exhausted, cooperators are once again at a
disadvantage against defectors. As shown in Fig. 1B (TODO), however,
cooperation can be maintained indefinitely when environmental change occurs
frequently, providing a stream of adaptive opportunities. While natural
organisms typically find themselves in changing environments, can cooperators
bet their success on these environments providing a steady influx of adaptive
opportunities?

Our previous model and others have neglected one potentially major determinant
of evolutionary outcomes---environmental change brought about by the organisms
themselves. Through their metabolism, their interactions with others, and even
through their death, organisms constantly modify their environment. These
changes can produce feedback loops in which environmental change alters
selection, which, in turn, alters phenotypes and their corresponding effects on
the environment. **The proposed research aims to reveal how endogenous
environmental change, or *niche construction* [@odling2003niche], affects the
evolution of cooperation.**

#### Model Overview

In our agent-based model, evolution occurs in a metapopulation consisting of
populations connected by limited migration. During each simulation cycle,
populations grow to carrying capacity, mutate, and migrate to neighboring
populations.

Individuals have a length $L + 1$ genotype. The first $L$ loci are *stress
loci*, and are each occupied by a $0$ or an element from the set $A = \{1,
\ldots, a_{max}\}$, where $a_{max}$ is the number of possible alleles.  These
alleles represent adaptations to the environment, and the number of loci
determine the number of possible adaptations. Any non-zero allele carries
fitness benefit $\delta$. Although there is no inherent difference between each
allele, this model rewards genotypes with sequential stress alleles, providing
fitness benefit $\epsilon$ for each allele whose value is 1 greater than the
previous allele (modulo $A$). As mutations occur randomly, each population will
evolve sequences that start with different allelic states.  Importantly, these
different sequences represent the different niches constructed at each patch.
An additional binary allele at locus $L + 1$ determines whether or not the
individual is a cooperator, which carries cost $c$.

Each population grows to capacity $S_{min} + p (S_{max} - S_{min})$, where $p$
is the proportion of cooperators in that population. During growth, mutations
alter the allelic state at stress loci and the cooperation locus with
probability $\mu_{s}$ and $\mu_{p}$, respectively. After growth, individuals
migrate to a randomly chosen neighbor patch at rate $m$. Finally, populations
are thinned to allow for growth in the next cycle. Individuals survive this
thinning with probability $d$.

Environmental changes are triggered either endogenously or exogenously,
depending on the experimental focus, and have one of two effects. The simpler
form reveals an additional stress locus, providing an additional opportunity
for adaptation. Immigrants to less adapted patches will be "pre-adapted" when
change occurs. The more complex form mimics a complete environmental change,
and re-sets the allelic state of each individual. When modeled as the onset of
a novel stress, individuals survive this change with probability $\mu_{t}$,
which represents the likelihood of gaining a mutation conferring tolerance.


### Aim 1: Phenotype-Driven Niche Construction

Spite as part of this


### Aim 2: Feedbacks in Host-Symbiont Co-Evolution

As described in the previous aim, the environmental state was implicit,
depending only on the state of the population.

paper [@hamblin2014viral]


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

