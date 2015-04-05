#!/usr/bin/env Rscript

library(magrittr)
library(dplyr)
library(ggplot2)
library(ggplot2bdc)
library(Hmisc)

source('formatting.R')
source('figsummary.R')

fig2A_data <- read.csv('../data/L00.csv')
fig2B_data <- read.csv('../data/L05_A06_1xDelta_0xEpsilon.csv') 

fig2_data <- bind_rows(fig2A_data, fig2B_data)
fig2_data$Replicate <- as.factor(fig2_data$Replicate)
fig2_data$Treatment <- factor(fig2_data$Treatment,
                              levels=c('L00',
                                       'L05_A06_1xDelta_0xEpsilon'),
                              labels=c('L00'='A',
                                       'L05_A06_1xDelta_0xEpsilon'='B'))


fig2 <- ggplot(data=fig2_data, aes(x=Time, y=CooperatorProportion)) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +        
    stat_summary(fun.data='figsummary', geom='ribbon', color=NA,
                 fill=color_cooperator, alpha=ribbon_alpha) +
    stat_summary(fun.y='mean', geom='line', color=color_cooperator) +
    scale_y_continuous(breaks=seq(from=0, to=1, by=0.25), limits=c(0,1)) +
    facet_grid(. ~ Treatment) +
    labs(x=label_time, y=label_cooperator_proportion) +
    theme_bdc_grey() +
    theme(strip.background = element_blank()) +
    theme(strip.text = element_text(size=rel(1.0), face='bold'))
fig2 <- rescale_plot(plot=fig2, ratio=1/1.2)
ggsave(filename='../figures/Figure2.png', plot=fig2, dpi=300)

