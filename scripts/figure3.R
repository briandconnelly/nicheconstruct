#!/usr/bin/env Rscript

library(dplyr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')

# Read the data sets
a_defect_invade_matched <- read.csv(bzfile('../data/defector_invade_matched_nomu.csv.bz2'))
a_defect_invade_matched$Treatment <- 'A'
b_defect_invade_block <- read.csv(bzfile('../data/defector_invade_matched_adapt.csv.bz2'))
b_defect_invade_block$Treatment <- 'B'
c_coop_invade <- read.csv(bzfile('../data/cooperator_invade_cheat_noadapt.csv.bz2'))
c_coop_invade$Treatment <- 'C'

# Combine the data
fig3data <- bind_rows(a_defect_invade_matched, b_defect_invade_block, c_coop_invade)
fig3data$Replicate <- as.factor(fig3data$Replicate)
fig3data$Treatment <- factor(fig3data$Treatment, levels=c('A','B','C'),
                             labels=c('A','B','C'))

# Make the plot
fig3 <- ggplot(data=fig3data, aes(x=Time, y=CooperatorProportion)) +
    facet_grid(. ~ Treatment, drop=FALSE) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') + 
    geom_line(aes(group=Replicate), alpha=0.08, color=color_cooperator) +
    scale_y_continuous(limits=c(0,1)) +
    labs(x=label_time, y=label_cooperator_proportion)
fig3 <- rescale_plot(plot=fig3, ratio=1/0.8)
#ggsave(filename='../figures/Figure3.png', plot=fig3, dpi=300)
ggsave(filename='../figures/Figure3-ba.pdf', plot=fig3)
