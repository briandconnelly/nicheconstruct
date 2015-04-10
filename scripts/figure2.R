#!/usr/bin/env Rscript

library(magrittr)
library(dplyr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')

# Read the data sets
base_data <- read.csv('../data/L05_A06_1xDelta_1xEpsilon.csv')
nonc_data <- read.csv('../data/L05_A06_2xDelta_0xEpsilon.csv')
noneg_data <- read.csv('../data/L05_A05_1xDelta_1xEpsilon.csv')

# Combine the data sets
fig3data <- bind_rows(base_data, nonc_data, noneg_data)
fig3data$Replicate <- as.factor(fig3data$Replicate)
fig3data$Treatment <- factor(fig3data$Treatment,
                             levels=c('L05_A06_1xDelta_1xEpsilon',
                                      'L05_A06_2xDelta_0xEpsilon',
                                      'L05_A05_1xDelta_1xEpsilon'),
                             labels=c('A', 'B', 'C'))

fig3 <- ggplot(data=fig3data, aes(x=Time, y=CooperatorProportion)) +
    facet_grid(. ~ Treatment) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +        
    geom_line(aes(group=Replicate), alpha=0.4, color=color_cooperator) +
    scale_y_continuous(breaks=seq(from=0, to=1, by=0.25), limits=c(0,1)) +
    labs(x=label_time, y=label_cooperator_proportion) +
    theme_bdc_grey() +
    theme(strip.background = element_blank()) +
    theme(strip.text = element_text(size=rel(1.0), vjust=0.2, face='bold'))
fig3 <- rescale_plot(plot=fig3, ratio=1/1.2)
ggsave(filename='../figures/Figure3.png', plot=fig3, dpi=300)
