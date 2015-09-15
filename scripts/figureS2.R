#!/usr/bin/env Rscript

library(dplyr)
library(magrittr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')
source('figsummary.R')

dilutiondata <- read.csv('../data/sweep_dilution.csv.bz2')
dilutiondata$Replicate <- as.factor(dilutiondata$Replicate)

integrals <- dilutiondata %>%
    group_by(DilutionFactor, Replicate) %>%
    summarise(Integral=sum(CooperatorProportion)/(max(Time)-min(Time)))

figs2 <- ggplot(data=integrals, aes(x=DilutionFactor, y=Integral)) +
    geom_point(shape=1, alpha=replicate_alpha) +
    stat_summary(fun.data='figsummary') +
    scale_y_continuous(limits=c(0,1)) +
    labs(x=label_dilutionsurvival, y=label_cooperator_presence)
figs2 <- rescale_golden(plot=figs2)
ggsave_golden(filename='../figures/FigureS2.png', plot=figs2, dpi=300)
