#!/usr/bin/env Rscript

library(dplyr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')

# Read the data sets
shape_data <- read.csv('../data/popsize_returns.csv.bz2') %>%
    select(Time, CooperatorProportion, Replicate, Shape)
base_data <- read.csv('../data/L05_A06_1xDelta_1xEpsilon.csv') %>%
    select(Time, CooperatorProportion, Replicate)
base_data$Shape <- 1.0

# Combine the data
alldata <- bind_rows(shape_data, base_data)

# Get the number of replicates for each treatment
# alldata %>% filter(Time==max(Time)) %>% group_by(Shape) %>% summarise(N=n())

# Make the plot
figX <- ggplot(data=alldata,
               aes(x=Time, y=CooperatorProportion)) +
    facet_grid(Shape ~ .) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') + 
    geom_line(aes(group=Replicate), color=color_cooperator, alpha=0.4) +
    scale_y_continuous(limits=c(0,1)) +
    labs(x=label_time, y=label_cooperator_proportion)
ggsave(filename='../figures/popsize_returns.png', plot=figX, dpi=300)
