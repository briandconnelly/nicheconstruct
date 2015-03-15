
library(magrittr)
library(dplyr)
library(ggplot2)
library(ggplot2bdc)
library(gtable)

source('gnh_labels.R')
source('theme_gnh.R')

change_freq <- 1000

producer_proportion <- read.csv('~/Desktop/GNH/PeriodicChange/avg_prop_producers.csv.bz2')

data <- producer_proportion %>%
    filter(GenomeLength==8) %>%
    filter(PopulationStructure=='lattice, 25x25') %>%
    filter(FitnessDistribution=='uniform') %>%
    filter(MigrationRate==0.05) %>%
    filter(MutationRateSocial==1e-5) %>%
    filter(MutationRateTolerance==1e-5) %>%
    filter(MutationRateAdaptation==1e-5) %>%
    filter(ProductionCost==0.1) %>%
    filter(MinCarryingCapacity==800) %>%
    filter(MaxCarryingCapacity==2000) %>%    
    filter(EnvChangeFreq==change_freq) %>%
    filter(Replicate==17)

p <- ggplot(data, aes(x=Time, y=ProducerProportion)) +
    geom_vline(aes(xintercept=seq(from=0, to=max(data_fig3a$Time), by=change_freq)), color='grey80', size=0.1) +
    geom_hline(yintercept=0.5, linetype='dotted', size=0.5, color='grey70', size=0.1) +
    geom_line() + 
    scale_y_continuous(limits=c(0,1)) +
    scale_x_continuous(breaks=c(0,2000,4000,6000,8000,10000)) +
    labs(x=label_time, y=label_producer_proportion) +
    theme_bdc_grey()
p <- rescale_square(plot=p)

g <- ggplotGrob(p)
g <- gtable_add_grob(g, textGrob(expression(bold("B")), gp=gpar(col='black', fontsize=20), x=0, hjust=0, vjust=0.5), t=1, l=2)

png('figures/Figure1B.png', width=3, height=3, units='in', res=300)
grid.newpage()
grid.draw(g)
dev.off()

#ggsave(plot=fig3a, '../figures/Figure3a.png', width=6, height=3.708204)
