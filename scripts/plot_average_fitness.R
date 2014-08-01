#!/usr/bin/env Rscript

if (!require("Hmisc")) install.packages("Hmisc")
if (!require("dplyr")) install.packages("dplyr")
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("devtools")) install.packages("devtools")
if (!require("ggplot2bdc")) devtools::install_github("briandconnelly/ggplot2bdc")

demo_data <- read.csv('data/demographics.csv.bz2')

summarize_demographics <- function(data)
{
    CI_size <- smean.cl.boot(data$Size, na.rm=TRUE)
    CI_fitness <- smean.cl.boot(data$AvgFitness, na.rm=TRUE)
    df <- data.frame(Size_Mean=CI_size[[1]], Size_CI_Lower=CI_size[[2]],
                     Size_CI_Upper=CI_size[[3]], Fitness_Mean=CI_fitness[[1]],
                     Fitness_CI_Lower=CI_fitness[[2]], Fitness_CI_Upper=CI_fitness[[3]])
    return(df)
}


summary_data <- demo_data %>% group_by(Time) %>% do(summarize_demographics(.))

# Plot the average size among populations
ggplot(summary_data, aes(x=Time, y=Size_Mean)) +
    geom_ribbon(aes(ymin=Size_CI_Lower, ymax=Size_CI_Upper), alpha=0.3, color=NA) +
    geom_line() +
    labs(x='Time', y='Population Size') +
    theme_bdc_grey() +
    coord_golden(xvals=summary_data$Time, yvals=summary_data$Size_Mean)
ggsave_golden('avg_popsize.pdf')


# Plot the average average (grand mean) fitness among populations
ggplot(summary_data, aes(x=Time, y=Fitness_Mean)) +
    geom_ribbon(aes(ymin=Fitness_CI_Lower, ymax=Fitness_CI_Upper), alpha=0.3, color=NA) +
    geom_line() +
    labs(x='Time', y='Fitness') +
    theme_bdc_grey() +
    coord_golden(xvals=summary_data$Time, yvals=summary_data$Fitness_Mean)
ggsave_golden('avg_fitness.pdf')

