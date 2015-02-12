library(magrittr)
library(dplyr)
library(ggplot2)
library(ggplot2bdc)
library(gtable)

load(file='~/Dropbox/Research/Models/niche_hike/data/producer_proportion.rda')
source('~/Dropbox/Research/Models/niche_hike/scripts/gnh_labels.R')
source('~/Dropbox/Research/Models/niche_hike/scripts/theme_gnh.R')
source('~/Dropbox/Research/Models/niche_hike/scripts/gnh_summary.R')

data <- producer_proportion %>%
    filter(PopulationStructure=='lattice, 25x25') %>%
    filter(FitnessDistribution=='uniform') %>%
    filter(MigrationRate==0.05) %>%
    filter(MutationRateSocial==1e-5) %>%
    filter(MutationRateTolerance==1e-5) %>%
    filter(MutationRateAdaptation==1e-5) %>%
    filter(ProductionCost==0.1) %>%
    filter(MinCarryingCapacity==800) %>%
    filter(MaxCarryingCapacity==2000) %>%
    filter(is.na(EnvChangeFreq)) %>%
    filter(Source=='GenomeLength')
    

stats <- data %>%                                                  
    group_by(GenomeLength, Time) %>% 
    do(gnh_summary(.$MeanProducerProportion)) %>%
    filter(GenomeLength %in% c(0,3,6,8)) %>%
    filter(Time < 2000)

stats$GenomeLength <- as.factor(stats$GenomeLength)


p <- ggplot(stats, aes(x=Time, y=Mean, color=GenomeLength, fill=GenomeLength)) +
    geom_hline(yintercept=0.5, linetype='dotted', size=0.5, color='grey70') +
    geom_ribbon(aes(ymin=Emin, ymax=Emax), color=NA, alpha=0.2) +
    geom_line() +
    scale_fill_hue(guide=FALSE) +
    scale_color_hue(name='Stress Loci') +
    labs(x='Time', y='Cooperator Proportion') +
    theme_bdc_grey() +
    theme(legend.position=c(.5, 1.035), legend.justification=c(0.5, 0.5))
p <- rescale_square(plot=p)

g <- ggplotGrob(p)
g <- gtable_add_grob(g, textGrob(expression(bold("A")), gp=gpar(col='black', fontsize=20), x=0, hjust=0, vjust=0.5), t=1, l=2)

png('figures/Figure1A.png', width=3, height=3, units='in', res=300)
grid.newpage()
grid.draw(g)
dev.off()

