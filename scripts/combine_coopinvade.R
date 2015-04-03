#!/usr/bin/env Rscript

# This is our baseline treatment

replicates <- seq(0,19)
treatment <- c('cheat', 'match', 'mismatch')
smaxes <- c(800,1100,1400,1700,2000,2300,2600)
mutations <- c('mu', 'nomu')

runs <- expand.grid(Treatment=treatment, CapacityMax=smaxes,
                    Mutations=mutations, Replicate=replicates)

runs$Filename <- sprintf('../data/raw/cooperator_invade_benefit/coopinvade_%s_%s_%04d_%02d/metapopulation.csv',
                         runs$Treatment, runs$Mutations, runs$CapacityMax, runs$Replicate)

get_dataset <- function(x)
{
    cat(sprintf('Reading data from %s ... ', x['Filename']))

    if(!file.exists(x['Filename']))
    {
        cat('File does not exist\n')
        return()
    }
    
    data <- read.csv(x['Filename'])
    
    if(nrow(data) < 1)
    {
        cat('Empty file\n')
        return()
    }
    
    data$Treatment <- x['Treatment']
    data$Mutations <- x['Mutations'] == 'mu'
    data$Benefit <- as.numeric(x['CapacityMax']) - 800
    data$Replicate <- as.numeric(x['Replicate'])
    
    cat('Done\n')
    return(data)
}
    
z <- apply(runs, 1, get_dataset)                                                   
z[sapply(z, is.null)] <- NULL                                                   
alldata <- do.call(rbind, z)                                                    
alldata$Replicate <- as.factor(alldata$Replicate)                               
alldata$Treatment <- as.factor(alldata$Treatment)  

write.csv(alldata, file='../data/cooperator_invade_benefit.csv', row.names=FALSE) 
