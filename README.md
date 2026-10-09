# A Data Fusion Framework for Covariate Prioritization in Incomplete Short-Term Soil Nitrogen Records

Conditional effects, importance-method disagreement, and predictive limits in a five-year grazing and cover crop trial.

**Aldi Airori**, Martha Mamo, John Guretzky, Sruti Das Choudhury, Tsegaye Legesse, Gandura Abagandura

*Department of Agronomy and Horticulture* · *School of Natural Resources* · *University of Nebraska–Lincoln*

---

## Research Summary

A nine-plot grazing and cover crop trial produced five years of soil data (2019–2023) that was patchy in the way most long-term agronomic records are: where measurements available only for certain years, treatments, or sampling times. Rather than assuming which covariates drive soil nitrogen, this project fuses the field record with remote sensing, a water-balance index, and greenhouse gas flux, ranks covariates three independent ways, and then tests whether any of it supports prediction.

It does not. That negative result, and the reasons behind it, are the contribution.

This repository documents how the analysis developed across model versions, so the reasoning — including the corrections — is auditable. [`model-development-summary.pdf`](reports/model-development-summary.pdf) 

## The Framework

Five checks, applied in order, before building a forecasting pipeline on a short record. Each
is a decision point where this project would have gone wrong without it.

**1 · Let coverage decide each variable's role, before modelling anything.**
Two years at one time point support a comparison, not a trajectory. High-quality data can only
do so much if it isn't collected consistently.

**2 · Test conditional variables directly before ranking discards them.**
Grazing ranked last or near-last under every method tried, yet held the only significant
management effect in the study.

**3 · Rank covariates at least two ways, and report the disagreement.**
CO₂ flux ranked third in-sample while *degrading* held-out prediction — visible only under
permutation.

**4 · Match covariate resolution to your sampling design.**
An annual drought index on multi-season sampling is collinear with year by construction.
Extracted per sampling window, it became testable.

**5 · Run the temporal holdout first — it decides whether the rest is worth building.**
Report interval coverage *with* width. Coverage here reached 100% only because the intervals
exceeded the full observed range.

## Key Findings

**A covariate can carry a real, conditional effect without being a useful global predictor.**

- Importance ranking demonstrates this: grazing ranked last or near-last under all three
  methods — 11th of 11 under impurity importance, in the negative-importance group under
  permutation, and near the bottom under GPR length-scales. However, it is an important
  covariate within the different management systems when analyzed separately. Grazed
  unfertilized plots lost 11.48 mg kg⁻¹ NH₄⁺ and 14.99 mg kg⁻¹ NO₃⁻ by 2023
  (Mann–Whitney U; Holm-corrected p = 0.036 and 0.030 within the 2023 endpoint family), with
  no equivalent effect where fertilizer or legume nitrogen was present.

- Due to the limitation of the soil record, five annual campaigns can only support description
  and association, not prediction. Trained on 2019–2022 and tested on the held-out 2023 season,
  the model returned near-constant predictions (R² = −3.26 for NH₄⁺, −1.83 for NO₃⁻) with mean
  95% intervals of 53 and 88 mg kg⁻¹ — wider than the full observed range of either analyte.

