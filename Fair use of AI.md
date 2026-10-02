## Fair use of AI
Generative AI tools were used during this project, and this section records where.

**Organizing and summarizing research ideas.** The research questions, study design, field and
laboratory work, and interpretation of results are the authors' own. AI was used to structure
and summarize those ideas — turning working notes and decisions into ordered arguments, and
drafting summaries of material the authors supplied.

**Coding for modelling.** AI assisted in writing and debugging the analysis pipelines: data
assembly, covariate extraction, Random Forest and Gaussian Process implementations, validation
procedures, and the figures and exports built from them. All code is in this repository and can
be inspected.

**Summarizing model reports.** AI assisted in drafting the model reports, changelog and
documentation from executed analysis outputs.

**Verification.** Every reported value has been checked against the executed notebooks and the
underlying statistical outputs. Model inputs, covariate sources, test statistics and p-values
were verified independently of the text describing them. AI was used to polish and organize
model inputs and documentation, not to produce results that were accepted without checking.

One instance of this mattered: a placeholder drought value introduced during drafting
propagated through two model versions before verification against gridded data caught it. The
correction reversed part of the interpretation and is documented in
[`CHANGELOG.md`](CHANGELOG.md). It is recorded here rather than quietly fixed, because the
value of a verification process is only demonstrated when it catches something.

The authors take full responsibility for the content, analysis and conclusions presented here.
