label_time <- 'Time (T)'
label_genome_length <- 'Genome Length (L)'
label_migration_rate <- 'Migration Rate (m)'
label_producer_proportion <- 'Producer Proportion'
label_producer_presence <- 'Producer Presence'
label_stressmu <- expression(bold(paste('Stress Tolerance Mutation Rate (', mu[t], ')')))
label_genomelengths <- c('0', '1', '2', '3', '4', '5', '6', '7', expression(bold('8')), '9', '10')
label_genomelengths08 <- c('0', expression(bold('8')) )
label_structure <- c('lattice, 25x25'=expression(bold('Structured')), 'well-mixed, 625'='Unstructured')

label_mu <- expression(bold(paste('Mutation Rate (', mu[p], ', ', mu[s], ')')))
label_socialmu <- expression(bold(paste('Mutation Rate at Social Locus (', mu[p], ')')))

label_producer_proportion_sd <- expression(bold(paste(sigma, '(Proportion of Producers Surviving)')))

label_benefit <- 'Production Benefit'
label_benefits <- c('0', '200', '400', '600', '800', '1000', expression(bold('1200')), '1400', '1600', '1800', '2000')

# TODO: highlight base values in labels with bold text or asterisk

mutation_labels <- c('1e-7'='0.0000001', '1e-6'='0.000001',
                     '1e-5'=expression(bold('0.00001')), '1e-4'='0.0001',
                     '1e-3'='0.001', '1e-2'='0.01', '1e-1'='0.1')
