#!/usr/bin/env Rscript

library(dplyr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')
source('figsummary.R')

fig1A_data <- read.csv('../data/L00.csv')
fig1B_data <- read.csv('../data/L05_A06_1xDelta_0xEpsilon.csv')
fig1C_data <- read.csv('../data/L05_A06_1xDelta_1xEpsilon.csv')

fig1_data <- bind_rows(fig1A_data, fig1B_data, fig1C_data)
fig1_data$Replicate <- as.factor(fig1_data$Replicate)
fig1_data$Treatment <- factor(fig1_data$Treatment,
                              levels=c('L00',
                                       'L05_A06_1xDelta_0xEpsilon',
                                       'L05_A06_1xDelta_1xEpsilon'),
                              labels=c('L00'='(a)',
                                       'L05_A06_1xDelta_0xEpsilon'='(b)',
                                       'L05_A06_1xDelta_1xEpsilon'='(c)'))

fig1 <- ggplot(data=fig1_data, aes(x=Time, y=CooperatorProportion)) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +
    stat_summary(fun.data='figsummary', geom='ribbon', color=NA,
                 fill='black', alpha=0.2) +
    stat_summary(fun.y='mean', geom='line', color='black') +
    scale_y_continuous(breaks=seq(from=0, to=1, by=0.25), limits=c(0,1)) +
    facet_grid(. ~ Treatment) +
    labs(x=label_time, y=label_cooperator_proportion)
fig1 <- rescale_plot(plot=fig1, ratio=1/0.8)
ggsave(filename='../figures/Figure1.png', plot=fig1, dpi=figure_dpi)

