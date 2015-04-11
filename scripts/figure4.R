#!/usr/bin/env Rscript

library(magrittr)
library(dplyr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')

target_frames <- c(0,272,325,390,500,690,812,900)

genotype_colors <- c('C: [1 2 3 4 5]'= color_cooperator,
                     'C: [1 2 3 4 6]'= color_cadapt,
                     'C: [1 2 3 5 6]'= color_cadapt2,
                     'D: [1 2 3 4 3]'= color_misc,
                     'D: [1 2 3 4 5]'= color_defector)

fig4data <- read.csv('../data/defector_invade_matched_sample.csv.bz2') %>%
    filter(Time %in% target_frames)
fig4data$Cooperator <- fig4data$Cooperator == 'True'
fig4data$Genotype <- as.factor(fig4data$Genotype)
fig4data$FullGenotype <- factor(sprintf("%s: %s", ifelse(fig4data$Cooperator, 'C', 'D'), fig4data$Genotype))
fig4data$TimeStr <- factor(sprintf("t=%d", fig4data$Time))


fig4 <- ggplot(data=fig4data, aes(x=X, y=Y, color=FullGenotype, fill=FullGenotype)) +
    facet_wrap(~ TimeStr, ncol=4) +
    geom_point(shape=22, size=4) +
    scale_x_continuous(limits=c(0, max(fig4data$X))) +
    scale_y_continuous(limits=c(0, max(fig4data$Y))) +
    scale_color_manual(guide=FALSE, values=genotype_colors) +
    scale_fill_manual(guide=FALSE, values=genotype_colors) +
    theme_bdc_lattice_population() +
    theme(strip.background = element_blank()) +
    theme(strip.text = element_text(size=rel(0.8), vjust=0.2, color='grey30')) +
    theme(panel.margin = grid::unit(0.25, 'lines')) +
    theme(panel.border = element_rect(fill='transparent', color=NA))
fig4 <- rescale_square(plot=fig4)
ggsave(filename='../figures/Figure4.png', plot=fig4)
