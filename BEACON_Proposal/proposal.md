---
geometry: margin=0.65in
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
@west2007evolutionary]. For example, cooperators must benefit more from the
cooperative act than others. This can occur when cooperators are clustered
together in spatially-structured populations [@kudzalfick2011high;
@fletcher2009simple; @nadell2010emergence] or when cooperators use
communication [@darch2012density; @brown2001cooperation] or other cues
[@gardner2010greenbeards; @sinervo2006selfrecognition; @veelders2010structural]
to cooperate conditionally with kin. Interestingly, cooperation can also be
bolstered by genetic linkage with self-benefitting traits
[@dandekar2012bacterial; @asfahl2015nonsocial; @foster2004pleiotropy], setting
the stage for an "adaptive race" in which cooperators and defectors vie for the
first highly-beneficial non-social adaptation [@waite2012adaptation;
@morgan2012selection]. We recently showed that cooperators can gain a
substantial leg up on defectors in an adaptive race when the cooperative
behavior increases population density, thus increasing the likelihood of
acquiring beneficial mutations (in prep.).  Nevertheless, this advantage is
fleeting (Fig.  1A). Once the opportunities for adaptation are exhausted,
cooperators are once again at a disadvantage against defectors. As shown in
Fig. 1B, however, cooperation can be maintained indefinitely when frequent
environmental changes produce a stream of non-social adaptive opportunities.
While natural organisms typically find themselves in changing environments,
cooperators may not be able to rely on the the environment to provide
sufficient adaptive opportunities for their long-term survival.

Previous studies on the evolution have have typically neglected one potentially
major determinant of evolutionary outcomes: environmental change brought about
by the organisms themselves. Through their metabolism, their interactions with
others, and even through their deaths, organisms constantly modify their
environment.  These changes can produce evolutionary feedback loops in which
environmental change alters selection, which, in turn, alters phenotypes and
their corresponding effects on the environment [@odling2003niche]. **This
research will reveal how endogenous environmental change, or *niche
construction*, affects the evolution of cooperation.** First, we will explore
how selective feedbacks influence evolution as populations construct their
environment. We then widen our scope to include scenarios where the environment
itself is biotic, such as when symbiont populations modify their host.

Because this research requires a level of control over both population and
environment that would be difficult to attain even with well-characterized
systems, we employ computational modeling for these initial studies. However,
we expect that the results gained through this project will be instrumental in
designing future microbial experiments. We first describe the model that will
be developed and then detail how it will be used to study the effects of niche
construction on the evolution of cooperation in two contexts.

#### Model Description {#model}

In our proposed agent-based model, each individual has a genotype of length
$L+1$.  A binary allele at the first locus determines whether or not the
individual is a cooperator, which carries cost $c$. The remaining $L$ loci are
*stress loci*, and are each occupied by a $0$ or an integer from the set
$A=\{1, \ldots, a_{max}\}$, where $a_{max}$ is the number of possible alleles.
These alleles represent adaptations to the environment, and the number of loci
determines the number of possible adaptations. All non-zero alleles carry
fitness benefit $\delta$. Although we define no inherent differences among the
alleles, we reward genotypes with sequentially increasing allelic states by
conferring fitness benefit $\epsilon$ for each allele whose value is 1 greater
than the allele at the previous locus (modulo $A$). Thus, the particular
sequence of alleles in a population determines which genotypes are most fit.
Because mutations are random, as described below, each population will evolve
sequences that start with different allelic states. These different sequences
represent the unique niches constructed by populations.

We observe the evolutionary process in a metapopulation of $N$ populations,
which are initiated with non-adapted individuals and cooperator proportion
$p_0$. Each population grows to capacity $S_{min} + p (S_{max} - S_{min})$,
where $p$ is the proportion of cooperators in that population. After growth,
mutations alter the allelic state at stress loci and the cooperation locus with
probabilities $\mu_{s}$ and $\mu_{p}$, respectively. Individuals then migrate
to a randomly chosen neighbor patch at rate $m$. These migrational
neighborhoods consist of adjacent population nodes on a lattice or other graph.
Finally, populations are thinned to proportion $d$ to accommodate the next
cycle of growth.


### Can Niche Construction Feedbacks Sustain the Evolution of Cooperation?

We will first explore how selective feedbacks affect the evolution of
cooperative public goods production. In our model, public goods enable
populations to reach greater densities ($S_{max} > S_{min}$). This increase in
growth provides larger populations with more mutational opportunities to gain
non-social adaptations. Importantly, as populations adapt, they alter selection
at their patch. Using our model (varying parameters $\epsilon$ and $a_{max}$),
we will explore how the degree to which individuals construct their
environments affects evolutionary trajectories and outcomes. Aside from
providing adaptive opportunity, niche construction may significantly diminish
the threat of invasion by immigrant defectors. We also hope to gain an
understanding of how emigration allows populations to effectively export their
environment, and whether this benefits cooperators, whose larger populations
produce more migrants.


