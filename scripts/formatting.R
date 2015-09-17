figure_dpi <- 300

label_time <- 'Time'
label_births <- 'Births'
label_cooperator_proportion <- 'Cooperator Proportion'
label_cooperator_presence <- 'Cooperator Presence'
label_cooperator_presence_scaled <- 'Scaled Cooperator Presence'
label_mean_fitness <- 'Mean Fitness'
label_tolerance <- 'Survival Rate, Initial Environmental Change'
label_dilutionsurvival <- 'Dilution Survival Rate'
label_benefit_slope <- 'Slope of Cooperative Benefit'
label_carrying_capacity <- 'Subpopulation Carrying Capacity'
label_initial_cooperator_proportion <- 'Initial Cooperator Proportion'
label_initial_cooperator_proportion_actual <- 'Cooperator Proportion after Initial Thinning'

color_cooperator <- '#729ECE'
color_defector <- '#ED665D'

ribbon_alpha <- 0.2
replicate_alpha <- 0.1

theme_negniche <- function()
{
    ggplot2bdc::theme_bdc_grey(base_size=12) +
        theme(strip.background = element_blank()) +
        theme(strip.text = element_text(size=rel(1.0), vjust=0.2, face='bold'))
}

ggplot2::theme_set(theme_negniche())

