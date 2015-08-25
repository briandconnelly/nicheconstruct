# Simulation Data

In most cases, each data file contains data from multiple replicate simulations. 
Configuration files used to generate these data sets are available in [configuration](../configuration).

Files ending with `.bz2` are compressed with bzip2.


## Description of Included Data Sets

| File Name      | Description                                                |
|:---------------|:-----------------------------------------------------------|
| [L00.csv](L00.csv) | Combined data from simulations where no adaptation was possible (see [Figure 1A](../figures/Figure1.png)) |
| [L05_A06_1xDelta_0xEpsilon.csv](L05_A06_1xDelta_0xEpsilon) | Combined data from simulations where populations could adapt to external environment, but niche construction was not possible (see [Figure 1B](../figures/Figure1.png)) |
| [L05_A06_1xDelta_1xEpsilon.csv](L05_A06_1xDelta_1xEpsilon) | Combined data from simulations where adaptation to external and constructed environments possible (see [Figure 1C](../figures/Figure1.png), [Figure 2A](../figures/Figure2.png)) |
| [L05_A06_2xDelta_0xEpsilon.csv](L05_A06_2xDelta_0xEpsilon.csv) | Combined data from simulations where the benefits of adaptations to the external environment were doubled, and niche construction was removed (see [Figure 2B](../figures/Figure2.png)) |
| [L05_A05_1xDelta_1xEpsilon.csv](L05_A05_1xDelta_1xEpsilon.csv) | Combined data from simulations where negative niche construction did not occur (see [Figure 2C](../figures/Figure2.png)) |
| [defector_invade_matched_nomu.csv.bz2](defector_invade_matched_nomu.csv.bz2) | Combined data from simulations where a rare defector invaded isogenic cooperator population, no mutations ([Figure 3A](../figures/Figure3.png)) |
| [defector_invade_matched_adapt.csv.bz2](defector_invade_matched_adapt.csv.bz2) | Combined data from simulations where a rare defector invaded isogenic cooperator population, adaptive mutations ([Figure 3B](../figures/Figure3.png)) |
| [cooperator_invade_cheat_noadapt.csv.bz2](cooperator_invade_cheat_noadapt.csv.bz2) | Combined data from simulations where a rare adapted cooperator invaded defector population, no mutations ([Figure 3C](../figures/Figure3.png)) |
| [defector_invade_matched_sample.csv.bz2](defector_invade_matched_sample.csv.bz2) | Data from a single representative replicate simulation in which a rare defector invaded an isogenic cooperator population, adaptive mutations ([Figure 4](../figures/Figure4.png)) |
| [defector_invade_matched_muboth.csv.bz2](defector_invade_matched_muboth.csv.bz2) | Combined data from simulations where a rare defector invaded isogenic cooperator population, mutations at all loci ([Figure S1](../figures/FigureS1.png)) |
| [sweep_dilution.csv.bz2](sweep_dilution.csv.bz2) | Combined data from simulations using different dilution factors, which altered how severely subpopulations were thinned at each simulation cycle (see [Figure S2](../figures/FigureS2.png)) |
