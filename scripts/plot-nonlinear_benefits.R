#!/usr/bin/env Rscript

library(dplyr)
library(magrittr)
library(ggplot2)
library(ggplot2bdc)

source('figsummary.R')
source('formatting.R')

# Read the data sets
treatment_data <- read.csv('../data/nonlinear_benefits.csv.bz2') %>%
    select(Time, CooperatorProportion, Replicate, Shape)
base_data <- read.csv('../data/L05_A06_1xDelta_1xEpsilon.csv') %>%
    select(Time, CooperatorProportion, Replicate)
base_data$Shape <- 1.0

# Combine the data
benefitdata <- bind_rows(treatment_data, base_data)
benefitdata$Replicate <- as.factor(benefitdata$Replicate)

# Make the plot
figXa <- ggplot(data=benefitdata,
               aes(x=Time, y=CooperatorProportion, color=Replicate)) +
    facet_grid(Shape ~ .) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +
    geom_line() +
    scale_y_continuous(limits=c(0,1)) +
    scale_color_grey(guide=FALSE) +
    labs(x=label_time, y=label_cooperator_proportion)
ggsave(filename='../figures/nonlinear_benefits.png', plot=figXa, dpi=300)

# Calculate the "Cooperator Presence", the area under the cooperator curve
presence <- benefitdata %>%
    group_by(Shape, Replicate) %>%
    summarise(Integral=sum(CooperatorProportion)/(max(Time)-min(Time)))

figXb <- ggplot(data=presence, aes(x=Shape, y=Integral)) +
    geom_point(shape=1, alpha=replicate_alpha) +
    stat_summary(fun.data='figsummary') +
    scale_y_continuous(limits=c(0,1)) +
    scale_x_continuous(limits=c(0,NA)) +
    labs(x=label_benefit_slope, y=label_cooperator_presence)
figXb <- rescale_golden(plot=figXb)
ggsave_golden(filename='../figures/nonlnear_benefits-integral.png', plot=figXb)
