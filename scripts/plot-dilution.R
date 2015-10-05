#!/usr/bin/env Rscript

library(dplyr)
library(magrittr)
library(ggplot2)
library(ggplot2bdc)

source('figsummary.R')
source('formatting.R')

dilutiondata <- read.csv(bzfile('../data/dilution.csv.bz2'))
dilutiondata$Replicate <- as.factor(dilutiondata$Replicate)


figXb <- ggplot(data=dilutiondata,
                aes(x=Births, y=CooperatorProportion, color=Replicate)) +
    facet_grid(DilutionSurvival ~ . ) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +
    geom_line() +
    scale_color_grey(guide=FALSE) +
    scale_y_continuous(limits=c(0,1), breaks=c(0,0.5,1)) +
    labs(x=label_births, y=label_cooperator_proportion) +
    theme(strip.text = element_text(size=rel(1.0), vjust=0.2, face='plain'))
ggsave(filename='../figures/dilution-births.png', plot=figXb, dpi=figure_dpi)


presence <- dilutiondata %>%
    group_by(DilutionSurvival, Replicate) %>%
    summarise(Integral=sum(CooperatorProportion)/n())

figXc <- ggplot(data=presence, aes(x=DilutionSurvival, y=Integral)) +
    geom_point(shape=1, alpha=replicate_alpha) +
    stat_summary(fun.data='figsummary') +
    scale_y_continuous(limits=c(0,1)) +
    scale_x_continuous(limits=c(0,1)) +
    labs(x=label_dilutionsurvival, y=label_cooperator_presence_scaled)
figXc <- rescale_golden(plot=figXc)
ggsave_golden(filename='../figures/dilution-births-integral.png', plot=figXc,
              dpi=figure_dpi)

