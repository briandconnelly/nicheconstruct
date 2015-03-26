#!/usr/bin/env Rscript

replicates <- seq(0,9)
treatment <- 'L01_A06_1xDelta_1xEpsilon'
runs <- expand.grid(Treatment=treatment, Replicate=replicates)
runs$Filename <- sprintf('../data/raw/data_%s_%02d/metapopulation.csv',
                         runs$Treatment, runs$Replicate)

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
    
    data$GenomeLength <- 1
    data$Alleles <- 6
    data$Delta <- 0.3
    data$Epsilon <- 0.00015
    data$Treatment <- x['Treatment']
    data$Replicate <- as.numeric(x['Replicate'])
    
    cat('Done\n')
    return(data)
}
    
z <- apply(runs, 1, get_dataset)                                                   
z[sapply(z, is.null)] <- NULL                                                   
alldata <- do.call(rbind, z)                                                    
alldata$Replicate <- as.factor(alldata$Replicate)                               
alldata$Treatment <- as.factor(alldata$Treatment)  

write.csv(alldata, file=sprintf('../data/%s.csv', treatment), row.names=FALSE) 
