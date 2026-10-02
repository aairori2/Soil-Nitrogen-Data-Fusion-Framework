# A Data Fusion Framework for Covariate Prioritization in Incomplete Short-Term Soil Nitrogen Records

Conditional effects, importance-method disagreement, and predictive limits in a five-year grazing and cover crop trial.

**Aldi Airori**, Martha Mamo, John Guretzky, Sruti Das Choudhury, Tsegaye Legesse, Gandura Abagandura
Department of Agronomy and Horticulture · School of Natural Resources · University of Nebraska–Lincoln

---

## What this is

A nine-plot grazing and cover crop trial produced five years of soil data (2019–2023) that was patchy in the way most long-term agronomic records are: some variables measured in some years, some treatments, some sampling times. Rather than assuming which covariates drive soil nitrogen, this project fuses the field record with remote sensing, a water-balance index, and greenhouse gas flux, ranks covariates three independent ways, and then tests whether any of it supports prediction.

It does not. That negative result, and the reasons behind it, are the contribution.

This repository documents how the analysis developed across model versions, so the reasoning — including the corrections — is auditable.

## Key findings

**Grazing depletes soil nitrogen only where no input replaces it.** Unfertilized plots lost 11.48 mg kg⁻¹ NH₄⁺ and 14.99 mg kg⁻¹ NO₃⁻ under grazing by 2023 (Mann–Whitney U; Holm-corrected p = 0.036 and 0.030 within the 2023 endpoint family). Fertilized and legume-interseeded plots showed no significant effect.

**Every importance method ranked grazing last or near-last anyway.** Impurity importance placed it 11th of 11, permutation importance put it in the negative-importance group, and GPR length-scales ranked it near the bottom. A covariate can carry a real, conditional effect without being a useful global predictor — global importance asks whether a variable separates the whole dataset, and one acting within a single treatment cannot.

**Five annual campaigns do not support forward prediction.** Trained on 2019–2022 and tested on the held-out 2023 season, the model returned near-constant predictions (R² = −3.26 for NH₄⁺, −1.83 for NO₃⁻) with mean 95% credible intervals of 53 and 88 mg kg⁻¹ — wider than the full observed range of either analyte. Interval coverage reached 100% only for that reason, which is why coverage is reported alongside width.

## Repository contents

```
reports/        model reports for each version, with methods, results and corrections
REFERENCES.md   full reference list, grouped by what each work supports
notebooks/      analysis pipelines (outputs cleared; see Data availability)
figures/        poster and dashboard graphics
poster/         conference poster (PDF)
CHANGELOG.md    what changed between model versions and why
```

## Methods in brief

| Stage | Approach |
|---|---|
| Coverage audit | Each variable assigned an analytical role from its temporal and treatment completeness |
| Covariates | NDVI, EVI, SAR-VV (Sentinel via Google Earth Engine); SPEI-90d per sampling window (GRIDMET); chamber CO₂, N₂O, CH₄ (Hutchinson–Mosier) |
| Ranking | Random Forest impurity importance, permutation importance on a held-out year, and Gaussian Process ARD length-scales |
| Model | One global GPR (Matérn ARD kernel) over 264 plot-level rows, with treatment, grazing and depth as model inputs |
| Validation | Temporal holdout (fit 2019–2022, predict 2023); leave-one-year-out cross-validation |
| Grazing effect | Mann–Whitney U within treatment × year, Holm-corrected within the 2023 endpoint family |

Soil inorganic nitrogen anchors the model because it was the only variable with complete coverage across all five years, all three treatments, and both sampling times. Carbon fractions and FAME profiles cover all treatments but only at Time 2 in 2022–2023, so they support a comparison rather than a trajectory and are not analysed here.

## Model versions

| Version | Change |
|---|---|
| v1.0 | Experimental baseline. NH₄⁺/NO₃⁻ trajectories by treatment, fitted with GPR on year alone — no covariates |
| v2.0 | Anchor model. Soil inorganic nitrogen established as the response variable after the coverage audit; grazing added as a factor; still no remote sensing covariates |
| v2.1 | Adds Google Earth Engine covariates and SPEI; Random Forest importance ranking; per-subset GPR |
| v3.0 | Adds chamber GHG flux as covariates; adds permutation importance |
| v3.1 | Single global GPR with ARD kernel; treatment, grazing and depth become model inputs rather than filters; adds temporal holdout with interval coverage and width; SPEI extracted per sampling window rather than annually |

`CHANGELOG.md` records the corrections as well as the additions, including a placeholder drought value that propagated through earlier versions before being replaced with gridded data.

## Data availability

This repository contains **aggregated results only** — group means with sample counts, test statistics, importance scores, and model outputs. No individual sample values are published.

Raw soil, flux, and laboratory data are available from the corresponding author on reasonable request.

Remote sensing and climate covariates are public: Sentinel-1 and Sentinel-2 via Google Earth Engine, and the GRIDMET drought product.

## Reproducing the analysis

The notebooks run in Google Colab and expect the raw data files in a Drive folder. Without those files the notebooks will not execute end to end, but every analytical step, parameter and decision is visible in the code and documented in the reports.

Dependencies: `scikit-learn`, `pandas`, `numpy`, `scipy`, `matplotlib`, `earthengine-api`. Earth Engine access requires a registered project.

## Links

- Interactive dashboard: [REPLACE WITH TABLEAU PUBLIC URL]
- All project links: [REPLACE WITH LINKTREE URL]
- Poster (PDF): `poster/`

## Citation

If you use the framework or the reported results, please cite the conference presentation:

> Airori, A., Mamo, M., Guretzky, J., Das Choudhury, S., Legesse, T., & Abagandura, G. (2026). *A data fusion framework for covariate prioritization in incomplete short-term soil nitrogen records.* [CONFERENCE NAME, LOCATION, DATE].

## References

Full reference list with notes on what each work supports: [`REFERENCES.md`](REFERENCES.md)

## License

Reports, figures and documentation: CC BY 4.0. Code: MIT.

## Contact

Aldi Airori — aairori2@unl.edu
Research Technologist, Department of Agronomy and Horticulture, University of Nebraska–Lincoln
