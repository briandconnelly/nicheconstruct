#!/usr/bin/env Rscript

# Plot Figure 3C

library(tidyr)
library(ggplot2)
library(ggplot2bdc)
library(gtable)

source('formatting.R')

fig3C_data <- read.csv('../data/L05_A05_1xDelta_1xEpsilon.csv')
fig3C_data$Replicate <- as.factor(fig3C_data$Replicate)

fig3C_avgfitness <- gather(fig3C_data, Type, MeanFitness, MeanCooperatorFitness,
                           MeanDefectorFitness)

fig3C <- ggplot(data=fig3C_avgfitness, aes(x=Time, y=MeanFitness, color=Type,
                                  fill=Type)) +
    geom_hline(aes(yintercept=4), linetype='dotted', color='grey70') + 
    stat_summary(fun.data='mean_cl_normal', geom='ribbon', color=NA, alpha=0.1) +
    stat_summary(fun.y='mean', geom='line') +
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
    #scale_y_continuous(limits=c(NA,4)) +
    labs(x=label_time, y=label_mean_fitness) +                                          
    theme_bdc_grey() +
    theme(legend.position=c(.5, 1.035), legend.justification=c(0.5, 0.5))
fig3C <- rescale_golden(plot=fig3C)

g <- ggplotGrob(fig3C)                                                          
g <- gtable_add_grob(g, textGrob(expression(bold('C')), gp=gpar(col='black', fontsize=20), x=0, hjust=0, vjust=0.5), t=1, l=2)

png('../figures/Figure3C.png', width=6, height=3.708204, units='in', res=300)   
grid.newpage()                                                                  
grid.draw(g)                                                                    
dev.off()
