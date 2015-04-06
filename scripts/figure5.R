#!/usr/bin/env Rscript

library(magrittr)
library(dplyr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')

target_frames <- c(0,272,325,500)

genotype_colors <- c('C: [1 2 3 4 5]'= color_cooperator,
                     'C: [1 2 3 4 6]'= color_cadapt,
                     'C: [1 2 3 5 6]'= color_cadapt2,
                     'D: [1 2 3 4 3]'= color_misc,
                     'D: [1 2 3 4 5]'= color_defector)

genotype_colors <- c('C: [1 2 3 4 5]'= '#1f78b4',
                     'C: [1 2 3 4 6]'= '#6DCCDA',
                     'C: [1 2 3 5 6]'= 'yellow',
                     'D: [1 2 3 4 3]'= 'yellow',
                     'D: [1 2 3 4 5]'= '#b2df8a')

# a6cee3

fig5data <- read.csv('../data/defector_invade_matched_sample.csv.bz2') %>% filter(Time %in% target_frames)
fig5data$Cooperator <- fig5data$Cooperator == 'True'
fig5data$Genotype <- as.factor(fig5data$Genotype)
fig5data$FullGenotype <- factor(sprintf("%s: %s", ifelse(fig5data$Cooperator, 'C', 'D'), fig5data$Genotype))
fig5data$TimeStr <- factor(sprintf("t=%d", fig5data$Time))


fig5 <- ggplot(data=fig5data, aes(x=X, y=Y, color=FullGenotype, fill=FullGenotype)) +
    facet_grid(. ~ TimeStr) +
    geom_point(shape=22, size=4) +
    scale_x_continuous(limits=c(0, max(fig5data$X))) +
    scale_y_continuous(limits=c(0, max(fig5data$Y))) +
    scale_color_manual(guide=FALSE, values=genotype_colors) +
    scale_fill_manual(guide=FALSE, values=genotype_colors) +
    theme_bdc_lattice_population() +
    theme(strip.background = element_blank()) +
    theme(strip.text = element_text(size=rel(0.6), vjust=0.2, color='grey30')) +
    theme(panel.margin = grid::unit(0.25, 'lines')) +
    theme(panel.border = element_rect(fill='transparent', color=NA))
fig5 <- rescale_square(plot=fig5)
ggsave(filename='../figures/Figure5.pdf', plot=fig5)
