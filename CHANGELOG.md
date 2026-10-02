# Changelog

How the analysis developed, and what was corrected along the way. Corrections are listed
alongside additions deliberately: several findings changed when errors were found, and the
record of that is part of what this repository documents.

---

## v3.1 — current

**Added**
- Single global Gaussian Process over all 264 plot-level rows, replacing the 18 per-subset
  models of v3.0. Treatment, grazing and depth now enter as model inputs rather than as
  filters, so they can carry effects.
- Anisotropic (ARD) Matérn kernel, giving one length-scale per input dimension and a second,
  model-intrinsic relevance ranking independent of Random Forest.
- Temporal holdout validation: fit 2019–2022, predict the held-out 2023 season. Reports RMSE,
  MAE, bias, R², and 95% credible-interval coverage **with** interval width.
- SPEI extracted per sampling window from GRIDMET (`spei30d`, `spei90d`, `spei180d`),
  replacing the annual value used through v3.0.

**Changed**
- Forecast-year SPEI set to the observed mean (about −0.6) rather than 0.0. Zero implied
  conditions wetter than seven of the nine observed sampling windows.
- Projections described as "projection under stated assumptions" rather than "forecast",
  since leave-one-year-out R² is negative in every fold.
- Grazing comparisons reported with Holm correction within the 2023 endpoint family
  (6 tests) rather than uncorrected. Corrected p = 0.030 for NO₃⁻ and 0.036 for NH₄⁺;
  neither survives correction across all 22 cells, so the family is stated explicitly.

**Fixed**
- Feature list passed to the GPR included `year` twice, producing 11 kernel length-scales
  for 10 named features.
- Dashboard export overwrote the GEE-extracted `spei_df` with the old annual dictionary,
  and misaligned Random Forest importance values to feature names.

---

## v3.0

**Added**
- Chamber greenhouse gas flux (CO₂, N₂O, CH₄; Hutchinson–Mosier) as covariates, aggregated
  to a seasonal mean per plot, year and grazing strip.
- Permutation importance on a held-out year, alongside impurity importance.

**Changed**
- Projection horizon shortened from 2030 to 2028, matching the five-year observed record.
- Random Forest reframed as a covariate ranking tool rather than a predictive model, after
  leave-one-year-out cross-validation returned negative R² in every fold.

**Fixed**
- Flux outliers removed: two CH₄ values near −71 g ha⁻¹ d⁻¹ and five above +50, all outside
  the plausible range for upland soils. Large CO₂ values retained as real peak-season
  respiration.

---

## v2.1

**Added**
- Google Earth Engine covariates: NDVI and EVI from Sentinel-2, VV backscatter from
  Sentinel-1, extracted per plot and sampling window.
- A standardized drought index as a covariate.
- Random Forest impurity importance to rank covariates before fitting the GPR.
- Log transformation of the nitrogen target, preventing negative predictions.

---

## v2.0 — anchor model

**Added**
- Coverage audit across five years of field and laboratory records, establishing soil
  inorganic nitrogen (NH₄⁺, NO₃⁻) as the only variable with complete temporal and
  treatment-level coverage, and therefore the modelling anchor.
- Grazing as an explicit factor, after grazed and ungrazed strips were found to be
  distinct sampling units rather than replicates.

**Changed**
- Study reframed from soil carbon to soil nitrogen. Carbon fractions and FAME profiles
  were measured at higher analytical resolution but could not support a trajectory.

---

## v1.0 — experimental baseline

- NH₄⁺ and NO₃⁻ trajectories by treatment, fitted with Gaussian Process regression on year
  alone, with no covariates.
- Data assembly: five years of records standardized into one schema with unique sample
  identifiers encoding year, plot, time point, depth, grazing condition and replicate.

---

## Corrections of record

Errors that changed a reported result, rather than only the code.

**Placeholder drought values (affected v2.1–v3.0).** The SPEI dictionary used through v3.0
held invented values — 2021 at −2.10 and 2022 at +0.88 — that contradicted both the manually
retrieved index and the gridded product. Replacing them with GRIDMET extraction reversed the
narrative: 2021 was near-normal, 2022 was the driest year on record here, and the relationship
between water balance and inorganic nitrogen is inverse rather than suppressive.

**Time points misread as treatments.** "T1" and "T2" in the study's data availability table
denote Time 1 and Time 2, not Treatment 1 and Treatment 2. Carbon fractions, FAME profiles and
pH/EC in 2022–2023 therefore cover **all three treatments at a single time point**, not one
treatment. This changed their analytical role from "descriptive only" to "snapshot comparison,
not a trajectory".

**Legume nitrate values shifted by one year.** Legume strips were not sampled in 2020; the
value displayed under 2020 belonged to 2021.

**Importance bars on mismatched scales.** ARD relevance and impurity importance were plotted
against separate maxima, making SPEI's ARD bar appear nearly as long as NDVI's when it is
about 62% of it. Both now share one scale.

**Grazing's permutation rank overstated.** Reported as "last under permutation"; it ranks
9th of 11, within the group of covariates whose importance is negative.
