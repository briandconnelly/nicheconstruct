label_time <- 'Time (T)'
label_genome_length <- 'Genome Length (L)'
label_migration_rate <- 'Migration Rate (m)'
label_producer_proportion <- 'Producer Proportion'
label_producer_presence <- 'Producer Presence'
label_stressmu <- expression(bold(paste('Survival Mutation Rate (', mu[t], ')')))

label_mu <- expression(bold(paste('Mutation Rate (', mu[p], ', ', mu[s], ')')))
label_socialmu <- expression(bold(paste('Mutation Rate at Social Locus (', mu[p], ')')))

label_producer_proportion_sd <- expression(bold(paste(sigma, '(Proportion of Producers Surviving)')))

# TODO: highlight base values in labels with bold text or asterisk

mutation_labels <- c('1e-7'='0.0000001', '1e-6'='0.000001', '1e-5'='0.00001', '1e-4'='0.0001', '1e-3'='0.001', '1e-2'='0.01', '1e-1'='0.1')
