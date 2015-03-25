# Combine all replicate data from the L05_A06_2xDelta_0xEpsilon treatment

# In this treatment, we examine whether doubling the benefits of non-social
# adaptation can allow cooperators to persist in the same way that they do when
# this same potential fitness is divided between the adaptive benefits and niche
# construction

replicates <- seq(0,9)
treatment <- 'L05_A06_2xDelta_0xEpsilon'
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
    
    data$GenomeLength <- 5
    data$Alleles <- 6
    data$Delta <- 0.6
    data$Epsilon <- 0
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

write.csv(alldata, file='../data/L05_A06_2xDelta_0xEpsilon.csv',
          row.names=FALSE) 
