#!/usr/bin/env Rscript

library(dplyr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')

# Read the data sets
base_data <- read.csv('../data/L05_A06_1xDelta_1xEpsilon.csv')
nonc_data <- read.csv('../data/L05_A06_2xDelta_0xEpsilon.csv')
noneg_data <- read.csv('../data/L05_A05_1xDelta_1xEpsilon.csv')

# Combine the data sets
fig2data <- bind_rows(base_data, nonc_data, noneg_data)
fig2data$Replicate <- as.factor(fig2data$Replicate)
fig2data$Treatment <- factor(fig2data$Treatment,
                             levels=c('L05_A06_1xDelta_1xEpsilon',
                                      'L05_A06_2xDelta_0xEpsilon',
                                      'L05_A05_1xDelta_1xEpsilon'),
                             labels=c('(a)', '(b)', '(c)'))

fig2 <- ggplot(data=fig2data, aes(x=Time, y=CooperatorProportion,
                                  color=Replicate)) +
    facet_grid(. ~ Treatment) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +
    geom_line() +
    scale_color_grey(guide=FALSE) +
    scale_y_continuous(breaks=seq(from=0, to=1, by=0.25), limits=c(0,1)) +
    labs(x=label_time, y=label_cooperator_proportion)
fig2 <- rescale_plot(plot=fig2, ratio=1/0.8)
ggsave(filename='../figures/Figure2.png', plot=fig2, dpi=figure_dpi)

