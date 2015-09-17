#!/usr/bin/env Rscript

library(dplyr)
library(magrittr)
library(ggplot2)
library(ggplot2bdc)

source('figsummary.R')
source('formatting.R')

cinvasion <- read.csv('../data/cooperator_invasion.csv.bz2')
cinvasion$Replicate <- as.factor(cinvasion$Replicate)
cinvasion$NicheConstructionFeedback <- factor(cinvasion$NicheConstructionFeedback,
                                              levels=c(TRUE, FALSE))

facet_labels <- data.frame(Time=0, CooperatorProportion=1,
                           NicheConstructionFeedback=c(TRUE, FALSE),
                           Label=c('A','B'))
facet_labels$NicheConstructionFeedback <- factor(facet_labels$NicheConstructionFeedback,
                                                 levels=c(TRUE, FALSE))

fig5 <- ggplot(data=cinvasion,
               aes(x=Time, y=CooperatorProportion, color=Replicate)) +
    facet_grid(NicheConstructionFeedback ~ .) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +
    geom_line() +
    geom_text(data=facet_labels, aes(label=Label), vjust=1.2, hjust=1.2,
              color='black', fontface='bold') +
    scale_y_continuous(limits=c(0,1)) +
    scale_color_grey(guide=FALSE) +
    labs(x=label_time, y=label_cooperator_proportion) +
    theme(strip.text = element_blank())
fig5 <- rescale_plot(plot=fig5, ratio=3.236)
ggsave_golden(filename='../figures/cooperator_invasion.png', plot=fig5,
              dpi=figure_dpi)

