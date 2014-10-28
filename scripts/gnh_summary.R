if (!require("Hmisc")) install.packages("Hmisc")

gnh_summary <- function(data)                                                   
{                                                                               
    cl95 <- smean.cl.boot(data)                                                 
    n <- length(data)                                                           
    df <- data.frame(N=n, Mean=cl95[[1]], Median=median(data),                  
                     CL95_lower=cl95[[2]], CL95_upper=cl95[[3]])                
    return(df)                                                                  
}

