#!/usr/bin/env Rscript

# Plot Figure 1C
#
# Dependencies can be installed with:
#    install.packages(c('magrittr', 'ggplot2', 'devtools', 'gtable'))
#    devtools::install_github('briandconnelly/ggplot2bdc')

library(magrittr)
library(ggplot2)
library(ggplot2bdc)
library(gtable)

source('formatting.R')

fig1C_data <- read.csv('../data/L05_A06_1xDelta_1xEpsilon.csv')
fig1C_data$Replicate <- as.factor(fig1C_data$Replicate)

fig1C <- ggplot(data=fig1C_data, aes(x=Time, y=CooperatorProportion)) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +        
    stat_summary(fun.data='mean_cl_normal', geom='ribbon', color=NA, fill='black', alpha=0.1) +
    stat_summary(fun.y='mean', geom='line', color='black') +
    scale_y_continuous(breaks=seq(from=0, to=1, by=0.25), limits=c(0,1)) +
    labs(x=label_time, y=label_cooperator_proportion) +
    theme_bdc_grey()
fig1C <- rescale_square(plot=fig1C)

g <- ggplotGrob(fig1C)                                                          
g <- gtable_add_grob(g, textGrob(expression(bold('C')), gp=gpar(col='black', fontsize=20), x=0, hjust=0, vjust=0.5), t=1, l=2)

png('../figures/Figure1C.png', width=6, height=6, units='in', res=300)   
grid.newpage()                                                                  
grid.draw(g)                                                                    
dev.off()

# Save a version with each replicate shown
ggsave(filename='../figures/Figure1C-all.png',
       plot=fig1C + geom_line(aes(color=Replicate)) + scale_color_hue(guide=FALSE),
       width=6, height=6, units='in', dpi=300)
