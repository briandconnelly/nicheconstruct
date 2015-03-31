# Wrapper for ggplot::mean_cl_boot that clips values in the range [0,1] so
# that ribbons aren't broken
figsummary <- function(x, ...)
{
    v <- mean_cl_boot(x, ...)
    v$ymin[v$ymin < 0] <- 0
    v$ymax[v$ymax > 1] <- 1
    v
}
