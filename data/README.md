# Simulation Data

In most cases, each data file contains data from multiple replicate simulations.
Configuration files used to generate these data sets are available in [configuration](../configuration).

Files ending with `.bz2` are compressed with bzip2.


## Description of Included Data Sets

| File Name      | Description                                                |
|:---------------|:-----------------------------------------------------------|
| [L00.csv.bz2](L00.csv.bz2) | Combined data from simulations where no adaptation was possible (see [Figure 1A](../figures/Figure1.png)) |
| [L05_A06_1xDelta_0xEpsilon.csv.bz2](L05_A06_1xDelta_0xEpsilon.csv.bz2) | Combined data from simulations where populations could adapt to external environment, but niche construction was not possible (see [Figure 1B](../figures/Figure1.png)) |
| [L05_A06_1xDelta_1xEpsilon.csv.bz2](L05_A06_1xDelta_1xEpsilon.csv.bz2) | Combined data from simulations where adaptation to external and constructed environments possible (see Figures [1C](../figures/Figure1.png), [2A](../figures/Figure2.png)) |
| [L05_A06_2xDelta_0xEpsilon.csv.bz2](L05_A06_2xDelta_0xEpsilon.csv.bz2) | Combined data from simulations where the benefits of adaptations to the external environment were doubled, and niche construction was removed (see [Figure 2B](../figures/Figure2.png)) |
| [L05_A05_1xDelta_1xEpsilon.csv.bz2](L05_A05_1xDelta_1xEpsilon.csv.bz2) | Combined data from simulations where negative niche construction did not occur (see [Figure 2C](../figures/Figure2.png)) |
| [defector_invade_matched_nomu.csv.bz2](defector_invade_matched_nomu.csv.bz2) | Combined data from simulations where a rare defector invaded isogenic cooperator population, no mutations ([Figure 3A](../figures/Figure3.png)) |
| [defector_invade_matched_adapt.csv.bz2](defector_invade_matched_adapt.csv.bz2) | Combined data from simulations where a rare defector invaded isogenic cooperator population, adaptive mutations ([Figure 3B](../figures/Figure3.png)) |
| [cooperator_invade_cheat_noadapt.csv.bz2](cooperator_invade_cheat_noadapt.csv.bz2) | Combined data from simulations where a rare adapted cooperator invaded defector population, no mutations ([Figure 3C](../figures/Figure3.png)) |
| [defector_invade_matched_sample.csv.bz2](defector_invade_matched_sample.csv.bz2) | Data from a single representative replicate simulation in which a rare defector invaded an isogenic cooperator population, adaptive mutations ([Figure 4](../figures/Figure4.png)) |
| [cooperator_invasion.csv.bz2](cooperator_invasion.csv.bz2) | TODO ([Figure 5](../figures/cooperator_invasion.png)) |
| [cooperator_invasion.csv.bz2](cooperator_invasion.csv.bz2) | Combined data from simulations in which the benefit of cooperation was increased, and the initial proportion of cooperators was 0 ([Figure 5](../figures/cooperator_invasion.png) |
| [initial_coop_prop.csv.bz2](initial_coop_prop.csv.bz2) | Combined data from simulations using different initial cooperator proportions (Figures [S1](../figures/initial_coop_prop.png) and [S2](../figures/initial_coop_prop-integral.png)) |
| [dilution.csv.bz2](dilution.csv.bz2) | Combined data from simulations using different subpopulation dilution survival rates (Figures [S3](../figures/dilution-births.png) and [S4](../figures/dilution-births-integral.png)) |
| [nonlinear_benefits.csv.bz2](nonlinear_benefits.csv.bz2) | Combined data from simullations using different shapes for the curve describing cooperative benefits (Figures [S6](../figures/nonlinear_benefits.png) and [S7](../figures/nonlinear_benefits-integral.png)) |
| [defector_invade_matched_muboth.csv.bz2](defector_invade_matched_muboth.csv.bz2) | Combined data from simulations where a rare defector invaded isogenic cooperator population, mutations at all loci ([Figure S8](../figures/defector_invasion_mu.png)) |
| [dilution.csv.bz2](dilution.csv.bz2) | Combined data from simulations using different dilution factors, which altered how severely subpopulations were thinned at each simulation cycle |
| [nonlinear_benefits.csv.bz2](nonlinear_benefits.csv.bz2) | Combined data from simulations using different functions for the benefit of cooperation |
