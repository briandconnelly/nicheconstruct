#!/usr/bin/env Rscript

library(magrittr)
library(dplyr)
library(ggplot2)
library(ggplot2bdc)

source('figsummary.R')
source('formatting.R')

tolerance_data <- read.csv('../data/tolerance.csv') 
tolerance_data$Replicate <- as.factor(tolerance_data$Replicate)

figXdata <- tolerance_data

figXintegrals <- figXdata %>%                                                 
    group_by(ToleranceMutationRate, Replicate) %>%                                      
    summarise(N=n(), Integral=sum(CooperatorProportion)/(max(Time)-min(Time)))

breaks_log <- 10^c(-5,-4,-3,-2,-1,0)
labels_log <- c(expression(paste(1, 'x', 10^{-5})),                   
                expression(paste(1, 'x', 10^{-4})),                   
                expression(paste(1, 'x', 10^{-3})),                   
                expression(paste(1, 'x', 10^{-2})),                   
                expression(paste(1, 'x', 10^{-1})),
                expression(paste(1)))
# expression(bold(paste('5', 'x', '10'^{'-2'}))),  

figX <- ggplot(data=figXintegrals, aes(x=ToleranceMutationRate, y=Integral)) +
    geom_point(shape=1, alpha=0.2) +
    stat_summary(fun.data='figsummary') +
    #scale_x_log10(breaks=unique(figXintegrals$ToleranceMutationRate)) +
    scale_x_log10(breaks=breaks_log, labels=labels_log) +
    scale_y_continuous(limits=c(0,1)) +
    labs(x=label_tolerance, y=label_cooperator_presence) +
    theme_bdc_grey(grid.y=TRUE)
figX <- rescale_golden(plot=figX)
ggsave_golden(filename='../figures/stresstolerance.pdf', plot=figX)


figXstats <- ggplot(figXdata, aes(x=Time, y=CooperatorProportion)) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +        
    stat_summary(fun.data='figsummary', geom='ribbon', color=NA, fill='black',
                 alpha=0.1) +
    stat_summary(fun.y='mean', geom='line', color='black') +
    scale_y_continuous(breaks=seq(from=0, to=1, by=0.25), limits=c(0,1)) +
    facet_grid(ToleranceMutationRate ~ .) +
    labs(x=label_time, y=label_cooperator_proportion) +
    theme_bdc_grey()

figXall <- ggplot(figXdata, aes(x=Time, y=CooperatorProportion)) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +        
    geom_line(aes(color=Replicate), alpha=0.8) +
    scale_color_hue(guide=FALSE) +
    scale_y_continuous(breaks=seq(from=0, to=1, by=0.25), limits=c(0,1)) +
    facet_grid(ToleranceMutationRate ~ .) +
    labs(x=label_time, y=label_cooperator_proportion) +
    theme_bdc_grey()
ggsave(filename='../figures/stresstolerance-all.pdf', plot=figXall)
