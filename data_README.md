# Aggregated data

Published results only. Every file holds group summaries, test statistics or model output;
no individual sample values appear in this repository. Groups smaller than three samples are
omitted so that no reported mean is effectively a single measurement.

Raw soil, flux and laboratory data are available from the corresponding author on reasonable
request.

---

## `dash_coverage.csv`
Result of the coverage audit: one row per variable per year.

| Column | Description |
|---|---|
| `variable` | Measured variable or variable group |
| `year` | 2019–2023 |
| `status` | `Complete`, `All treatments`, `Time 2 only`, `Plot IDs lost`, `Not collected` |
| `role` | Analytical role the coverage supports: `Response`, `Covariate`, `Baseline`, `Snapshot` |

## `dash_n_means.csv`
Soil inorganic nitrogen, summarised by treatment, grazing, depth, year and sampling time.

| Column | Description |
|---|---|
| `analyte` | `NH4` or `NO3` |
| `treatment` | `Unfertilized`, `Fertilized`, `Legume` |
| `grazing` | `Yes` or `No` |
| `depth_cm` | `0-10` or `10-20` |
| `year` | 2019–2023 |
| `time_point` | `T0` baseline, `T1` July, `T2` September |
| `mean`, `sd` | Group mean and standard deviation, mg kg⁻¹ |
| `n` | Samples in the group (minimum 3) |

## `dash_relevance.csv`
Covariate relevance under three ranking methods, for both analytes.

| Column | Description |
|---|---|
| `analyte` | `NH4` or `NO3` |
| `method` | `RF impurity`, `Permutation (change in MSE)`, `GPR ARD` |
| `covariate` | Covariate name; treatment appears as one-hot terms under `GPR ARD` |
| `value` | RF impurity and GPR ARD are shares summing to 1. Permutation is the change in held-out mean squared error when the covariate is shuffled; negative means shuffling improved prediction |
| `rank` | Rank within analyte and method, 1 = highest |

**Scales are not comparable between methods.** Shares and MSE changes are different quantities.

## `dash_grazing_effects.csv`
Grazed versus ungrazed comparison within each treatment and year.

| Column | Description |
|---|---|
| `analyte` | `NH4` or `NO3` |
| `treatment`, `year` | Comparison group |
| `mean_grazed`, `sd_grazed`, `n_grazed` | Grazed strips |
| `mean_ungrazed`, `sd_ungrazed`, `n_ungrazed` | Ungrazed strips |
| `diff` | Grazed minus ungrazed, mg kg⁻¹ |
| `p_value` | Mann–Whitney U, two-sided, uncorrected |
| `p_holm_2023` | Holm-corrected p within the 2023 endpoint family (6 tests); blank for other years |
| `sig_uncorrected` | `*` p < 0.05, `**` p < 0.01, uncorrected |

Legume strips were not sampled in 2020, so those rows are absent. 2019 predates grazing.

## `dash_spei.csv`
Water-balance index per sampling window, from GRIDMET (~4.6 km grid). All nine plots fall
within a single grid cell, so values vary in time but not between plots.

| Column | Description |
|---|---|
| `year`, `time_point` | Sampling window |
| `spei30d`, `spei90d`, `spei180d` | SPEI at three accumulation windows; negative is drier. `spei90d` is used in the model |

## `dash_holdout_points.csv`
Temporal holdout predictions. Points are plot-level means, not individual samples.

| Column | Description |
|---|---|
| `analyte` | `NH4` or `NO3` |
| `observed` | Measured 2023 value, mg kg⁻¹ |
| `predicted` | Model prediction from training on 2019–2022 |
| `lower95`, `upper95` | 95% credible interval |
| `inside95` | Whether the observation fell inside its interval |

## `dash_holdout_metrics.csv`
Summary of the same holdout.

| Column | Description |
|---|---|
| `analyte` | `NH4` or `NO3` |
| `n_train`, `n_test` | Rows used |
| `rmse`, `mae`, `bias` | Error metrics, mg kg⁻¹ |
| `r2` | Negative values indicate prediction worse than the test-set mean |
| `coverage95` | Fraction of observations inside their interval |
| `mean_interval_width` | Mean width of the 95% interval, mg kg⁻¹ — read alongside coverage |

## `dash_plots.csv`
Plot layout for mapping.

| Column | Description |
|---|---|
| `plot_id` | 101–303 |
| `treatment` | `Unfertilized`, `Fertilized`, `Legume` |
| `lat`, `lon` | Plot centroid, rounded to five decimal places (about 1 m) |
