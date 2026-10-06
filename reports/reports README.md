# Reports

Written documentation of the analysis. Start with the development summary for the whole arc, then
go to a version report for the detail.

---

## Files

| File | Covers | What it is |
|---|---|---|
| `model-development-summary.md` | v1.0 to v3.1 | How the analysis reached its current form. One section per version: the question it asked, what it settled, and what it led to. Consolidated results and the corrections that changed an interpretation |
| `model-report-v2.1.md` | v2.1 | First full report. Covariate fusion, Random Forest ranking, per-subset Gaussian Process fitting |
| `model-report-v3.0.md` | v3.0 | Adds greenhouse gas flux and permutation importance. First version to report that cross-validation could not predict an unseen year |
| `model-report-v3.1.md` | v3.1 | Current. Global GPR with ARD kernel, temporal holdout validation, per-window drought index, and the full results |

**v3.1 is the current analysis.** If you only read one, read that.

---

## Why v1.0 and v2.0 have no full report

Those versions were exploratory. v1.0 tested whether soil organic carbon fractions could carry a
trajectory model and established the data schema; v2.0 ran the coverage audit that moved the study
to soil inorganic nitrogen. Neither produced results intended to stand on their own, so neither
was written up separately.

Both are covered in `model-development-summary.md`, and the changes they introduced are recorded
in [`../CHANGELOG.md`](../CHANGELOG.md).

---

## How these relate to each other

The version reports are cumulative in method but not in conclusion. v2.1 and v3.0 describe
analyses whose findings were later revised, in some cases substantially: the drought index used
through v3.0 held placeholder values, and the per-subset model structure used through v3.0
prevented treatment and grazing from carrying any effect.

They are kept as written rather than updated. Where a reported result changed, the correction is
documented in `../CHANGELOG.md` and the current position is in the v3.1 report.

For results to cite, use **v3.1**. For understanding how the analysis developed, read in order.

---

## Related material

- Aggregated results behind the reported numbers: [`../data/`](../data/)
- Analysis code for each version: [`../notebooks/`](../notebooks/)
- References, grouped by what each work supports: [`../REFERENCES.md`](../REFERENCES.md)
