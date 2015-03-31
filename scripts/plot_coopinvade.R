#!/usr/bin/env Rscript

library(dplyr)
library(magrittr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')
source('figsummary.R')

cidata <- read.csv('../data/cooperator_invade.csv')
cidata$Replicate <- as.factor(cidata$Replicate)
cidata$Treatment <- as.factor(cidata$Treatment)

integrals <- cidata %>%
    group_by(Treatment, Mutations, MigrationRate, Replicate) %>%
    summarise(N=n(), Integral=sum(CooperatorProportion)/(max(Time)-min(Time)))

# Migration rate, treatment, mutationrate

ci_nomu <- filter(cidata, Mutations==FALSE)
p_nomu_prop <- ggplot(data=ci_nomu, aes(x=Time, y=CooperatorProportion,
                                        color=Replicate)) +
    facet_grid(MigrationRate ~ Treatment) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +
    stat_summary(fun.data='figsummary', geom='ribbon', color=NA, fill='black',
                 alpha=0.1) +
    stat_summary(fun.y='mean', geom='line', color='black') +
    scale_color_hue(guide=FALSE) +
    theme_bdc_grey() +
    labs(x=label_time, y=label_cooperator_proportion, title='Without Mutations')
ggsave(filename='../figures/cooperator_invade-NoMutations-proportion.pdf', plot=p_nomu_prop)


ci_mu <- filter(cidata, Mutations==TRUE)
p_mu_prop <- ggplot(data=ci_mu, aes(x=Time, y=CooperatorProportion,
                                        color=Replicate)) +
    facet_grid(MigrationRate ~ Treatment) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +
    stat_summary(fun.data='figsummary', geom='ribbon', color=NA, fill='black',
                 alpha=0.1) +
    stat_summary(fun.y='mean', geom='line', color='black') +
    scale_color_hue(guide=FALSE) +
    theme_bdc_grey() +
    labs(x=label_time, y=label_cooperator_proportion, title='With Mutations')
ggsave(filename='../figures/cooperator_invade-Mutations-proportion.pdf', plot=p_mu_prop)


int_nomu <- filter(integrals, Mutations==FALSE)
ggplot(data=integrals, aes(x=MigrationRate, y=Integral, group=as.factor(MigrationRate)) ) +
    facet_grid(Mutations ~ Treatment) +
    geom_boxplot() +
    scale_x_log10() +
    theme_bdc_grey() +
    labs(x='Migration Rate', y=label_cooperator_presence)



int_mu <- filter(integrals, Mutations==TRUE)
