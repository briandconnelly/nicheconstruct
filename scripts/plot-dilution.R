#!/usr/bin/env Rscript

library(dplyr)
library(magrittr)
library(ggplot2)
library(ggplot2bdc)
library(gtable)

source('figsummary.R')
source('formatting.R')

dilutiondata <- read.csv(bzfile('../data/dilution.csv.bz2'))
dilutiondata$Replicate <- as.factor(dilutiondata$Replicate)

figXa <- ggplot(data=dilutiondata,
                aes(x=Time, y=CooperatorProportion, color=as.factor(Replicate))) +
    facet_grid(DilutionSurvival ~ . ) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +
    geom_line() +
    scale_color_grey(guide=FALSE) +
    scale_y_continuous(limits=c(0,1), breaks=c(0,0.5,1)) +
    labs(x=label_time, y=label_cooperator_proportion)
ggsave(filename='../figures/dilution-time.png', plot=figXa, dpi=figure_dpi)

# png('../figures/dilution-time.png', width=7.22, height=8.18, units='in',
#     res=figure_dpi)
# gA <- gtable_add_grob(ggplotGrob(figXa), textGrob(expression(bold("A")),
#                                                   gp=gpar(col='black',
#                                                           fontsize=20),
#                                                   x=0, hjust=0, vjust=0.5), t=1, l=2)
# grid.draw(gA)
# dev.off()


figXb <- ggplot(data=dilutiondata,
                aes(x=Births, y=CooperatorProportion, color=as.factor(Replicate))) +
    facet_grid(DilutionSurvival ~ . ) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +
    geom_line() +
    scale_color_grey(guide=FALSE) +
    scale_y_continuous(limits=c(0,1), breaks=c(0,0.5,1)) +
    labs(x=label_births, y=label_cooperator_proportion)
ggsave(filename='../figures/dilution-births.png', plot=figXb, dpi=figure_dpi)

# png('../figures/dilution-births.png', width=7.22, height=8.18, units='in',
#     res=figure_dpi)
# gB <- gtable_add_grob(ggplotGrob(figXb), textGrob(expression(bold("B")),
#                                                   gp=gpar(col='black',
#                                                           fontsize=20),
#                                                   x=0, hjust=0, vjust=0.5), t=1, l=2)
# grid.draw(gB)
# dev.off()


presence <- dilutiondata %>%
    group_by(DilutionSurvival, Replicate) %>%
    summarise(Integral=sum(CooperatorProportion)/n())

figXc <- ggplot(data=presence, aes(x=DilutionSurvival, y=Integral)) +
    geom_point(shape=1, alpha=replicate_alpha) +
    stat_summary(fun.data='figsummary') +
    scale_y_continuous(limits=c(0,1)) +
    scale_x_continuous(limits=c(0,1)) +
    labs(x=label_dilutionsurvival, y=label_cooperator_presence_scaled)
figXc <- rescale_golden(plot=figXc)
ggsave_golden(filename='../figures/dilution-births-integral.png', plot=figXc,
              dpi=figure_dpi)

# png('../figures/dilution-births-integral.png', width=6, height=3.708204,
#     units='in', res=figure_dpi)
# gC <- gtable_add_grob(ggplotGrob(figXc), textGrob(expression(bold("C")),
#                                                   gp=gpar(col='black', fontsize=20),
#                                                   x=0, hjust=0, vjust=0.5), t=1, l=2)
# grid.draw(gC)
# dev.off()

# How many cycles does it take to get to the same number of births?
# x2 <- dilutiondata %>%
#     group_by(DilutionSurvival, Replicate) %>%
#     filter(Births >= 2822103628) %>%
#     summarise(TimeToThresh=min(Time))
# ggplot(x2, aes(x=DilutionSurvival, y=TimeToThresh)) +
#     stat_summary(fun.data='mean_cl_boot', geom='errorbar', width=0) +
#     stat_summary(fun.y='mean', geom='point') + 
#     scale_x_continuous(limits=c(0,1))