### How do Selective Feedbacks affect Host-Symbiont Co-Evolution?

In our first set of experiments, the state of the environment is implicit,
depending entirely on the composition of the population. However, the
environment is often itself a biological entity, which can produce additional
evolutionary feedbacks. These feedbacks are certainly present in infections and
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


### Summary

TODO


\newpage

![(**A**) Through "genetic niche hiking", cooperators outrun defectors by association with non-social adaptations that compensate for the cost of cooperation. Once defectors become equally adapted, however, they quickly drive cooperators to extinction. (**B**) When environmental change is frequent (here every 1,000 cycles), the continual potential for adaptation allows cooperators to persist indefinitely.](figures/Figure1all-scaled.png)

![Model Overview: For simplicity, we consider two clonal populations. (**A**) Because public good production is costly, the cooperator population has lower fitness relative to the defector population as shown in the bar graph. However, these public goods enable the cooperator population to be larger. (**B**) As a result, the cooperator population more quickly acquires mutations. Because these mutations are beneficial, the fitness of cooperators surpasses that of the ancestral defector (bar graph baseline). (**C**) Selection favors alleles at adjacent loci that form sequences, offering a further boost to cooperators. (**D**) The cooperator patch now favors individuals with allelic state $2,3,1$.](figures/diagram1.pdf)

\newpage

## Abstract (1600 chars)

Through their interactions, their activities, and even their mere presence,
organisms change the environment for themselves and others. This "niche
construction" process becomes particularly interesting when it creates
evolutionary feedback, whereby selective pressures are altered in response to
environmental change. With the proposed project, we aim to reveal how niche
construction influences the evolution of cooperation, which has been a
long-standing challenge to evolutionary theory. We will develop and use a
simulation model in which 

populations of individuals that cooperatively
produce a public good that permits increased growth in a stressful environment
and investigate how local- and global-scale niche construction affects the
ability of these populations to resist invasion by non-producing cheats. We
find that niche construction profoundly impacts the evolution of cooperation by
creating new opportunities for adaptation. Cooperators are able to escape
subversion by cheats as long as niche construction clears these paths of
adaptation. This work provides a crucial step towards understanding how
evolution occurs in complex environments like those found in nature.

## Criterion One: Scientific Strength of the Proposed Project (250 chars)

The selective feedbacks that organisms produce as they change their environment
has received relatively little attention, despite their potential to radically
alter evolutionary outcomes. By incorporating these selective feedbacks, this
project will offer new insights into the evolution of cooperation, both in the
context of single populations and in host-symbiont interactions.


## Criterion Two: Centrality of Project to BEACON’s Mission (250 chars)


## Criterion Three: Quality of Plan for Obtaining External Funding (250 chars)

The preliminary results will enable us to be competitive in finding external
funding. Several recent publications have argued that insights into the
selective feedbacks produced by niche construction are critical for
understanding host-pathogen co-evolution.


## Criterion Four: Degree of Multidisciplinarity of Project (250 chars)

This project is a collaboration of a computer scientist (Connelly) and a biologist (Turner).


## Criterion Five: Impact on Education and Human Resource Development (250 chars)

B. Connelly is currently developing hands-on activities at the Pacific Science
Center that introduce evolution and the effects of environmental change to high
school students and the general public. He will lead these several times in the
coming year


## Criterion Six: Knowledge Transfer to Industry (250 chars)

Understanding the forces that maintain cooperation is essential in medicine for
developing "anti-infective" treatments, in industry for wastewater treatment,
and in engineering networks where resources are shared among cars and other
devices.


## Criterion Seven: Impact on Achieving the Diversity Goals of BEACON (250 chars)


## Criterion Eight: Multi-Institutionality (250 chars)

This project is a collaboration between individuals from the University of
Washington and Michigan State University.


## Criterion Nine: Budget Appropriateness (1600 chars)

All funds will be allocated to salary for Connelly, who will lead model development, run simulations, analyze data, and lead preparation for all manuscripts that result. Computational resources for simulations will be funded by a grant to Connelly from Google.


## Criterion Ten: Overall Quality

## Diversity plan (1600 characters maximum)

## Data management plan (1600 characters maximum)

We are committed to practices that facilitate the maintenance and dissemination
of all data produced during and after the duration of the proposed research in
a manner consistent with the requirements defined by the NSF as specified in
the Grant Proposal Guide. It is a primary concern that all data related to this
project are accessible, understandable, usable, and clearly demonstrate the
methods used in order to be repeatable. For the purposes of this project, we
define data to be software, configuration files, and result data. We include
published figures, plots, and tables of data used for making plots as well as
curriculum materials for educational and outreach programs. All data will be
stored in plain-text formats and will be readable by freely-available software.
Descriptive metadata will be included in order to sufficiently annotate all
result data and configuration files, as well as to indicate the steps necessary
to regenerate those data. All data will be made publically available and
released under licensed approved by the [Open Source Initiative](http://opensource.org).


## Comments (1600 characters maximum)

\newpage

# References

