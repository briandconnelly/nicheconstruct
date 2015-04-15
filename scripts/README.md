# Analysis Scripts

These scripts are used to analyze the [data](../data) and create the
[figures](../figures).

## Dependencies

* [R](http://www.r-project.org) (version 3.1.3 used)
* [magrittr](http://cran.r-project.org/web/packages/magrittr/) (version 1.5 used)
* [dplyr](http://cran.r-project.org/web/packages/dplyr/) (version 0.4.1 used)
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
| [figureS1.R](figureS1.R) | Create [Figure S1](../figures/FigureS1.png) |
| [formatting.R](formatting.R) | Define some variables for formatting figures |
| [figsummary.R](figsummary.R) | Function for calculating statistics shown in [Figure 1](../figures/Figure1.png) |

