#!/usr/bin/env Rscript

library(magrittr)
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
fig4data <- bind_rows(a_defect_invade_matched, b_defect_invade_block, c_coop_invade)
fig4data$Replicate <- as.factor(fig4data$Replicate)
fig4data$Treatment <- factor(fig4data$Treatment,
                             levels=c('A','B','C'),
                             labels=c('A','B','C'))

# Make the plot
fig4 <- ggplot(data=fig4data, aes(x=Time, y=CooperatorProportion)) +
    facet_grid(. ~ Treatment, drop=FALSE) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') + 
    geom_line(aes(group=Replicate), alpha=0.08, color=color_cooperator) +
    scale_y_continuous(limits=c(0,1)) +
    labs(x=label_time, y=label_cooperator_proportion) +
    theme_bdc_grey() +
    theme(strip.background = element_blank()) +
    theme(strip.text = element_text(size=rel(1.0), face='bold'))
fig4 <- rescale_plot(plot=fig4, ratio=1/1.2)
ggsave(filename='../figures/Figure4.png', plot=fig4, dpi=300)

