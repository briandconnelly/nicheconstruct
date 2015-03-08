---
geometry: margin=0.75in
fontsize: 10pt
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

## Evolution of Cooperation through Niche Construction Feedback

Cooperative behaviors are common across all branches of the tree of life.
Insects divide labor within their colonies, plants and soil bacteria exchange
essential nutrients, birds care for others' young, and the trillions of cells
in the human body restrain their growth and coordinate to provide vital
functions. Each instance of cooperation presents an evolutionary challenge: How
can individuals that sacrifice their own well-being to help others avoid
subversion by those that do not? Over time, we would expect these *defectors*
to rise in abundance at the expense of others, eventually driving
cooperators---and perhaps the entire population---to extinction.

Several factors can defer this potential *tragedy of the commons*
[@hardin1968tragedy; @hamilton1964geneticalboth; @nowak2006five;
@west2007evolutionary]. For example, it has frequently been demonstrated that
close relatives must benefit from the cooperative act more than others. This
can occur when cooperators are clustered together in spatially-structured
populations [@kudzalfick2011high; @fletcher2009simple; @nadell2010emergence] or
when cooperators use communication [@darch2012density; @brown2001cooperation]
or other cues [@gardner2010greenbeards; @sinervo2006selfrecognition;
@veelders2010structural] to cooperate conditionally with kin. Interestingly,
cooperation can also be bolstered by genetic linkage with self-benefitting
traits [@dandekar2012bacterial; @asfahl2015nonsocial; @foster2004pleiotropy],
setting the stage for an "adaptive race" in which cooperators and defectors vie
for the first highly-beneficial non-social adaptation [@waite2012adaptation;
@morgan2012selection]. We recently showed that cooperators can gain a
substantial leg up on defectors in an adaptive race when the cooperative
behavior increases population density, thus increasing the likelihood of
acquiring beneficial mutations (in prep.).  Nevertheless, this advantage is
fleeting (Fig.  1A). Once the opportunities for adaptation are exhausted,
cooperators are once again at a disadvantage against defectors. As shown in
Fig. 1B, however, cooperation can be maintained indefinitely when frequent
environmental changes produce a stream of non-social adaptive opportunities.
While natural organisms typically find themselves in changing environments,
cooperators likely can not bet their long-term success on the environment
providing a sufficient influx of adaptive opportunities.

Our previous study and others have neglected one potentially major determinant
of evolutionary outcomes: environmental change brought about by the organisms
themselves. Through their metabolism, their interactions with others, and even
through their deaths, organisms constantly modify their environment. These
changes can produce evolutionary feedback loops in which environmental change
alters selection, which, in turn, alters phenotypes and their corresponding
effects on the environment [@odling2003niche]. **This research will reveal how
endogenous environmental change, or *niche construction*, affects the evolution
of cooperation.** First, we will explore how selective feedbacks influence
evolution as populations construct their environment. We then widen our scope
to include scenarios where the environment itself is also a target of
selection, such as when symbiont populations modify their host.

Because this research requires a level of control over both population and
environment that would be difficult to attain even with well-characterized
natural systems, we employ computational modeling for these initial studies.
However, we expect that the results gained through this project will be
instrumental in designing future microbial experiments. We first describe the
model that will be developed and then detail how it will be used to reveal how
niche construction affects the evolution of cooperation in two contexts.

#### Model Description {#model}

In our proposed agent-based model, each individual has a length $L+1$ genotype.
A binary allele at the first locus determines whether or not the individual is
a cooperator, which carries cost $c$. The remaining $L$ loci are *stress loci*,
and are each occupied by a $0$ or an integer from the set $A=\{1, \ldots,
a_{max}\}$, where $a_{max}$ is the number of possible alleles. These alleles
represent adaptations to the environment, and the number of loci determines the
number of possible adaptations. All non-zero alleles carry fitness benefit
$\delta$. Although we define no inherent differences among the alleles, we
reward genotypes with sequentially increasing allelic states by conferring
fitness benefit $\epsilon$ for each allele whose value is 1 greater than the
previous allele (modulo $A$). Because mutations are random, as described below,
each population will evolve sequences that start with different allelic states.
Importantly, these different sequences represent the unique niches constructed
at each patch. We observe the evolutionary process in a metapopulation of $N$
populations of these individuals, where each population is initiated with
non-adapted individuals and cooperator proportion $p_0$.

Each population grows to capacity $S_{min} + p (S_{max} - S_{min})$, where $p$
is the proportion of cooperators in that population. After growth, mutations
alter the allelic state at stress loci and the cooperation locus with
probability $\mu_{s}$ and $\mu_{p}$, respectively. Individuals then migrate to
a randomly chosen neighbor patch at rate $m$. These migrational neighborhoods
consist of adjacent population nodes on a lattice or other graph. Finally,
populations are thinned to proportion $d$ to accommodate growth in the next
cycle.


### Can Niche Construction Feedbacks Sustain the Evolution of Cooperation?

We first explore how selective feedbacks affect the evolution of cooperative
public goods production. In our model, public goods enable populations to reach
greater densities ($S_{max} > S_{min}$). This increase in growth provides
larger populations with more mutational opportunities to gain non-social
adaptations. Importantly, as populations adapt to their environment, they alter
selection at that patch. Using our model, we will explore how the degree to
which individuals construct their environments ($\epsilon$, $a_{max}$) affects
evolutionary trajectories and outcomes. Aside from providing adaptive
opportunity, niche construction may significantly diminish the threat of
invasion by immigrant defectors. We also hope to gain an understanding of how
emigration allows populations to effectively export their environment, and
whether this benefits cooperators, whose larger populations produce more
migrants.


### How do Selective Feedbacks affect Host-Symbiont Co-Evolution?

In our first set of experiments, the state of the environment is implicit,
depending entirely on the composition of the population. However, the
environment is often itself a biological entity, which can produce additional
evolutionary feedbacks. These feedbacks are certainly present in infections or
the human microbiome, where bacterial behaviors greatly affect host fitness. As
the host population changes, so too will selection on their symbiont
populations. Here, evolutionary outcomes depend greatly on the degree of shared
interest between the host and symbiont. For example, the cooperative production
of virulence factors by the pathogen *P.  aeruginosa* in lung infections is
harmful to those with cystic fibrosis. Conversely, cooperative light production
by *A. fischeri* is vital for the survival of its host, the Hawaiian bobtail
squid.

To address how feedbacks from niche construction affect social evolution in
host-symbiont systems, we will extend our model to include selection and
replication at the host level. Here, host fitness will be dependent on the
state of the symbiont population. By altering this dependence, we can observe
how host-symbiont co-evolution differs with *positive-* and *negative niche
construction*. As hosts replicate, we can also explore how co-evolution differs
when symbiont populations are transferred vertically or horizontally. It was
recently suggested that this niche construction perspective will be critical
for improving our understanding of viral evolution [@hamblin2014viral] and
evolution in co-infecting parasites [@hafer2015when].


### Future Directions (may be cut)

Natural organisms display a great diversity of social behaviors. Along with
public goods, bacteria also commonly produce toxins that inhibit or kill
competing strains [@riley2002bacteriocins]. These *public bads* benefit the
immune cooperator strain both by reducing competition for resources and by
limiting their competitors' mutational opportunities. By extending our model to
capture additional forms of social interaction such as these, we hope to
identify general principles about how niche construction influences the
evolution of  social behaviors.


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

