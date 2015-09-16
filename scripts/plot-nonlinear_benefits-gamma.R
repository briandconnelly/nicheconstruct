#!/usr/bin/env Rscript

library(ggplot2)
library(ggplot2bdc)

source('formatting.R')

S <- 2000
s <- 800

pdata <- expand.grid(Time=1:1000/1000, Gamma=c(0.25, 0.5, 1, 2, 4))
pdata$PSize <- s + ((pdata$Time^pdata$Gamma) * (S-s))

p_gamma <- ggplot(pdata, aes(x=Time, y=PSize, color=as.factor(Gamma))) +
    geom_hline(aes(yintercept=s), linetype='dotted', color='grey70') +
    geom_hline(aes(yintercept=S), linetype='dotted', color='grey70') +
    geom_line() +
    scale_color_hue(name=expression(gamma)) +
    scale_y_continuous(limits=c(0,2000), breaks=c(0,s,S),
                       labels=c('0',expression(S['min']),expression(S['max']))) +
    labs(x='Cooperator Proportion', y='Carrying Capacity') +
    theme(legend.position=c(.5, 1.035), legend.justification=c(0.5, 0.5))
p_gamma <- rescale_golden(plot=p_gamma)
ggsave_golden(filename='../figures/nonlinear_benefits-gamma.png', plot=p_gamma,
              dpi=figure_dpi)
