# Model Configuration Files

Simulations described in the paper can be re-run using these configuration
files.  The configuration file can be specified using the `--config` argument
to `ncsimulate.py`:

```sh
python ncsimulate.py --config other_config.cfg
```

| Configuration File | Description                                                                            |
|:-------------------|:---------------------------------------------------------------------------------------|
| `L00.cfg`          | No opportunities for adaptation ([Figure 1A](../figures/Figure1.png))                  |
| `L05_A06_1xDelta_0xEpsilon.cfg` | Adaptation to external environment, but no niche construction ([Figure 1B](../figures/Figure1.png)) |
| `L05_A06_1xDelta_1xEpsilon.cfg` | Adaptation to external and constructed environments ([Figure 1C](../figures/Figure1.png), [Figure 2A](../figures/Figure2.png)) |
| `L05_A06_2xDelta_0xEpsilon.cfg` | Increased benefits for adaptation to external environment, no niche construction ([Figure 2B](../figures/Figure2.png)) |
| `L05_A05_1xDelta_1xEpsilon.cfg` | Without negative niche construction ([Figure 2C](../figures/Figure2.png)) |
| `defector_invade_matched_nomu.cfg` | Rare defector invading isogenic cooperator population, no mutations ([Figure 3A](../figures/Figure3.png)) |
| `defector_invade_matched_adapt.cfg` | Rare defector invading isogenic cooperator population, adaptive mutations ([Figure 3B](../figures/Figure3.png)) |
| `cooperator_invade_cheat_noadapt.cfg` | Rare adapted cooperator invading defector population, no mutations ([Figure 3C](../figures/Figure3.png)) |
| `defector_invade_matched_sample.cfg` | Rare defector invading isogenic cooperator population, adaptive mutations ([Figure 4](../figures/Figure4.png)) |
| `defector_invade_matched_muboth.cfg` | Rare defector invading isogenic cooperator population, mutations at all loci ([Figure S1](../figures/FigureS1.png)) |

