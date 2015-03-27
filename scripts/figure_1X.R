#!/usr/bin/env Rscript

library(magrittr)
library(ggplot2)
library(ggplot2bdc)
library(gtable)

source('formatting.R')

fig1X_data <- read.csv('../data/L05_A05_1xDelta_1xEpsilon.csv')
fig1X_data$Replicate <- as.factor(fig1X_data$Replicate)

fig1X <- ggplot(data=fig1X_data, aes(x=Time, y=CooperatorProportion)) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +        
    stat_summary(fun.data='mean_cl_normal', geom='ribbon', color=NA, fill='black', alpha=0.1) +
    stat_summary(fun.y='mean', geom='line', color='black') +
    scale_y_continuous(breaks=seq(from=0, to=1, by=0.25), limits=c(0,1)) +
    labs(x=label_time, y=label_cooperator_proportion) +
    theme_bdc_grey()
fig1X <- rescale_square(plot=fig1X)

g <- ggplotGrob(fig1X)                                                          
g <- gtable_add_grob(g, textGrob(expression(bold('X')), gp=gpar(col='black', fontsize=20), x=0, hjust=0, vjust=0.5), t=1, l=2)

png('../figures/Figure1X.png', width=6, height=6, units='in', res=300)   
grid.newpage()                                                                  
grid.draw(g)                                                                    
dev.off()

# Save a version with each replicate shown
ggsave(filename='../figures/Figure1X-all.png',
       plot=fig1X + geom_line(aes(color=Replicate)) + scale_color_hue(guide=FALSE),
       width=6, height=6, units='in', dpi=300)