- To address the issue of limited soil data, grouping folds by plot ID — as [Lucero et al. (2026)](https://acsess.onlinelibrary.wiley.com/doi/10.1002/saj2.70334)
  did — may suit sparse soil records better than the year-grouped folds used here, though it
  tests generalization to new plots rather than to new years.

- Another limitation is the small plot size relative to the drought index grid. Nine one-acre
  plots share a single 4.6 km pixel, so SPEI varies in time but not in space, unlike the 10 m
  vegetation and SAR covariates.

## Repository Contents

```
Notebook/           analysis pipelines (outputs cleared; see Data availability)
data/               aggregated data from v3.1 analysis
poster/             conference poster (PDF)
reports/            model reports for each version, with methods, results and corrections
CHANGELOG.md        what changed between model versions and why
FAIR-USE-OF-AI.md   disclosure of AI use
REFERENCES.md       full reference list, grouped by what each work supports

```

## Methods in Brief

| Stage | Approach |
|---|---|
| Coverage audit | Each variable assigned an analytical role from its temporal and treatment completeness |
| Covariates | NDVI, EVI, SAR-VV (Sentinel via Google Earth Engine); SPEI-90d per sampling window (GRIDMET); chamber CO₂, N₂O, CH₄ (Hutchinson–Mosier) |
| Ranking | Random Forest impurity importance, permutation importance on a held-out year, and Gaussian Process ARD length-scales |
| Grazing effect | Mann–Whitney U within treatment × year, Holm-corrected within the 2023 endpoint family |
| Model | One global GPR (Matérn ARD kernel) over 264 plot-level rows, with treatment, grazing and depth as model inputs |
| Validation | Temporal holdout (fit 2019–2022, predict 2023); leave-one-year-out cross-validation |
| Projection | Test projection year advanced to 2028; covariates held at observed means; treatments assumed unchanged |


Soil inorganic nitrogen anchors the model because it was the only variable with complete coverage across all five years, all three treatments, and both sampling times. Carbon fractions and FAME profiles cover all treatments but only at Time 2 in 2022–2023, so they support a comparison rather than a trajectory and are not analysed here.

## Model Versions

| Version | Change |
|---|---|
| v1.0 | Data assembly and experimental baseline; test the model with soil organic carbon fraction data|
| v2.0 | Anchor model. Soil inorganic nitrogen established as the response variable after the coverage audit; grazing added as a factor; NDVI and EVI extracted from Google Earth Engine |
| v2.1 | Adds SPEI; Random Forest importance ranking; per-subset GPR |
| v3.0 | Adds chamber GHG flux as covariates; adds permutation importance |
| v3.1 | Single global GPR with ARD kernel; treatment, grazing and depth become model inputs rather than filters; adds temporal holdout with interval coverage and width; SPEI extracted per sampling window rather than annually |

[`CHANGELOG.md`](CHANGELOG.md) records the corrections as well as the additions, including a placeholder drought value that propagated through earlier versions before being replaced with gridded data.

## Data Availability

This repository contains **aggregated results only** — group means with sample counts, test statistics, importance scores, and model outputs. No individual sample values are published.

Raw soil, flux, and laboratory data are available from the corresponding author on reasonable request.

Remote sensing and climate covariates are public: Sentinel-1 and Sentinel-2 via Google Earth Engine, and the GRIDMET drought product.

## Reproducing The Analysis

The notebooks run in Google Colab and expect the raw data files in a Drive folder. Without those files the notebooks will not execute end to end, but every analytical step, parameter and decision is visible in the code and documented in the reports.

Dependencies: `scikit-learn`, `pandas`, `numpy`, `scipy`, `matplotlib`, `earthengine-api`. Earth Engine access requires a registered project.

## Links

- Interactive dashboard: [`Tableau Dashboard`](https://public.tableau.com/app/profile/aldi.airori/viz/SoilNitrogenDataFusionFramework/Dashboard1#1)
- All project links: [`Aldi's Linktree`](https://linktr.ee/aldiairori?utm_source=linktree_profile_share&ltsid=eabc19c9-753e-4344-abd4-e266a5038769)
- Poster (PDF): [`Research Poster`](poster/Research-Poster.pdf)

## Citation

If you use the framework or the reported results, please cite the conference presentation:

> Airori, A., Mamo, M., Guretzky, J., Das Choudhury, S., Legesse, T., & Abagandura, G. (2026). A data fusion framework for covariate prioritization in incomplete short-term soil nitrogen records. Poster Presentation at the CANVAS 2026 Conference. Portland, Oregon.

## References

Full reference list with notes on what each work supports: [`REFERENCES.md`](REFERENCES.md)

## License

Reports, figures and documentation: CC BY 4.0. Code: MIT.

## Fair Use of AI

Read the [`description`](FAIR-USE-OF-AI.md)

## Contact

Aldi Airori — aairori2@unl.edu
Research Technologist I, Department of Agronomy and Horticulture, University of Nebraska–Lincoln
