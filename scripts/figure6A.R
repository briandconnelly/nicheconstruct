#!/usr/bin/env Rscript

library(magrittr)
library(dplyr)
library(ggplot2)
library(ggplot2bdc)
library(gtable)

source('formatting.R')
source('figsummary.R')

# Read the data sets
benefit_data <- read.csv('../data/benefit.csv')

base_data <- read.csv('../data/L05_A06_1xDelta_1xEpsilon.csv')
base_data$PopsizeMax <- 2000
base_data2 <- select(base_data, Time, PopulationSize, CooperatorProportion, MinCooperatorFitness, MaxCooperatorFitness, MeanCooperatorFitness, MinDefectorFitness, MaxDefectorFitness, MeanDefectorFitness, ShannonIndex, SimpsonIndex, GenomeLength, Alleles, Delta, Epsilon, PopsizeMax, Replicate)

# Combine the data sets
fig6Adata <- bind_rows(benefit_data, base_data2)
fig6Adata$Benefit <- fig6Adata$PopsizeMax - 800

# Get the area under the curve of cooperator proportion for each replicate of
# each treatment ("Cooperator Presence")
fig6Aintegrals <- fig6Adata %>%
    group_by(Benefit, Replicate) %>%
    summarise(N=n(), Integral=sum(CooperatorProportion)/(max(Time)-min(Time)))


# Make the plot
fig6A <- ggplot(data=fig6Aintegrals, aes(x=Benefit, y=Integral)) +
    geom_point(shape=1, alpha=0.2) +
    stat_summary(fun.data='figsummary') + 
    scale_y_continuous(limits=c(0,1)) + 
    labs(x=label_benefit, y=label_cooperator_presence) +
    theme_bdc_grey(grid.y=TRUE)
fig6A <- rescale_golden(plot=fig6A)

g <- ggplotGrob(fig6A)                                                          
g <- gtable_add_grob(g, textGrob(expression(bold('A')), gp=gpar(col='black', fontsize=20), x=0, hjust=0, vjust=0.5), t=1, l=2)

png('../figures/Figure6A.png', width=6, height=3.708204, units='in', res=300)   
grid.newpage()                                                                  
grid.draw(g)                                                                    
dev.off()
