# References

Works cited in the model reports, the poster, and the analysis notebooks, grouped by what they support. The note under each entry says why it is cited here rather than summarising the paper.

---

## Covariate importance and ranking

**Breiman, L. (2001).** Random forests. *Machine Learning*, 45(1), 5–32.
[doi:10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324)
The original method, and the source of both impurity-based and permutation importance.

**Strobl, C., Boulesteix, A.-L., Zeileis, A., & Hothorn, T. (2007).** Bias in random forest variable importance measures: Illustrations, sources and a solution. *BMC Bioinformatics*, 8, 25.
[doi:10.1186/1471-2105-8-25](https://doi.org/10.1186/1471-2105-8-25)
Shows that importance measures are unreliable when predictors differ in scale of measurement or number of categories, and traces this to biased split selection within trees and to bootstrap sampling with replacement. Explains why a binary covariate such as grazing is structurally disadvantaged under impurity importance: it offers the split search a single candidate cut point where continuous covariates offer many.

**Strobl, C., Boulesteix, A.-L., Kneib, T., Augustin, T., & Zeileis, A. (2008).** Conditional variable importance for random forests. *BMC Bioinformatics*, 9, 307.
[doi:10.1186/1471-2105-9-307](https://doi.org/10.1186/1471-2105-9-307)
Extends the above to correlated predictors and proposes a conditional permutation scheme. Relevant to the NDVI, EVI and SAR-VV cluster, which measure overlapping signals.

**Nicodemus, K. K., Malley, J. D., Strobl, C., & Ziegler, A. (2010).** The behaviour of random forest permutation-based variable importance measures under predictor correlation. *BMC Bioinformatics*, 11, 110.
[doi:10.1186/1471-2105-11-110](https://doi.org/10.1186/1471-2105-11-110)

**Fisher, A., Rudin, C., & Dominici, F. (2019).** All models are wrong, but many are useful: Learning a variable's importance by studying an entire class of prediction models simultaneously. *Journal of Machine Learning Research*, 20(177), 1–81.
[jmlr.org/papers/v20/18-760.html](https://jmlr.org/papers/v20/18-760.html)
A variable important to one well-performing model may be unimportant to another. The justification for ranking covariates by more than one method rather than trusting a single ordering.

**Hooker, G., Mentch, L., & Zhou, S. (2021).** Unrestricted permutation forces extrapolation: Variable importance requires at least one more model, or there is no free variable importance. *Statistics and Computing*, 31, 82.
[doi:10.1007/s11222-021-10057-z](https://doi.org/10.1007/s11222-021-10057-z)
Permute-and-predict diagnostics can mislead under dependence among features, and a permuted feature can improve predictive performance. The mechanism behind the negative permutation value for CO₂ flux.

---

## Modelling and validation

**Rasmussen, C. E., & Williams, C. K. I. (2006).** *Gaussian Processes for Machine Learning.* MIT Press.
[gaussianprocess.org/gpml](https://gaussianprocess.org/gpml/)
Reference text for Gaussian Process regression. Chapter 2 covers regression; Chapter 5 covers model selection and the ARD kernel used for length-scale relevance.

**Neal, R. M. (1996).** *Bayesian Learning for Neural Networks.* Lecture Notes in Statistics 118. Springer.
Origin of automatic relevance determination.

**Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera-Arroita, G., et al. (2017).** Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography*, 40(8), 913–929.
[doi:10.1111/ecog.02881](https://doi.org/10.1111/ecog.02881)
Structured data invites overfitting with non-causal predictors, and blocking in time can force extrapolation by restricting the predictor ranges available for training. Supports the temporal holdout design and explains why held-out predictions flatten toward the prior mean.

**Ambroise, C., & McLachlan, G. J. (2002).** Selection bias in gene extraction on the basis of microarray gene-expression data. *PNAS*, 99(10), 6562–6566.
[doi:10.1073/pnas.102102699](https://doi.org/10.1073/pnas.102102699)
Selecting features on the full dataset before cross-validation produces severely biased error estimates. The basis for nesting feature selection inside training folds, listed in next steps.

**Mann, H. B., & Whitney, D. R. (1947).** On a test of whether one of two random variables is stochastically larger than the other. *Annals of Mathematical Statistics*, 18(1), 50–60.
[doi:10.1214/aoms/1177730491](https://doi.org/10.1214/aoms/1177730491)

**Holm, S. (1979).** A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*, 6(2), 65–70.
Used to correct the grazing comparisons within the 2023 endpoint family.

---

## Data sources

**Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., & Moore, R. (2017).** Google Earth Engine: Planetary-scale geospatial analysis for everyone. *Remote Sensing of Environment*, 202, 18–27.
[doi:10.1016/j.rse.2017.06.031](https://doi.org/10.1016/j.rse.2017.06.031)

**Huete, A., Didan, K., Miura, T., Rodriguez, E. P., Gao, X., & Ferreira, L. G. (2002).** Overview of the radiometric and biophysical performance of the MODIS vegetation indices. *Remote Sensing of Environment*, 83(1–2), 195–213.
[doi:10.1016/S0034-4257(02)00096-2](https://doi.org/10.1016/S0034-4257(02)00096-2)
Source of the EVI formulation.

**Vicente-Serrano, S. M., Beguería, S., & López-Moreno, J. I. (2010).** A multiscalar drought index sensitive to global warming: The standardized precipitation evapotranspiration index. *Journal of Climate*, 23(7), 1696–1718.
[doi:10.1175/2009JCLI2909.1](https://doi.org/10.1175/2009JCLI2909.1)

**Abatzoglou, J. T. (2013).** Development of gridded surface meteorological data for ecological applications and modelling. *International Journal of Climatology*, 33(1), 121–131.
[doi:10.1002/joc.3413](https://doi.org/10.1002/joc.3413)
Source of the GRIDMET drought product. Its documentation notes that the dataset will not capture microclimates finer than its roughly 4 km grid — the limitation behind nine plots sharing one water-balance pixel.

---

## Agronomic context

**Lucero, M., Adee, E., Ruiz Diaz, D., Sullivan, T., Jha, G., Simon, L., & Joshi, D. R. (2026).** Machine learning insights into long-term soil fertility legacy and seasonal weather effects in corn–soybean rotation. *Soil Science Society of America Journal*, 90, e70334.
[doi:10.1002/saj2.70334](https://doi.org/10.1002/saj2.70334)
Methodological template for applying Random Forest to a long-term fertility trial, and the source of the plot-grouped cross-validation discussed as an alternative to the year-grouped folds used here.

**Blanco-Canqui, H., Shaver, T. M., Lindquist, J. L., Shapiro, C. A., Elmore, R. W., Francis, C. A., & Hergert, G. W. (2015).** Cover crops and ecosystem services: Insights from studies in temperate soils. *Agronomy Journal*, 107, 2449–2474.
[doi:10.2134/agronj15.0086](https://doi.org/10.2134/agronj15.0086)

**Santos, E. R. S., et al. (2023).** Integrated crop-livestock systems result in less nitrate leaching than ungrazed crop systems in North Florida. *Journal of Environmental Quality*.
[doi:10.1002/jeq2.20474](https://doi.org/10.1002/jeq2.20474)
Found lower cumulative nitrate leaching under grazed than ungrazed systems. *Full author list to be confirmed before formal citation.*

**Grazing of cover crops improves soil nitrogen dynamics in organic vegetable systems with minimal soil health tradeoffs (2026).** *Frontiers in Soil Science*.
[doi:10.3389/fsoil.2026.1825405](https://doi.org/10.3389/fsoil.2026.1825405)
Reports grazing increasing soil nitrogen across dissolved organic, inorganic and microbial pools — the opposite direction to the unfertilized result here, supporting the view that grazing's effect depends on the system's nitrogen inputs. *Authors to be confirmed before formal citation.*

---

## Notes on use

Entries marked for confirmation have been verified by title, journal and DOI but not by full author list. Confirm these against the publisher record before citing them in a manuscript.

Software: analyses used `scikit-learn` for Random Forest and Gaussian Process regression, `scipy` for the Mann–Whitney tests, and the Earth Engine Python API for covariate extraction. Cite the corresponding software papers if the methods section requires it.
