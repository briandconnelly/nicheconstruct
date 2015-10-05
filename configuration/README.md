# Model Configuration Files

Simulations described in the paper can be re-created using these configuration
files.  The configuration file can be specified using the `--config` argument
to `ncsimulate.py`:

```sh
python ncsimulate.py --config other_config.cfg
```

## Description of Included Configuration Files

| File               | Description                                                                            |
|:-------------------|:---------------------------------------------------------------------------------------|
| [L00.cfg](L00.cfg) | No opportunities for adaptation ([Figure 1a](../figures/Figure1.png))                  |
| [L05_A06_1xDelta_0xEpsilon.cfg](L05_A06_1xDelta_0xEpsilon.cfg) | Adaptation to external environment, but no niche construction ([Figure 1b](../figures/Figure1.png)) |
| [L05_A06_1xDelta_1xEpsilon.cfg](L05_A06_1xDelta_1xEpsilon.cfg) | Adaptation to external and constructed environments ([Figure 1c](../figures/Figure1.png), [Figure 2a](../figures/Figure2.png)) |
| [L05_A06_2xDelta_0xEpsilon.cfg](L05_A06_2xDelta_0xEpsilon.cfg) | Increased benefits for adaptation to external environment, no niche construction ([Figure 2b](../figures/Figure2.png)) |
| [L05_A05_1xDelta_1xEpsilon.cfg](L05_A05_1xDelta_1xEpsilon.cfg) | Without negative niche construction ([Figure 2c](../figures/Figure2.png)) |
| [defector_invade_matched_nomu.cfg](defector_invade_matched_nomu.cfg) | Rare defector invading isogenic cooperator population, no mutations ([Figure 3a](../figures/Figure3.png)) |
| [defector_invade_matched_adapt.cfg](defector_invade_matched_adapt.cfg) | Rare defector invading isogenic cooperator population, adaptive mutations ([Figure 3b](../figures/Figure3.png)) |
| [cooperator_invade_cheat_noadapt.cfg](cooperator_invade_cheat_noadapt.cfg) | Rare adapted cooperator invading defector population, no mutations ([Figure 3c](../figures/Figure3.png)) |
| [defector_invade_matched_sample.cfg](defector_invade_matched_sample.cfg) | Rare defector invading isogenic cooperator population, adaptive mutations ([Figure 4](../figures/Figure4.png)) |
| [cooperator_invasionl.cfg](cooperator_invasionl.cfg) | Cooperator invasion with niche construction feedbacks ([Figure 5a](../figures/cooperator_invasion.png)) |
| [cooperator_invasion-ctrl.cfg](cooperator_invasion-ctrl.cfg) | Cooperator invasion without niche construction feedbacks ([Figure 5b](../figures/cooperator_invasion.png)) |
| [dilution.cfg](dilution.cfg) | Populations evolved for at least 2822103628 births to explore effect of dilution survival rate (Figures [S3](../figures/dilution-births.png) and [S4](../figures/dilution-births-integral.png))|
| [defector_invade_matched_muboth.cfg](defector_invade_matched_muboth.cfg) | Rare defector invading isogenic cooperator population, mutations at all loci ([Figure S8](../figures/defector_invasion_mu.png)) |
