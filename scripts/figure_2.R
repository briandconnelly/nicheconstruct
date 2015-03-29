#!/usr/bin/env Rscript

# Plot Figure 2

library(magrittr)
library(dplyr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')

# Read the data sets
gnh_data <- read.csv('../data/L05_A06_1xDelta_0xEpsilon.csv')
base_data <- read.csv('../data/L05_A06_1xDelta_1xEpsilon.csv')
nonc_data <- read.csv('../data/L05_A06_2xDelta_0xEpsilon.csv')
noneg_data <- read.csv('../data/L05_A05_1xDelta_1xEpsilon.csv')
neg_data <- read.csv('../data/L01_A06_1xDelta_1xEpsilon.csv')


# Combine the data sets
fig2data <- bind_rows(gnh_data, base_data, nonc_data, noneg_data, neg_data)
fig2data$Replicate <- as.factor(fig2data$Replicate)
fig2data$Treatment <- factor(fig2data$Treatment,
                             levels=c('L05_A06_1xDelta_0xEpsilon',
                                      'L05_A06_1xDelta_1xEpsilon',
                                      'L05_A06_2xDelta_0xEpsilon',
                                      'L05_A05_1xDelta_1xEpsilon',
                                      'L01_A06_1xDelta_1xEpsilon'),
                             labels=c('A', 'B', 'C', 'D', 'E'))

# Get the area under the curve of cooperator proportion for each replicate of
# each treatment ("Cooperator Presence")
fig2integrals <- fig2data %>%
    group_by(Treatment, Replicate) %>%
    summarise(N=n(), Integral=sum(CooperatorProportion)/(max(Time)-min(Time)))


fig2 <- ggplot(data=fig2integrals, aes(x=Treatment, y=Integral)) +
    geom_boxplot() +
    scale_y_continuous(limits=c(0,1)) + 
    labs(x='', y=label_cooperator_presence) +
    theme_bdc_grey(ticks.x=FALSE, grid.y=TRUE) + 
    theme(axis.text.x = element_text(vjust=1, face='bold', size=rel(1.2)))
fig2 <- rescale_golden(plot=fig2)
ggsave_golden(plot=fig2, filename='../figures/Figure2.png', dpi=300)


alt <- ggplot(data=fig2integrals, aes(x=1, y=Integral)) +
    facet_grid(. ~ Treatment) +
    geom_boxplot() +
    scale_y_continuous(limits=c(0,1)) + 
    labs(x='', y=label_cooperator_presence) +
    #theme_bdc_grey(base_family='Helvetica', ticks.x=FALSE, grid.y=TRUE) + 
    theme_bdc_grey(ticks.x=FALSE, grid.y=TRUE) + 
    theme(axis.text.x = element_blank())
