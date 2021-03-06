#!/usr/bin/env Rscript

library(dplyr)
library(magrittr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')

# Read the data sets
treatment_data <- read.csv('../data/initial_coop_prop.csv.bz2') %>%
    select(Time, CooperatorProportion, Replicate, InitialCooperatorProportion)
base_data <- read.csv('../data/L05_A06_1xDelta_1xEpsilon.csv') %>%
    select(Time, CooperatorProportion, Replicate)
base_data$InitialCooperatorProportion <- 0.5

# Combine the data
initpropc <- bind_rows(treatment_data, base_data)
initpropc$Replicate <- as.factor(initpropc$Replicate)


# Make the plot of individual trajectories
figXa <- ggplot(data=initpropc,
               aes(x=Time, y=CooperatorProportion, color=Replicate)) +
    facet_grid(InitialCooperatorProportion ~ .) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +
    geom_line() +
    scale_y_continuous(limits=c(0,1), breaks=c(0,0.5,1)) +
    scale_color_grey(guide=FALSE) +
    labs(x=label_time, y=label_cooperator_proportion) +
    theme(strip.text = element_text(size=rel(1.0), vjust=0.2, face='plain'))
ggsave(filename='../figures/initial_coop_prop.png', plot=figXa, dpi=figure_dpi)


# Calculate the "Cooperator Presence", the area under the cooperator curve
# For this, we'll use the actual initial cooperator proportion, not the
# parameter value.
presence <- initpropc %>%
    group_by(InitialCooperatorProportion, Replicate) %>%
    arrange(Time) %>%
    summarise(Start=head(CooperatorProportion, n=1),
              Integral=sum(CooperatorProportion)/(max(Time)-min(Time)))

figXb <- ggplot(data=presence, aes(x=Start, y=Integral)) +
    geom_point(shape=1, alpha=replicate_alpha) +
    stat_smooth(method='loess') +
    scale_y_continuous(limits=c(0,1)) +
    scale_x_continuous(limits=c(0,1)) +
    labs(x=label_initial_cooperator_proportion_actual, y=label_cooperator_presence)
figXb <- rescale_golden(plot=figXb)
ggsave_golden(filename='../figures/initial_coop_prop-integral.png', plot=figXb)

