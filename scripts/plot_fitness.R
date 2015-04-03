#!/usr/bin/env Rscript

library(magrittr)
library(dplyr)
library(tidyr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')

base_data <- read.csv('../data/L05_A06_1xDelta_1xEpsilon.csv')
delta_data <- read.csv('../data/L05_A06_2xDelta_0xEpsilon.csv')
posnc_data <- read.csv('../data/L05_A05_1xDelta_1xEpsilon.csv')
negnc_data <- read.csv('../data/L01_A06_1xDelta_1xEpsilon.csv')

fig3data <- bind_rows(base_data, delta_data, posnc_data, negnc_data)
fig3data$Replicate <- as.factor(fig3data$Replicate)
fig3data$Treatment <- factor(fig3data$Treatment,
                             levels=c('L05_A06_1xDelta_1xEpsilon',
                                      'L05_A06_2xDelta_0xEpsilon',
                                      'L05_A05_1xDelta_1xEpsilon',
                                      'L01_A06_1xDelta_1xEpsilon'),
                             labels=c('A', 'B', 'C', 'D'))
fig3data$Row[fig3data$Treatment=='A'] <- 1
fig3data$Row[fig3data$Treatment=='B'] <- 1
fig3data$Row[fig3data$Treatment=='C'] <- 2
fig3data$Row[fig3data$Treatment=='D'] <- 2
fig3data$Col[fig3data$Treatment=='A'] <- 1
fig3data$Col[fig3data$Treatment=='B'] <- 2
fig3data$Col[fig3data$Treatment=='C'] <- 1
fig3data$Col[fig3data$Treatment=='D'] <- 2

fig3_avgfitness <- gather(fig3data, Type, MeanFitness, MeanCooperatorFitness,
                          MeanDefectorFitness)

maxfitnesses <- data.frame(Treatment=c('L05_A06_1xDelta_1xEpsilon',
                                       'L05_A06_2xDelta_0xEpsilon',
                                       'L05_A05_1xDelta_1xEpsilon',
                                       'L01_A06_1xDelta_1xEpsilon'),
                           MaxCFitness=c(3.6, 3.9, 3.9, 1.2),
                           MaxDFitness=c(3.7, 4, 4, 1.3))
maxfitnesses$Treatment <- factor(maxfitnesses$Treatment,
                                 levels=c('L05_A06_1xDelta_1xEpsilon',
                                          'L05_A06_2xDelta_0xEpsilon',
                                          'L05_A05_1xDelta_1xEpsilon',
                                          'L01_A06_1xDelta_1xEpsilon'),
                                 labels=c('A', 'B', 'C', 'D'))
maxfitnesses$Row[maxfitnesses$Treatment %in% c('A','B')] <- 1
maxfitnesses$Row[maxfitnesses$Treatment %in% c('C','D')] <- 2
maxfitnesses$Col[maxfitnesses$Treatment %in% c('A','C')] <- 1
maxfitnesses$Col[maxfitnesses$Treatment %in% c('B','D')] <- 2

facet_labels <- data.frame(Time=c(0,0,0,0), MeanFitness=c(4,4,4,4),
                           Type=c('MeanDefectorFitness','MeanDefectorFitness','MeanDefectorFitness','MeanDefectorFitness'),                 
                           Row=c(1,1,2,2),                             
                           Col=c(1,2,1,2),               
                           Label=c('A','B','C','D')) 

fig3 <- ggplot(data=fig3_avgfitness, aes(x=Time, y=MeanFitness, color=Type, fill=Type)) +
    #facet_wrap(~ Treatment, ncol=2) +
    facet_grid(Row ~ Col) +
    geom_hline(data=maxfitnesses, aes(yintercept=MaxCFitness), linetype='dashed', color='grey70') +
    geom_hline(data=maxfitnesses, aes(yintercept=MaxDFitness), linetype='dashed', color='grey70') +
    stat_summary(fun.data='mean_cl_normal', geom='ribbon', color=NA, alpha=0.1) +
    stat_summary(fun.y='mean', geom='line') +
    geom_text(data=facet_labels, aes(label=Label), vjust=1, hjust=0, color='black') +
    scale_color_manual(name='Type',                                             
                       labels=c('MeanDefectorFitness'='Defector',               
                                'MeanCooperatorFitness'='Cooperator'),          
                       values=c('MeanDefectorFitness'=color_defector,                
                                'MeanCooperatorFitness'=color_cooperator)) +           
    scale_fill_manual(name='Type', guide=FALSE,                                 
                      labels=c('MeanDefectorFitness'='Defector',                
                               'MeanCooperatorFitness'='Cooperator'),           
                      values=c('MeanDefectorFitness'=color_defector,                 
                               'MeanCooperatorFitness'=color_cooperator)) + 
    labs(x=label_time, y=label_mean_fitness) +                                          
    theme_bdc_grey() +
    theme(strip.background = element_blank()) +
    theme(strip.text = element_blank()) +
    theme(legend.position=c(.5, 1.035), legend.justification=c(0.5, 0.5))

fig3 <- rescale_square(plot=fig3)
ggsave(filename='../figures/Figure3.png', plot=fig3, dpi=300)

