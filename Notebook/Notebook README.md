# Notebooks

Python exports of the Google Colab notebooks behind each model version. They are provided for
inspection rather than execution: data paths point to a directory that must be set, and Earth
Engine access requires your own registered project. Raw data is not published here (see
[`../data/README.md`](../data/README.md)).

Read them in order. Each version builds on the one before, and what changed between them, with
the reasoning, is in [`../CHANGELOG.md`](../CHANGELOG.md).

---

## Files

| File | Version | What it does |
|---|---|---|
| `v1_0_baseline.py` | v1.0 | Data assembly and the experimental baseline. Standardizes five years of records into one schema with unique sample identifiers, then fits Gaussian Process regression to soil organic carbon fractions against year alone |
| `v2_0_anchor.py` | v2.0 | Coverage audit, establishing soil inorganic nitrogen as the modelling anchor. Adds grazing as an explicit factor and extracts NDVI, EVI and SAR-VV per plot and sampling window from Google Earth Engine |
| `v2_1_covariates.py` | v2.1 | Adds a drought index, Random Forest impurity importance for covariate ranking, and a log-transformed nitrogen target. Fits one GPR per treatment × grazing × depth subset |
| `v3_0_ghg.py` | v3.0 | Adds chamber greenhouse gas flux as covariates and permutation importance alongside impurity importance. Shortens the projection horizon to 2028 |
| `v3_1_global_gpr.py` | v3.1 | Replaces the per-subset models with one global GPR using an ARD Matérn kernel, with treatment, grazing and depth as model inputs. Adds temporal holdout validation and extracts the drought index per sampling window |

`v3_1_global_gpr.py` is the current analysis. Earlier versions are kept because the reasoning
behind the final design only makes sense alongside what preceded it, including the parts that
were wrong.

---

## Before running anything

**Set the data directory.** Each script expects a `DATA_DIR` constant near the top. Point it at
a folder containing the soil nitrogen master file and the greenhouse gas flux file.

**Register an Earth Engine project.** The covariate extraction calls `ee.Initialize()` and needs
a project ID of your own. Scripts from v2.0 onward will not run without it.

**Expect them not to run end to end.** Without the raw data files the extraction and modelling
cells will fail. Every analytical step, parameter and decision is nonetheless visible in the
code, and the aggregated outputs are published in `../data/aggregated/`.

---

## Dependencies

```
scikit-learn    Random Forest, Gaussian Process regression, permutation importance
pandas, numpy   data assembly and aggregation
scipy           Mann–Whitney U tests
matplotlib      figures
earthengine-api covariate extraction
```

Developed in Google Colab, which supplies all of these except `earthengine-api`.

---

## A note on what these show

The scripts include steps that were later found to be wrong, in the versions where they occurred.
A placeholder drought value runs through v2.1 and v3.0; per-subset model fitting runs through
v3.0, which prevented treatment and grazing from carrying any effect. Both are documented in
`../CHANGELOG.md` and corrected in v3.1.

They are left in place rather than retrofitted. The point of publishing the development history
is that it is auditable, which it would not be if each version were quietly revised to match the
last.
