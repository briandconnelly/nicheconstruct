#!/usr/bin/env Rscript

library(magrittr)
library(dplyr)
library(ggplot2)
library(ggplot2bdc)

source('formatting.R')

# Read in the data sets and select the important columns that match
allneg_data <- read.csv('../data/L05_A06_1xDelta_1xEpsilon_NEGNC.csv') %>%
    select(Time, PopulationSize, CooperatorProportion, ShannonIndex, Treatment, Replicate)
highmu_data_raw <- read.csv('../data/L05_A06_1xDelta_1xEpsilon_HighMutation.csv.bz2')
highmu_data_raw$Treatment <- 'L05_A06_1xDelta_1xEpsilon_HighMutation'
highmu_data <- highmu_data_raw %>%
    select(Time, PopulationSize, CooperatorProportion, ShannonIndex, Treatment, Replicate) %>%
    filter(Replicate < 10)

fig6data <- bind_rows(allneg_data, highmu_data)
fig6data$Replicate <- as.factor(fig6data$Replicate)
fig6data$Treatment <- factor(fig6data$Treatment,
                             levels=c('L05_A06_1xDelta_1xEpsilon_NEGNC',
                                      'L05_A06_1xDelta_1xEpsilon_HighMutation'),
                             labels=c('A', 'B'))

# fig6data %>% group_by(Treatment) %>% summarise(num_replicates=length(unique(Replicate)))
# fig6data %>%
#     filter(Time==max(fig6data$Time)) %>% 
#     filter(CooperatorProportion > 0.1) %>%
#     group_by(Treatment) %>%
#     summarise(num_dominant=n())

fig6 <- ggplot(data=fig6data, aes(x=Time, y=CooperatorProportion,
                                  group=Replicate)) +
    facet_grid(. ~ Treatment) +
    geom_hline(aes(yintercept=0.5), linetype='dotted', color='grey70') +        
    geom_line(aes(group=Replicate), alpha=0.4, color=color_cooperator) +
    scale_y_continuous(breaks=seq(from=0, to=1, by=0.25), limits=c(0,1)) +
    labs(x=label_time, y=label_cooperator_proportion) +
    theme_bdc_grey() +
    
    theme(strip.background = element_blank()) +
    theme(strip.text = element_text(size=rel(1.0), face='bold'))
fig6 <- rescale_plot(plot=fig6, ratio=1/1.2)
ggsave(filename='../figures/Figure6.png', plot=fig6, dpi=300)


figS2 <- ggplot(data=fig6data, aes(x=Time, y=ShannonIndex, group=Replicate)) +
    facet_grid(. ~ Treatment) +
    geom_line(aes(group=Replicate), alpha=0.4, color=color_diversity) +
    scale_y_continuous(limits=c(0, NA)) +
    labs(x=label_time, y=label_diversity) +
    theme_bdc_grey(grid.y=TRUE) +
    theme(strip.background = element_blank()) +
    theme(strip.text = element_text(size=rel(1.0), face='bold'))
figS2 <- rescale_plot(plot=figS2, ratio=1/1.2)
ggsave(filename='../figures/FigureS2.png', plot=figS2, dpi=300)
