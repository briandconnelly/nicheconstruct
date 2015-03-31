#!/usr/bin/env Rscript

# Plot Figure 2

library(magrittr)
library(dplyr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')
source('figsummary.R')

# Read the data sets
base_data <- read.csv('../data/L05_A06_1xDelta_1xEpsilon.csv')
nonc_data <- read.csv('../data/L05_A06_2xDelta_0xEpsilon.csv')
noneg_data <- read.csv('../data/L05_A05_1xDelta_1xEpsilon.csv')
neg_data <- read.csv('../data/L05_A06_1xDelta_1xEpsilon_NEGNC.csv')

# Combine the data sets
fig2data <- bind_rows(base_data, nonc_data, noneg_data, neg_data)
fig2data$Replicate <- as.factor(fig2data$Replicate)
fig2data$Treatment <- factor(fig2data$Treatment,
                             levels=c('L05_A06_1xDelta_1xEpsilon',
                                      'L05_A06_2xDelta_0xEpsilon',
                                      'L05_A05_1xDelta_1xEpsilon',
                                      'L05_A06_1xDelta_1xEpsilon_NEGNC'),
                             labels=c('Niche Construction',
                                      'No Niche Construction',
                                      'Positive NC Only',
                                      'Negative NC Only'))

subplot_labels <- data.frame(Time=0, CooperatorProportion=1,
                             Treatment=c('Niche Construction',
                                         'No Niche Construction',
                                         'Positive NC Only',
                                         'Negative NC Only'),
                             Label=c('A', 'B', 'C', 'D'))

fig2 <- ggplot(data=fig2data, aes(x=Time, y=CooperatorProportion)) +
    facet_grid(. ~ Treatment) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +        
    stat_summary(fun.data='figsummary', geom='ribbon', color=NA, fill='black',
                 alpha=0.1) +
    stat_summary(fun.y='mean', geom='line', color='black') +
    geom_text(data=subplot_labels, aes(label=Label), hjust=0, vjust=1, face='bold') + 
    scale_y_continuous(breaks=seq(from=0, to=1, by=0.25), limits=c(0,1)) +
    labs(x=label_time, y=label_cooperator_proportion) +
    theme_bdc_grey() +
    theme(strip.background = element_blank()) +
    theme(strip.text = element_text(size=rel(0.6), vjust=0.2, color='grey30'))
fig2 <- rescale_plot(plot=fig2, ratio=1/1.2)
ggsave(filename='../figures/Figure2.png', plot=fig2, dpi=300)
