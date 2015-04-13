#!/usr/bin/env Rscript

library(magrittr)
library(dplyr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')

s1data <- read.csv(bzfile('../data/defector_invade_matched_muboth.csv.bz2'))
s1data$Replicate <- as.factor(s1data$Replicate)

figS1 <- ggplot(data=s1data, aes(x=Time, y=CooperatorProportion)) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') + 
    geom_line(aes(group=Replicate), alpha=0.08, color=color_cooperator) +
    scale_y_continuous(limits=c(0,1)) +
    labs(x=label_time, y=label_cooperator_proportion)
figS1 <- rescale_plot(plot=figS1, ratio=1/1.2)
ggsave(filename='../figures/FigureS1.png', plot=figS1, dpi=300)

# Get the number of replicates where cooperators remained dominant (58/160)
num_cooperator_dominant <- s1data %>%
    filter(Time==max(s1data$Time)) %>%
    filter(CooperatorProportion > 0.5) %>%
    summarise(NumCooperatorReps=n())
