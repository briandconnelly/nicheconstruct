# Analysis Scripts

These scripts are used to analyze the [data](../data) and create the
[figures](../figures).

## Dependencies

* [R](http://www.r-project.org) (version 3.2.2 used)
* [magrittr](http://cran.r-project.org/web/packages/magrittr/) (version 1.5 used)
* [dplyr](http://cran.r-project.org/web/packages/dplyr/) (version 0.4.3 used)
* [ggplot2](http://cran.r-project.org/web/packages/ggplot2/) (version 1.0.1 used)
* [ggplot2bdc](https://github.com/briandconnelly/ggplot2bdc) (version 0.2.0 used)

These packages can be installed in R using the following commands:

```r
install.packages(c('magrittr', 'dplyr', 'ggplot2', 'devtools'))
devtools::install_github('briandconnelly/ggplot2bdc')
```

## Contents

| File               | Description                                       |
|:-------------------|:--------------------------------------------------|
| [figure1.R](figure1.R) | Create [Figure 1](../figures/Figure1.png)     |
| [figure2.R](figure2.R) | Create [Figure 2](../figures/Figure2.png)     |
| [figure3.R](figure3.R) | Create [Figure 3](../figures/Figure3.png)     |
| [figure4.R](figure4.R) | Create [Figure 4](../figures/Figure4.png)     |
| [plot-cooperator_invasion.R](plot-cooperator_invasion.R) | Create [Figure 5](../figures/cooperator_invasion.png) |
| [plot-initial_coop_prop.R](plot-initial_coop_prop.R) | Create Figures [S1](../figures/initial_coop_prop.png) and [S2](../figures/initial_coop_prop-integral.png) |
| [plot-dilution.R](plot-dilution.R) | Create Figures [S3](../figures/dilution-births.png) and [S4](../figures/dilution-births-integral.png) |
| [plot-nonlinear_benefits-gamma.R](plot-nonlinear_benefits-gamma.R) | Create [Figure S5](../figures/nonlinear_benefits-gamma.png) |
| [plot-nonlinear_benefits.R](plot-nonlinear_benefits.R) | Create Figures [S6](../figures/plot-nonlinear_benefits-gamma.R) and [S7](../figures/plot-nonlinear_benefits-gamma.R) |

| [plot-defector_invasion_mu.R](plot-defector_invasion_mu.R) | Create [Figure S8](../figures/defector_invasion_mu.png) |
| [formatting.R](formatting.R) | Define some variables for formatting figures |
| [figsummary.R](figsummary.R) | Function for calculating bounded confidence intervals |

