# Decision models: source summaries

The selected Zotero **Decision Models** collection contains sixteen research papers
and seven web-only releases/model cards. The current evidence concerns fast,
schema-conditioned probabilistic decisions. It does not constitute a general
survey of decision theory or optimization. Read [the synthesis](SYNTHESIS.md) for
comparisons, and [the implementation guide](REPOSITORIES.md) for source maps.

Dates below describe the PDF version filed. Publication dates remain separately
recorded in [the provenance manifest](papers/manifest.json); multiple October
versions are ordered by their confirmed day. All sixteen are arXiv preprints: no
peer-reviewed venue is confirmed in the curated records. Source-specific numbers
are reported results, not measurements rerun by this library. Citation keys come
from Zotero and remain unchanged.

## Overview table

| Date | Authors | Title | One-line contribution | PDF |
|---|---|---|---|---|
| 2026-09 | Li et al. | Beyond Calibration: Do a Typed-Decision Model's Probabilities Obey the Probability Axioms? | Label-free logical checks expose inconsistency between negation, disjunction, yes/no and categorical probabilities. | [pdf](papers/2026/09_Li_et_al._Beyond_Calibration_Do_a_Typed_Decision_Models_Probabilities_Obey_the_Probability_Axioms.pdf) |
| 2026-09 | Deußer et al. | Evaluating and Benchmarking the System One Model Jev | A broad, reproducible evaluation separates choice calibration, binary thresholds and rubric scoring. | [pdf](papers/2026/09_Deusser_et_al._Evaluating_and_Benchmarking_the_System_One_Model_Jev.pdf) |
| 2026-09 | Zhang et al. | AnyJev Technical Report | Frozen-LLM readouts separate label-prior correction, option-order averaging, calibration and adaptive rotation cost. | [pdf](papers/2026/09_Zhang_et_al._AnyJev_Technical_Report.pdf) |
| 2026-10 | Cao et al. | SearchJev: A Fast and Calibrated System-1 Model for Search Agents | Task-specific decision training within a hybrid controller improves a small search-agent evaluation. | [pdf](papers/2026/10_Cao_et_al._SearchJev_A_Fast_and_Calibrated_System_1_Model_for_Search_Agents.pdf) |
| 2026-10 | Rafe and Das | Benchmarking System One decision models against trained classifiers and language models for automated decision gates | Matched decision gates compare specialist models, trained classifiers and LLM readouts under calibration, rejection and cascade costs. | [pdf](papers/2026/10_Rafe_and_Das_Benchmarking_System_One_decision_models_against_trained_classifiers_and_language_models_for_automated_decision_gates.pdf) |
| 2026-10 | Xu et al. | JevOut: Natural Context Can Flip Decision Models | Answer-preserving context changes expose confident decision errors under an explicit search budget. | [pdf](papers/2026/10_Xu_et_al._JevOut_Natural_Context_Can_Flip_Decision_Models.pdf) |
| 2026-10 | Li et al. | JEV-as-a-Judge: Accept When Confident, Escalate When Unsure | Frozen and prospective judge cascades quantify when confidence can save cost without losing accuracy. | [pdf](papers/2026/10_Li_et_al._JEV_as_a_Judge_Accept_When_Confident_Escalate_When_Unsure.pdf) |
| 2026-10 | Sharma et al. | TypedBench: A Benchmark for Calibration, Framing Sensitivity, and Cost in System One Decision Models | Policy-generated tasks evaluate wording robustness, calibration noise floors and decisions under asymmetric costs. | [pdf](papers/2026/10_Sharma_et_al._TypedBench_A_Benchmark_for_Calibration_Framing_Sensitivity_and_Cost_in_System_One_Decision_Models.pdf) |
| 2026-10 | Duan et al. | General Decision Models: Benchmarking and Insights Beyond Jev | A broad benchmark, analytic probability probes and agent tests separate local speed from system reliability. | [pdf](papers/2026/10_Duan_et_al._General_Decision_Models_Benchmarking_and_Insights_Beyond_Jev.pdf) |
| 2026-10 | Zhuang et al. | StartLux-Decision: AutoThink Decision Models with Reinforcement Learning for Calibrated Deliberative Decisions | Instant and AutoThink models combine bidirectional readout, selective reasoning and decision-weighted probability rewards. | [pdf](papers/2026/10_Zhuang_et_al._StartLux_Decision_AutoThink_Decision_Models_with_Reinforcement_Learning_for_Calibrated_Deliberative_Decisions.pdf) |
| 2026-10 | Geuter et al. | Releasing the Inner Jev: A Simple Recipe for Open Decision Models | Answer-letter readout and short LoRA training yield competitive open decisions on OpenDecisions and JevBench. | [pdf](papers/2026/10_Geuter_et_al._Releasing_the_Inner_Jev_A_Simple_Recipe_for_Open_Decision_Models.pdf) |
| 2026-10 | Li and Wagle | LLM-as-Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them | Prefix-free candidate scoring tests when frozen LLMs suffice and when anchored fine-tuning or bounded reasoning helps. | [pdf](papers/2026/10_Li_and_Wagle_LLM_as_Jev_LLMs_Are_Already_Jev_Style_Decision_Models_When_and_How_to_Fine_Tune_Them.pdf) |
| 2026-10 | Imperatrice et al. | Are AI Decision Models Biased? A Case Study of Jev | Behavioral tasks distinguish selected answers from probability shifts under irrelevant context, framing and option order. | [pdf](papers/2026/10_Imperatrice_et_al._Are_AI_Decision_Models_Biased_A_Case_Study_of_Jev.pdf) |
| 2026-10 | Zhang et al. | Typed Decision Models on Tabular Data | Four decision models and three LLMs separate option-format robustness from table-serialization robustness. | [pdf](papers/2026/10_Zhang_et_al._Typed_Decision_Models_on_Tabular_Data.pdf) |
| 2026-10 | Zhu et al. | Intern-Decision: Efficient Multimodal Decision Making with Autoregressive Masked Language Modeling | Multimodal masked decision training scores multiple fields in one causal pass, with separate calibration and handoff evaluations. | [pdf](papers/2026/10_Zhu_et_al._Intern_Decision_Efficient_Multimodal_Decision_Making_with_Autoregressive_Masked_Language_Modeling.pdf) |
| 2026-10 | Chen et al. | System1-Arena: Which Decisions Can Be Left to System 1? | Shared probability-scoring requests separate strong static decisions from weak closed-loop control across 30 models. | [pdf](papers/2026/10_Chen_et_al._System1_Arena_Which_Decisions_Can_Be_Left_to_System_1.pdf) |

<a id="beyond-calibration-do-a-typed-decision-model-s-probabilities-obey-the-probability-axioms"></a>

## 2026-09 — Li et al. — Beyond Calibration: Do a Typed-Decision Model's Probabilities Obey the Probability Axioms?

**Venue / provenance:** arXiv preprint `2609.33209v1`; filed PDF version dated 2026-09-27. Zotero publication date: 2026-09-27. DOI: [10.48550/arXiv.2609.33209](https://doi.org/10.48550/arXiv.2609.33209). [PDF](papers/2026/09_Li_et_al._Beyond_Calibration_Do_a_Typed_Decision_Models_Probabilities_Obey_the_Probability_Axioms.pdf) · [generated text](papers/text/2026/09_Li_et_al._Beyond_Calibration_Do_a_Typed_Decision_Models_Probabilities_Obey_the_Probability_Axioms.txt).

**Zotero citation key:** `2026.LI.calibrationtypeddecisionmodelsprobabilitiesobeyprobabilityaxioms`

**Where it fits.** Li, He and Li (2026), *Beyond Calibration: Do a Typed-Decision Model's Probabilities Obey the Probability Axioms?*, distinguish calibration across examples from coherence across logically related questions about one example. A well-ranked confidence score is not automatically a consistent joint belief.

**What it contains.** For 100 ChaosNLI and 60 PubMedQA items with three mutually exclusive, exhaustive labels, the study asks whether each label applies, whether it does not apply, whether either alternative applies, and which label applies. Definitions are held fixed, and these identities require no gold labels. Design choices (renaming PubMedQA's yes/no/maybe answers, cycling option order through all permutations) avoid confusing wordings. The comparison controls are a measured repeat-noise floor, confidence-matched pairs, the readout (first-token versus verbalized) and removal of double-negation labels; a bundling check compares single and joint requests.

Across 480 negation pairs, mean absolute complementarity violation is 0.064 for Jev, 0.293 for Qwen3.8-27B first-token probabilities and 0.122 for its verbalized probabilities. The gap to the first-token readout survives every control (Table 2). Jev is not coherent either: its violation is about five times its repeat-noise floor of 0.013, and its three single-label yes/no probabilities sum to about 1.14 on average. The systems fail differently: Qwen's first-token readout rejects both a statement and its negation in 196 of 480 pairs and does not become more coherent when confident, whereas Jev's violations shrink from 0.142 on uncertain pairs to 0.018 on its most confident ones (Figure 3).

**Strengths.** Explicit partitions make the logical requirements clear; matched questions and the controls separate repeat noise, confidence, readout and double negation. The label-free checks expose cross-form biases and within-item inconsistencies that accuracy and per-form calibration metrics cannot detect.

**Limitations.** The sample contains two English domains, one main wording per relation, one Jev version and one comparison backbone with thinking disabled. Coherence is necessary for combining probability statements but not sufficient for informativeness or accuracy: constant prior probabilities can pass.

**Evidence locations.** §§3–7; Eqs. 1 and 3; Figures 1 and 3; Tables 1–2. The arXiv banner dates v1 to 27 September; the typeset title page says 29 September. The manifest follows the version banner. The [author supplement](https://github.com/bro789/typed-decision-coherence) is linked for reproduction but is not selected as a substantial maintained implementation snapshot.

<a id="deusser-benchmark"></a>

## 2026-09 — Deußer et al. — Evaluating and Benchmarking the System One Model Jev

**Venue / provenance:** arXiv preprint `2609.37647v1`; attached PDF dated 2026-09-29. Zotero publication date: 2026-09-29. DOI: [10.48550/arXiv.2609.37647](https://doi.org/10.48550/arXiv.2609.37647). [PDF](papers/2026/09_Deusser_et_al._Evaluating_and_Benchmarking_the_System_One_Model_Jev.pdf) · [generated text](papers/text/2026/09_Deusser_et_al._Evaluating_and_Benchmarking_the_System_One_Model_Jev.txt).

**Zotero citation key:** `2026.DEUSSER.evaluatingbenchmarkingsystemonemodeljev`

**Where it fits.** Deußer, Sparrenberg and Sifa (2026), *Evaluating and Benchmarking the System One Model Jev*, establish a broad empirical baseline for a hosted typed-decision service. The central contribution is measurement across interfaces and tasks, rather than a new architecture or a proof that bounded outputs are reliable.

**What it contains.** Sections 3–4 evaluate Jev 1.13.0 on 37 datasets using 346,009 answered requests, one frozen template per dataset and no in-context examples. Templates were piloted on 20 training/validation examples. The open-weight controls use the same requests and exact next-token probabilities restricted to valid option codes, with thinking disabled. This is a stronger control for the decision interface than asking a baseline to generate JSON and verbalize confidence. Table 3 reports Jev ahead of Qwen3.8-27B on 27 datasets, behind on nine and tied on one; eleven Jev leads have non-overlapping bootstrap intervals, whereas none of Qwen's leads do. Jev exceeds Gemma-4-E4B on all 37 datasets.

Choice calibration pools 279,925 answers over 22 datasets: ECE is 0.028, but the mean per-dataset ECE is 0.061 and some difficult datasets are much worse (Figure 2; Appendix Table 8). The binary interfaces err in opposite directions: single-question yes/no probabilities are slightly under-confident (mean P(yes) 0.465 against a 0.518 base rate), which explains recall deficits despite high AUROC, while multi-label fan-out over-predicts positives. Table 4 shows that thresholds selected on separate training/validation data raise UNFAIR-ToS micro-F1 from 0.499 to 0.748. Rubric scoring is the one area where Qwen matches or slightly beats Jev, with higher correlation on 9 of 12 dimensions. The whole study, 346,009 requests, cost under US$10 (US$9.40 including pilot and extra analyses; Table 7). The paper releases a content-addressed harness and raw responses, with a Zenodo DOI, enabling analysis without repeat API calls.

**Strengths.** Full evaluation splits, explicit task/primitive mappings, frozen prompts, uncertainty intervals and matched probability readouts make the results auditable. The paper tests calibration, selective prediction, threshold transfer, multilingual performance and contamination explanations instead of relying on average accuracy alone. It reports both useful confidence rankings and interface-specific probability failures.

**Limitations.** The authors note one untuned template per dataset, baselines scored without reasoning, and no measurement of run-to-run variance (§5). The closed model's architecture and training data remain unknown; option-rotation and question-removal probes cannot detect memorized question–answer pairs, so the unusually strong MMLU mathematics result remains unexplained. Pooled ECE is dominated by large datasets. Prices, latency and behavior describe jev-1.13.0, not later aliases.

**Evidence locations.** §§3.2–3.7, Tables 1–4 and 7, Figures 2–4, §§4.4–4.6, §5 and Appendix Table 8. See [official code source maps](REPOSITORIES.md).

<a id="anyjev-technical-report"></a>

## 2026-09 — Zhang et al. — AnyJev Technical Report

**Venue / provenance:** arXiv preprint `2610.00831v1`; filed PDF version dated 2026-09-30. Zotero publication date: 2026-09-30. DOI: [10.48550/arXiv.2610.00831](https://doi.org/10.48550/arXiv.2610.00831). [PDF](papers/2026/09_Zhang_et_al._AnyJev_Technical_Report.pdf) · [generated text](papers/text/2026/09_Zhang_et_al._AnyJev_Technical_Report.txt).

**Zotero citation key:** `2026.ZHANG.anyjevtechnicalreport`

**Where it fits.** Zhang et al. (2026), *AnyJev Technical Report*, ask how much decision capability can be obtained from unchanged open LLMs by improving the readout. The contribution is an inference procedure and cost analysis rather than a newly pretrained decision backbone.

**What it contains.** L0 restricts next-token probabilities to legal option-label tokens, divides out a label prior and averages cyclic option rotations in log space (Eqs. 2–3). The prior is estimated by batch calibration, a running mean of the model's own outputs over already-scored inputs, without gold labels; a content-free-probe estimator exists in the code but is explicitly not used (§4.1). The prior strength α = 0.75 is chosen once, globally, from a separate sweep over 230 model–question pairs scored against gold labels. An answer-mass gate detects cases where the requested labels capture too little model probability. Temperature calibration is a separate fitted step. An adaptive rule reads well-spaced rotations and stops when a log-margin threshold is met; its target is agreement with the model's full-rotation answer, not correctness against ground truth.

On two 20-option tasks, rotations improve accuracy for all eleven tested models and lower order-flip rates from about 0.33 to 0.138 and 0.183. Calibration improvements mainly come from temperature fitting, not rotations alone. On the JevBench public subset (213 of 231 items, 2–6 options), debiasing has no measurable accuracy effect: +0.006 [−0.004, 0.018] pooled over 1,704 decisions. The headline efficiency result is Table 3: on an 18-option question on one H100, the adaptive budget reads 7.3 of 18 rotations, serves 2.22× as many decisions per second on vLLM and returns the full-rotation decision 98.7% of the time. Additional full-split evaluation shows that the label-prior correction is task-dependent.

**Strengths.** Matched unchanged weights isolate readout effects. Negative results for shared heads, cache reuse and option masking are documented. The report names both places labels enter (α and temperature), distinguishes one prefill per rotation from one prefill for the entire decision and separates probability calibration from debiasing.

**Limitations.** Eighteen public benchmark items are excluded, and timing and accuracy use different workloads. The 7.3-rotation serving run selects and bounds its threshold on the same states; the disjoint selection/verification analysis that supports a reliable bound reads 10.6 rotations instead (§5). No general accuracy or regret guarantee is offered.

**Evidence locations.** §§4–10; Eqs. 2–3; Tables 1–3 and 10–11; Appendix E. See [AnyJev source map](REPOSITORIES.md#anyjevtxt).

<a id="searchjev"></a>

## 2026-10 — Cao et al. — SearchJev: A Fast and Calibrated System-1 Model for Search Agents

**Venue / provenance:** arXiv preprint `2610.05107v1`; attached PDF dated 2026-10-04. Zotero publication date: 2026-10-04. DOI: [10.48550/arXiv.2610.05107](https://doi.org/10.48550/arXiv.2610.05107). [PDF](papers/2026/10_Cao_et_al._SearchJev_A_Fast_and_Calibrated_System_1_Model_for_Search_Agents.pdf) · [generated text](papers/text/2026/10_Cao_et_al._SearchJev_A_Fast_and_Calibrated_System_1_Model_for_Search_Agents.txt).

**Zotero citation key:** `2026.CAO.searchjevfastcalibratedsystem1modelsearchagents`

**Where it fits.** Cao et al. (2026), *SearchJev: A Fast and Calibrated System-1 Model for Search Agents*, turn the decision interface into a search-specific trained component. A larger model retains planning, query generation and answer composition; the decision model handles bounded judgments and delegates uncertain ones. This is a hybrid controller, not an autonomous optimal-policy learner.

**What it contains.** SearchDecision-Bench covers routing, rewriting, relevance, sufficiency, navigation and verification with categorical, ordinal and binary outputs (Tables 1–2). A Qwen3.5 backbone scores single-token option labels through its existing LM head and normalizes only over valid labels (Eq. 1). SLCD combines source-weighted soft-target cross-entropy and Brier loss (Eq. 2); separate held-out temperature calibration is fitted by output type (Eq. 3). A confidence threshold selects which judgments go to System 2. Dataset identity/query checks remove overlapping examples and synthetic variants derived from evaluation sources.

Both sizes are LoRA-trained. The abstract's headline is 5.2–5.3× faster decisions than same-size autoregressive JSON baselines with 41–74% lower mean ECE; Table 3 shows 27.6/37.1 ms median decision latency for the 0.8B/4B variants versus 144.2/195.2 ms. SearchJev-4B does not dominate Jev 1.13 on every task: Jev leads navigation (72.1 versus 57.2) and retains the lowest mean ECE. The end-to-end experiment samples 100 BrowseComp-Plus questions, runs each agent once, fixes System 2 at Qwen3.5-27B and uses BM25 retrieval. Table 4 reports 45% answer accuracy and 4,080 s median active time for System 2 alone, and 46.0% and 1,018 s for a hybrid using Jev 1.13 as System 1. The 4B hybrid reaches 54% at 1,102 s, eight points above the Jev hybrid; the 0.8B hybrid ties Jev at 46% while being faster (868 s) with fewer System-2 calls. Active time includes retrieval and model calls. OOD evaluation covers four decision families; verification accuracy and calibration transfer remain uneven (Table 5).

**Strengths.** It connects a concrete probability-learning objective to an operational routing rule and measures final answer quality alongside local accuracy, calls, output tokens and time. Keeping the larger reasoner fixed and including a Jev hybrid makes the system comparison interpretable. It exposes both task-level and held-out-dataset results rather than treating calibration as universal.

**Limitations.** A single run on 100 search questions supports a limited deployment claim. Table 8 (Appendix E.2, Agent Resource Diagnostics) records zero explicit System-2 short-decision calls in both SearchJev runs, and the aggregate logs cannot recover the gate threshold (Appendix D.3); this neither proves the gate was disabled nor isolates a benefit from uncertainty delegation. Task-specific training and the change from JSON decoding to direct readout occur together, so baseline gains do not isolate either. Calibration deteriorates on some held-out families, and no OOD sufficiency/navigation tests are provided. The authors note that LLMs help label about a third of training rows and that evaluation covers only Chinese and English (Appendix H).

**Evidence locations.** Abstract; §§2.2, 3.1–3.3, 4.4 and 5.1–5.3; Eqs. 1–3; Tables 2–5; Appendices D.3, E.2 (Table 8) and H. See [official code source maps](REPOSITORIES.md).

<a id="benchmarking-system-one-decision-models-against-trained-classifiers-and-language-models-for-automated-decision-gates"></a>

## 2026-10 — Rafe and Das — Benchmarking System One decision models against trained classifiers and language models for automated decision gates

**Venue / provenance:** arXiv preprint `2610.00346v2`; filed PDF version dated 2026-10-06. Zotero publication date: 2026-09-29. DOI: [10.48550/arXiv.2610.00346](https://doi.org/10.48550/arXiv.2610.00346). [PDF](papers/2026/10_Rafe_and_Das_Benchmarking_System_One_decision_models_against_trained_classifiers_and_language_models_for_automated_decision_gates.pdf) · [generated text](papers/text/2026/10_Rafe_and_Das_Benchmarking_System_One_decision_models_against_trained_classifiers_and_language_models_for_automated_decision_gates.txt).

**Zotero citation key:** `2026.RAFE.benchmarkingsystemonedecisionmodelstrainedclassifierslanguagemodelsautomateddecisiongates`

**Where it fits.** Rafe and Das (2026), *Benchmarking System One decision models against trained classifiers and language models for automated decision gates*, connect model evaluation to a program that accepts, rejects or escalates a bounded choice. They also test whether a conventional classifier is preferable when stable labels and training data are available.

**What it contains.** One harness sends the same requests to eight checkpoints from six decision-model families (Jev, Laya, Kev, decider-2b, this-that-model-1.0 and Nimble-9B) and to generative comparators (Gemma-4-31B, Qwen3.6-27B, Qwen3-14B and Mistral-Small-24B). The generative models are read out three ways: stated (verbal) probabilities in a JSON reply, option-key likelihoods, and, for Qwen3.6-27B, a thinking mode. Trained classifiers (DeBERTa-v3-large, BERT-base, BGE-small embeddings) and a zero-shot NLI classifier complete the field. Four research questions cover accuracy with and without task labels (RQ1), calibration transfer and guaranteed-risk selective prediction (RQ2), sensitivity to option count, naming and rendering (RQ3), and accuracy–cost cascades (RQ4).

With task labels, fine-tuned DeBERTa-v3-large has the highest observed accuracy on every labelled task except the power task (Table 5). Without labels, no decision model is significantly more accurate than Jev on workflows or intents, while Gemma-4-31B matches it on typed decisions and beats it on CLINC-150 at higher cost and latency. Swapping yes and no flips 50.5 answers per hundred for Jev and at least 16.8 for every generative model, against at most 6.5 for four fine-tuned decision checkpoints. In the CLINC-150 gate, an empirical in-scope threshold lets Jev route 0.92 of in-scope requests at risk 0.047 but still accept 0.310 of out-of-scope inputs; an explicit out-of-scope option cuts that to 0.195 while routing 0.925 in scope. A Learn-then-Test guarantee of 5% risk leaves Jev only 0.528 coverage. An intent-trained first stage escalating to Gemma-4-31B reaches Gemma's accuracy at about Jev's price.

**Strengths.** The paper separates calibration as shipped from recalibration, probability elicitation from model identity, and in-scope risk from out-of-scope handling. It states the stronger assumptions behind certified thresholds and compares against supervised baselines rather than only generative models. It traces the largest open-checkpoint lead to training-data exposure.

**Limitations.** Trained classifiers receive labelled task data that zero-shot competitors do not; this is a deployment choice rather than a supervision-matched architecture test. Format failures affect verbal readouts. Cascade latency is composed offline from measured stage latencies under a stated utilization, not a live end-to-end run.

**Evidence locations.** Abstract; §§3–7; Tables 5 and 11; Appendix A; Appendix C (Table C.8). The filed v2 is dated 6 October, while Zotero retains the original 29 September publication date.

<a id="jevout"></a>

## 2026-10 — Xu et al. — JevOut: Natural Context Can Flip Decision Models

**Venue / provenance:** arXiv preprint `2609.30243v2`; attached PDF dated 2026-10-08. Zotero publication date: 2026-09-24. DOI: [10.48550/arXiv.2609.30243](https://doi.org/10.48550/arXiv.2609.30243). [PDF](papers/2026/10_Xu_et_al._JevOut_Natural_Context_Can_Flip_Decision_Models.pdf) · [generated text](papers/text/2026/10_Xu_et_al._JevOut_Natural_Context_Can_Flip_Decision_Models.txt).

**Zotero citation key:** `2026.XU.jevoutnaturalcontextcanflipdecisionmodels`

**Where it fits.** Xu et al. (2026), *JevOut: Natural Context Can Flip Decision Models*, test whether constrained outputs remain reliable when surrounding language changes without changing the correct answer. The study examines the input side of decision reliability, complementing calibration and interface checks.

**What it contains.** The evaluation retains each target model's initially correct items, fixes its most probable wrong option as the target, and permits natural context additions while preserving the original question, options and their order. A proposer and a separate semantic checker generate and accept candidates. Probability-guided allocation uses the target's margin over its strongest competitor; the budget is at most 64 accepted target evaluations per decision (Eqs. 1–4; §3). The seven datasets span knowledge, reasoning, legal cases, multi-answer selection and recorded tool-routing checkpoints. Development and held-out source items are disjoint.

Table 1 reports targeted flip rates of 61.4% for Jev (508 initially correct decisions), 72.6% for OpenSourceJev (328), 73.2% for Von (328) and 64.9% for a plain Qwen scorer (285). These are search success rates conditional on initial correctness, not ordinary test error rates or comparable populations across models. On initially confident Jev decisions (gold probability ≥ 0.9, n = 290), 45.5% can still be flipped under the same budget (Table 2). The phenomenon does not depend on the optimizer: repeated independent target-aware generation already reaches 48.0% on the same 508 Jev decisions, and full optimization adds 13.4 points. Three blinded annotators assess 250 sampled successful contexts: 91.6% meet all validity criteria by majority judgment. Matched controls show that probability-based allocation improves flip discovery over label-only allocation; frozen contexts also transfer across systems (§§4.4–4.5). Proposers fine-tuned on optimization trajectories raise one-generation flip rates on held-out Jev items from 16.1% to 18.7% (V1) and 21.9% (V2), and best-of-four from 29.1% to 34.3% (§4.6; Table 4).

**Strengths.** The fixed wrong target, retained failure denominator, matched-budget controls, human validity audit and transfer experiments make the robustness claim precise. It distinguishes harmless-looking additions from explicit answer commands and measures resulting confidence, not merely label changes. A plain next-token scorer provides a useful interface control.

**Limitations.** The search has the gold answer and chosen wrong target and excludes rejected proposals from its accepted-target-call budget; its full computational cost exceeds 64 simple calls. The human result validates sampled successes rather than every generated context. Different initial-correctness populations prevent a simple robustness leaderboard. Tasks are English only, and tool routing is evaluated at recorded checkpoints. Flip rates are conditional search successes, not the failure rate of natural production inputs.

**Evidence locations.** §§3–4 (including §4.6) and Limitations; Tables 1–4; Figures 4–5; Appendices B–D and G–J. See [official code source maps](REPOSITORIES.md).

<a id="jev-judge"></a>

## 2026-10 — Li et al. — JEV-as-a-Judge: Accept When Confident, Escalate When Unsure

**Venue / provenance:** arXiv preprint `2609.26550v5`; attached PDF dated 2026-10-09. Zotero publication date: 2026-09-22. DOI: [10.48550/arXiv.2609.26550](https://doi.org/10.48550/arXiv.2609.26550). [PDF](papers/2026/10_Li_et_al._JEV_as_a_Judge_Accept_When_Confident_Escalate_When_Unsure.pdf) · [generated text](papers/text/2026/10_Li_et_al._JEV_as_a_Judge_Accept_When_Confident_Escalate_When_Unsure.txt).

**Zotero citation key:** `2026.LI.jevasajudgeacceptwhenconfidentescalatewhenunsure`

**Where it fits.** Li et al. (2026), *JEV-as-a-Judge: Accept When Confident, Escalate When Unsure*, study a concrete accept-or-escalate decision. Jev supplies a verdict and probabilities; an expensive judge resolves low-confidence cases. The contribution is an empirical operating envelope and threshold-validation procedure, rather than a novel routing algorithm.

**What it contains.** The base study contains 5,172 judgments, with public preference/factuality tasks, answer-adjudication controls, reverse-order tests and follow-ups on style and prose. Sixteen other judges include generative and reward models. Generative judges share the verdict-and-probability output contract, with no emitted rationale; the study separately records reasoning settings. For human adjudication, one team member, blind to labels and judge outputs, adjudicated all 163 items in a 990-item subset that Jev or GPT-6 gets wrong under the supplied labels, plus 20 controls (183 adjudications). It distinguishes a 642-item pilot, held-out evaluation and exploratory follow-ups (§§3–4).

As a standalone judge, Jev comes within three points of GPT-6 wherever the verdict can be read off the text, at 0.36% of its fee and a 0.15 s median latency. It trails by 7–28 points where the verdict must be derived (expert knowledge, code, math and logic puzzles), and its confidence marks this boundary (abstract; §§5–6).

For the frozen two-order cascade (§8), aligned probabilities from both candidate orders are averaged; τ = 0.9 is chosen by the point rule (mean paired loss within two points) on 96 pilot selection pairs and fixed before held-out evaluation. Table 4 reports 93.4% accuracy versus GPT-6's 92.5% on 1,610 held-out preference pairs, with 31.5% escalated and 41.4% of the fallback's fee. The pool is 83% RewardBench: JudgeBench needs substantially more escalation and has less cost saving. These rows are offline reconstructions from retained outputs; a 510-pair live replication measures actual cascade latency. §9 then prospectively selects a threshold per new workload on 100 local labels with the stricter lower-confidence-bound rule and runs 570 held-out pairs live: accuracy matches the fallback exactly at 90.2%, with 74.2% escalation and 75.5% of its fee (Table 5). Both rules minimize cost under an accuracy tolerance rather than a calibrated economic utility.

**Strengths.** The paper distinguishes threshold exploration, frozen selection, live replication and prospective workload testing. It includes source-cluster uncertainty intervals, a matched-spend random-routing control, human adjudication and explicit failure cases. The cost accounting includes both first-stage orders and escalation; stronger uncertainty control costs more and is visible in the results.

**Limitations.** Confidence routing is weaker on style-adversarial comparisons and reference-free prose. Thresholds are workload- and fallback-dependent, and the favorable held-out mixture's savings shrink on the harder prospective workloads. The two-order protocol doubles first-stage judgments. The authors note that the comparison is not compute-matched, that Jev 1.13.0 is a black-box version whose training data cannot be checked for benchmark exposure, and that a decision-only judge gives no explanation a user could audit.

**Evidence locations.** Abstract; §§3–9 and Limitations; Eq. 1; Tables 3–5; Figure 8; Appendices N–Q. Rechecked 2026-10-20: the [author project repository](https://github.com/yubol-bobo/jev-as-a-judge) supplies a website, manuscript and figures, but no experimental reproduction code. The paper's supplementary package remains unverified as a public download; see [implementation coverage boundaries](REPOSITORIES.md#coverage-boundaries).

<a id="typedbench-a-benchmark-for-calibration-framing-sensitivity-and-cost-in-system-one-decision-models"></a>

## 2026-10 — Sharma et al. — TypedBench: A Benchmark for Calibration, Framing Sensitivity, and Cost in System One Decision Models

**Venue / provenance:** arXiv preprint `2610.11392v2`; filed PDF version dated 2026-10-09. Zotero publication date: 2026-10-08. DOI: [10.48550/arXiv.2610.11392](https://doi.org/10.48550/arXiv.2610.11392). [PDF](papers/2026/10_Sharma_et_al._TypedBench_A_Benchmark_for_Calibration_Framing_Sensitivity_and_Cost_in_System_One_Decision_Models.pdf) · [generated text](papers/text/2026/10_Sharma_et_al._TypedBench_A_Benchmark_for_Calibration_Framing_Sensitivity_and_Cost_in_System_One_Decision_Models.txt).

**Zotero citation key:** `2026.SHARMA.typedbenchbenchmarkcalibrationframingsensitivitycostsystemonedecisionmodels`

**Where it fits.** Sharma et al. (2026), *TypedBench: A Benchmark for Calibration, Framing Sensitivity, and Cost in System One Decision Models*, evaluate whether probabilities are useful when software actually acts on them. The benchmark complements evaluations of public classification datasets with explicit policies whose labels can be derived from generated inputs.

**What it contains.** Seven generators cover support tickets, phishing, retrieval relevance, log triage, policy compliance, guardrail intent and multilingual tickets. Nine suites vary wording, criteria, option order/count, input length, noise, missing information and question bundling; they also measure ordinal consistency, selective prediction, asymmetric cost and cascades. Calibration is compared with a null ECE: the expected ECE of a perfectly calibrated predictor with the same confidences, obtained by resampling labels. Because finite samples always yield some ECE, only the ratio ECE/null above one indicates excess miscalibration.

The evaluation includes Jev, two Laya encoder checkpoints and three Kev decoder sizes, alongside conventional and restricted-answer LLM baselines. Restating the same ticket-priority policy moves Jev accuracy by 24 percentage points, yet Jev remains the most accurate on that rule-applying question, where both encoders barely beat the majority baseline (0.34–0.38 against 0.34). Almost every model and question exceeds its null ECE; Jev is systematically under-confident (all its temperature refits are below 1), while the encoder is mostly over-confident, but Jev's confidence still ranks its own errors best (lowest or tied-lowest AURC). Under asymmetric costs, acting on the probabilities of the two most accurate models (Jev and Kev-9B) costs more than acting on their top answer: on ticket priority, 2,300 versus 1,080 per 10⁴ decisions for Jev (Table 4). This holds on all four cost questions and at every asymmetric ratio from 1.5:1; weaker models instead save cost. On out-of-scope items with a "none of the above" option, Jev abstains only about half the time, whereas decoders almost always do.

**Strengths.** Paired perturbations, explicit rule-based labels, independent generator seeds for supervised baselines, per-question diagnostics and cost-sensitive outcomes separate several failure modes hidden by a pooled benchmark score.

**Limitations.** Templated, rule-generated inputs trade naturalness for controllable labels; fresh examples do not eliminate familiarity with their task families. Much of the detailed stress evaluation uses tickets and phishing, while additional generators receive canonical wording only. The results concern the tested checkpoints and hardware. No author-verified TypedBench implementation snapshot was identified; a cited earlier calibration repository is not treated as its official code.

**Evidence locations.** §§3–7; Tables 1 and 4; Figures 2–3; Appendices A, B, D, H and J.

<a id="general-decision-models"></a>

## 2026-10 — Duan et al. — General Decision Models: Benchmarking and Insights Beyond Jev

**Venue / provenance:** arXiv preprint `2610.03935v2`; attached PDF dated 2026-10-12. Zotero publication date: 2026-10-02. DOI: [10.48550/arXiv.2610.03935](https://doi.org/10.48550/arXiv.2610.03935). [PDF](papers/2026/10_Duan_et_al._General_Decision_Models_Benchmarking_and_Insights_Beyond_Jev.pdf) · [generated text](papers/text/2026/10_Duan_et_al._General_Decision_Models_Benchmarking_and_Insights_Beyond_Jev.txt).

**Zotero citation key:** `2026.DUAN.generaldecisionmodelsbenchmarkinginsightsjev`

**Where it fits.** Duan et al. (2026), *General Decision Models: Benchmarking and Insights Beyond Jev*, provide the widest systems critique in this corpus and an open decision-model training recipe. Their evidence connects bounded local choices to long-context behavior, interactive workflows and aggregate social predictions.

**What it contains.** JEVal contains 11,257 bilingual instances from 36 datasets in ten domains and evaluates 25 model configurations. The paper distinguishes accuracy, returned-choice ECE, raw full-vector Brier error and latency; generative baselines report probabilities under the specified output contract. Decision models lead when evidence is in the input (SII-Decision-27B and Kev-27B are the two most accurate configurations on long-context and document understanding) and trail the best generative LLM by three to six points in medicine, finance and law. Table 1 places the authors' SII-Decision-27B at 79.24 accuracy versus 78.38 for Jev, with the lowest ECE of all configurations (0.0149). Jev, Kev-27B, Intern-Decision-4B and SII-Decision-27B are all better calibrated (by returned-choice ECE) than every generative configuration. In controlled analytic probability tasks (100 items each), Jev selects the prior mode on all items but assigns it 89.35% probability on average when the true average is 35.60% (Table 2; Figure 5). This isolates distribution distortion even when the selected option is right.

In the τ-bench agent experiment, Jev chooses an action while the same DeepSeek base model supplies arguments/responses. Overall success falls from 77.6% to 66.1%, median episode time drops from 267.1 to 160.6 seconds, and P95 time increases from 695.5 to 816.0 seconds (Table 3). Long inputs hurt decision models as they do LLMs: Jev's LongBench accuracy falls from 93.5% at 4–8k tokens to 74.5% near 20k, with evidence in the middle of the context used least (Figures 6–7). In social simulation, Jev agrees less with a reference LLM profiler than Qwen3.8-27B (Jaccard 53.88% versus 65.24%; Table 4), but on individual survey prediction it is on par with non-thinking DeepSeek-V4-Flash (37.69% versus 37.90%) at the lowest latency (0.50 s), and an earlier SII-Decision-27B checkpoint comes within 0.54 points of the best, thinking, configuration at 8.36 s versus 211.65 s (Table 5). Driving about 330,000 ElectionSim voters, SII-Decision-27B calls 47 of 51 states but with roughly twice the vote-share error of the GPT-4o-mini pipeline and a pro-Democratic lean (Figure 8).

SII-Decision-4B and SII-Decision-27B (Qwen3.5-4B and Qwen3.8-27B backbones) retain the backbone's existing single-token label readout and answer a typical query in about 60 and 110 ms on one H100. Reasoning-to-Readout Self-Distillation averages option distributions after two teacher reasoning chains and trains the no-reasoning student to match them, with an ordinal term and a KL anchor to the frozen original model (Eqs. 11–12). It needs no gold labels, so any question with an option set can serve as training data; the 27B model uses 39,279 such questions, beyond which gains stall (§6).

**Strengths.** The paper examines probability estimates against analytically known distributions, reports both median and tail system latency, and holds the argument-generating model fixed in the action-selection comparison. It distinguishes local prediction, sequence-level success and population-level error. The open models, data and training recipe connect single-pass inference to a specified teacher objective.

**Limitations.** Each interactive task runs once, so trajectory variation and alternative controllers could change the systems result. The profiling reference is another LLM rather than verified human truth. Self-distillation inherits teacher weaknesses. Latency settings differ (local RTX 4090, H100, hosted Jev with transport), so speed comparisons are protocol-specific.

**Evidence locations.** §§4–6; Tables 1–5; Figures 3–10; Eqs. 6–12; Appendices E–F. See [official code source maps](REPOSITORIES.md).

<a id="startlux-decision-autothink-decision-models-with-reinforcement-learning-for-calibrated-deliberative-decisions"></a>

## 2026-10 — Zhuang et al. — StartLux-Decision: AutoThink Decision Models with Reinforcement Learning for Calibrated Deliberative Decisions

**Venue / provenance:** arXiv preprint `2610.17309v1`; filed PDF version dated 2026-10-12. Zotero publication date: 2026-10-12. DOI: [10.48550/arXiv.2610.17309](https://doi.org/10.48550/arXiv.2610.17309). [PDF](papers/2026/10_Zhuang_et_al._StartLux_Decision_AutoThink_Decision_Models_with_Reinforcement_Learning_for_Calibrated_Deliberative_Decisions.pdf) · [generated text](papers/text/2026/10_Zhuang_et_al._StartLux_Decision_AutoThink_Decision_Models_with_Reinforcement_Learning_for_Calibrated_Deliberative_Decisions.txt).

**Zotero citation key:** `2026.ZHUANG.startluxdecisionautothinkdecisionmodelsreinforcementlearningcalibrateddeliberativedecisions`

**Where it fits.** Zhuang et al. (2026), *StartLux-Decision: AutoThink Decision Models with Reinforcement Learning for Calibrated Deliberative Decisions*, make inference-time computation a decision variable. This complements always-direct readout and confidence routing to an entirely separate model.

**What it contains.** Instant enables bidirectional prompt attention in full-attention layers. AutoThink keeps causal attention and reads an initial distribution p₀; if its top probability reaches the gate g = 0.9 it returns p₀, otherwise it reasons for up to 4,096 tokens, reads p₁ and returns (1 − α)p₀ + αp₁ with α = 0.75 (Eq. 2). Questions are separate batch rows; the letter readout supports 26 options, with longer lists handled by a multi-round grouping procedure. Thus this interface differs from Intern-Decision's simultaneous masked fields.

Three-stage training combines foundational decision training, variant-specific adaptation and reasoning training. RLCD² rewards improvement in a decision-weighted proper score measured by a frozen scorer, with a soft penalty for long reasoning. Decision Index's public subset guided data, attention and checkpoint choices; DecisionPivot is the stated independent evaluation. Reported deployment includes vLLM, llama.cpp and MLX.

Headline results: on the public Decision Index 0.3 subset the Instant models beat the strongest comparable-scale open decision models by 7.4–16.9 points, and the 27B AutoThink model reaches 73.4. On DecisionPivot contrast pairs, AutoThink beats its Instant counterpart by 11.5–18.4 points, with 27B reaching 86.9% pair accuracy and leading all evaluated systems (§4). RLCD² raises the share of reasoning traces that terminate within the limit by up to 48 points and cuts mean reasoning length by up to 65%, leaving held-out accuracy largely unchanged (§3; Table 2). The stated trade-off is that restrictive budgets lower DecisionPivot accuracy, and even the released 3,072-token budget loses about 4 points on the longest computations at 4B (§3.4; Figure 6). Policy-aware calibration narrows signed confidence–accuracy gaps across 184 selection and routing settings from [−11.7, +20.5] to [−2.7, +2.1] points (§5).

**Strengths.** The paper distinguishes development benchmarks from independent evaluation, discloses task-family specialization, and examines probability fusion, selection effects, reasoning termination and runtime compatibility. The public repository has substantial serving, inference, evaluation and adaptation code.

**Limitations.** Public Decision Index scores are not independent test estimates. AutoThink's full cost includes reasoning and a second readout, which single-readout latency does not capture. Grouped large-option decisions do not reproduce one jointly normalized distribution over the full list. Policy-aware calibration maps still show up to 6.1 points of overconfidence on unseen datasets. The released inference and LoRA utilities are not the full training pipeline and data.

**Evidence locations.** Abstract; §§2–6; Figure 2; Eqs. 1–6; §4.1; Appendix D. See [StartLux source map](REPOSITORIES.md#startluxdecisiontxt).

<a id="releasing-the-inner-jev-a-simple-recipe-for-open-decision-models"></a>

## 2026-10 — Geuter et al. — Releasing the Inner Jev: A Simple Recipe for Open Decision Models

**Venue/provenance.** arXiv preprint 2610.17205v1, 12 October 2026; Harvard University and the Kempner Institute. This is the Jeff release, distinct from SII-Decision. [Primary record](https://arxiv.org/abs/2610.17205).

**Zotero citation key:** `2026.GEUTER.releasinginnerjevsimplerecipeopendecisionmodels`. **PDF:** [open](papers/2026/10_Geuter_et_al._Releasing_the_Inner_Jev_A_Simple_Recipe_for_Open_Decision_Models.pdf).

**Where it fits.** Complements Zhang et al. 2026 (*AnyJev Technical Report*) and Li and Wagle 2026 (*LLM-as-Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them*) by separating pretrained capability, head adaptation and backbone adaptation.

**What it contains.** Sections 3–5 introduce OpenDecisions: 2,352 questions, eleven families, three question types and 23 languages. Four Gemma/Qwen backbones use answer-letter logits and temperature scaling. LoRA and a head initialized from LM-head letter rows are trained on a 417,825-question pool. At 400 steps Gemma 4 31B rises from 79.6 to 84.4 Capability on OpenDecisions, versus Jev's 80.1, and scores 81.5 on JevBench v1.7. The paper reports three runs and about five GPU-hours per run. Backbone adaptation drives most improvement; head-only training contributes little and longer training is not consistently better.

**Strengths.** Zero-shot, head-only, LoRA and training-duration controls isolate what training adds. The paper reports calibration, seed variation and external tasks, and releases [Jeff serving source](https://github.com/j-geuter/Jeff), weights and OpenDecisions.

**Limitations.** The validation set resembles JevBench and includes synthetic/model-labelled examples. Capability is a benchmark composite, not universal utility. Some ablations use one seed, and validation-based temperature/checkpoint choices do not establish external dominance. The public serving repository alone does not establish release of the full training pipeline.

---

<a id="llm-as-jev-llms-are-already-jev-style-decision-models-when-and-how-to-fine-tune-them"></a>

## 2026-10 — Li and Wagle — LLM-as-Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them

**Venue / provenance:** arXiv preprint `2610.02076v3`; filed PDF version dated 2026-10-13. Zotero publication date: 2026-10-01. DOI: [10.48550/arXiv.2610.02076](https://doi.org/10.48550/arXiv.2610.02076). [PDF](papers/2026/10_Li_and_Wagle_LLM_as_Jev_LLMs_Are_Already_Jev_Style_Decision_Models_When_and_How_to_Fine_Tune_Them.pdf) · [generated text](papers/text/2026/10_Li_and_Wagle_LLM_as_Jev_LLMs_Are_Already_Jev_Style_Decision_Models_When_and_How_to_Fine_Tune_Them.txt).

**Zotero citation key:** `2026.LI.llmasjevllmsarealreadyjevstyledecisionmodelswhenhowfinetunethem`

**Where it fits.** Li and Wagle (2026), *LLM-as-Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them*, provide a matched-backbone alternative to attributing all gains to a specialized decision architecture. The filed v3 uses this title; earlier versions used a different title.

**What it contains.** The prompt contains all options and ends with a fixed prefix before a bracketed numeric identifier. Candidate suffixes are prefix-free, allowing variable-length identifiers and large option sets. Their sequence log-likelihoods are scored through shared-prefix caching and parallel suffix evaluation, then normalized over candidates. This can require several short scoring steps after prefill, so it is not universally a single-forward-pass method.

For adaptation, a tree-factorized listwise loss changes legal candidate preferences; three KL anchors to the frozen model preserve legal-versus-illegal mass at trie nodes (L_mass), relative rankings among illegal exit tokens (L_out) and outputs at non-decision positions (L_pos) (Eq. 3). Inference uses full suffix likelihood, whereas local tree normalization is a training construction. Frozen Qwen3.5-4B obtains 81.4% on public JevBench (188/231), on par with the training-free SemIf readout; joint scoring of all candidates beats an isolated-scoring model on the same backbone, 81.4% versus 76.2% (Table 15). The reported LoRA configuration reaches 84.0%. Fine-tuning gains concentrate in represented domains, especially high-cardinality routing and the smaller 0.6B model, whose Banking77 accuracy rises from 22.2% to 60.5%. With native thinking under a 4,096-token budget, the frozen 4B model reaches 94.8% on JevBench, matching GPT-5.6 Sol (94.4%); the authors report it remains over 5× cheaper than large models in non-thinking mode (§5; Appendix L).

**Strengths.** Same-backbone controls, high-cardinality tasks, multimodal checks and tests of general text-generation behavior distinguish readout, adaptation and capability retention. The study reports both useful adaptation and deterioration without adequate regularization (training only on intents lowers JevBench from 81.4% to 74.9%).

**Limitations.** Two backbone sizes and public benchmarks do not establish universal training-free sufficiency. Tuned data mixtures and regularization choices matter. Thinking-mode results consume additional sequential computation. No verified author implementation repository was found; similarly named community projects are distinct.

**Evidence locations.** §§3–5; Eqs. 1–3; Tables 1, 7, 11 and 15; Figure 6; Appendices B–C and L.

<a id="are-ai-decision-models-biased-a-case-study-of-jev"></a>

## 2026-10 — Imperatrice et al. — Are AI Decision Models Biased? A Case Study of Jev

**Venue / provenance:** arXiv preprint `2610.19619v1`; filed PDF version dated 2026-10-14. Zotero publication date: 2026-10-14. DOI: [10.48550/arXiv.2610.19619](https://doi.org/10.48550/arXiv.2610.19619). [PDF](papers/2026/10_Imperatrice_et_al._Are_AI_Decision_Models_Biased_A_Case_Study_of_Jev.pdf) · [generated text](papers/text/2026/10_Imperatrice_et_al._Are_AI_Decision_Models_Biased_A_Case_Study_of_Jev.txt).

**Zotero citation key:** `2026.IMPERATRICE.areaidecisionmodelsbiasedcasestudyjev`

**Where it fits.** Imperatrice et al. (2026), *Are AI Decision Models Biased? A Case Study of Jev*, evaluate whether structured outputs remain sensitive to information that should not alter a decision. The work connects behavioral probes to confidence-based automation without treating a model as a human experimental participant.

**What it contains.** The main protocol collects 41,500 responses from Jev 1.13.0 across cognitive reflection, anchoring, conjunction, framing, sunk-cost, zero-risk and demographic pricing tasks. At the level of selected answers the results are largely encouraging: nine cognitive-reflection items are always answered correctly, and characteristic human choice patterns are mostly avoided. The striking exception is conjunction: the familiar example is answered correctly in all 500 responses, but an edited version is answered wrongly in all 500, at about 95% mean confidence. A separate 30-scenario conjunction robustness experiment contains 15,000 responses and reports 53.96% incorrect selections, with substantial scenario and answer-order variation.

Effects are smaller than in humans but present. An irrelevant dice value shifts the probability-weighted sentence by 0.30 months between the anchors that moved human sentences by 2.53 months (Figure 1). Loss framing leaves choices largely intact but raises the probability on the risky option by about 34 points in the original task. In the edited zero-risk task, reversing option order drops selection of the larger-reduction program from 99.6% to 65.6%. In pricing, 125 names with repeated calls yield small group differences; the only significant gap is $12.30 between Black and White customers in the explicit condition, with Black customers priced lower, opposite to classic human evidence (Figure 6). Because several manipulations move probabilities without changing the selected answer, they can still alter an escalation threshold or expected-score calculation.

**Strengths.** Original and adapted tasks, answer-order reversals and separate reporting of choices, probabilities and derived scores expose effects hidden by aggregate accuracy. The authors do not pool normatively different tasks into one universal bias score.

**Limitations.** Repeated responses to a small set of scenarios are not independent population samples, and one hosted model version cannot establish a general property of decision models. Probability-weighted prices and sentences are analyst-constructed summaries. Small demographic effects in one pricing setup do not establish fairness across applications.

**Evidence locations.** §§3–8; Tables 1 and 3; Figures 1–6. The separate conjunction robustness sample should not be silently counted inside the 41,500-response main protocol.

<a id="typed-decision-models-on-tabular-data"></a>

## 2026-10 — Zhang et al. — Typed Decision Models on Tabular Data

**Venue/provenance.** arXiv preprint 2610.19536v1, 14 October 2026; Wisconsin–Madison, Jilin University and CUHK Shenzhen. [Primary record](http://arxiv.org/abs/2610.19536).

**Zotero citation key:** `2026.ZHANG.typeddecisionmodelstabulardata`. **PDF:** [open](papers/2026/10_Zhang_et_al._Typed_Decision_Models_on_Tabular_Data.pdf).

**Where it fits.** Connects Sharma et al. 2026 (*TypedBench: A Benchmark for Calibration, Framing Sensitivity, and Cost in System One Decision Models*) and Xu et al. 2026 (*JevOut: Natural Context Can Flip Decision Models*) to serialized tables, rather than conventional supervised numerical TFMs.

**What it contains.** Sections 3–6 compare Jev, Clef, Kev-27B and GPT-6 Luna Decisions with three generative LLMs on row classification, fact verification and anomaly detection. Original requests are evaluated under 21 applicable rewrite types: option names/order, table format and row/column order. Decision models achieve competitive accuracy at lower reported cost. Jev, Clef and Kev are relatively stable to option formulation; GPT-6 Luna Decisions remains order-sensitive. Every model changes at least a third of row decisions under some rewrite despite fairly stable aggregate accuracy. Selectively re-querying low-confidence rows recovers much of the benefit of re-querying all rows.

**Strengths.** Information-preserving rewrites distinguish representation from content, and decision-level analyses reveal instability hidden by average scores. Related-backbone comparisons and a selective re-querying intervention strengthen interpretation.

**Limitations.** Seven models, three tasks and 21 rewrites do not establish arbitrary robustness. Confidence tracks stability more strongly than correctness; stable errors can be confident. Re-querying adds requests and partly repairs weak initial serialization. No author-linked code repository is identified in the filed paper.

---

<a id="intern-decision-efficient-multimodal-decision-making-with-autoregressive-masked-language-modeling"></a>

## 2026-10 — Zhu et al. — Intern-Decision: Efficient Multimodal Decision Making with Autoregressive Masked Language Modeling

**Venue / provenance:** arXiv preprint `2610.22131v1`; filed PDF version dated 2026-10-15. Zotero publication date: 2026-10-15. DOI: [10.48550/arXiv.2610.22131](https://doi.org/10.48550/arXiv.2610.22131). [PDF](papers/2026/10_Zhu_et_al._Intern_Decision_Efficient_Multimodal_Decision_Making_with_Autoregressive_Masked_Language_Modeling.pdf) · [generated text](papers/text/2026/10_Zhu_et_al._Intern_Decision_Efficient_Multimodal_Decision_Making_with_Autoregressive_Masked_Language_Modeling.txt).

**Zotero citation key:** `2026.ZHU.interndecisionefficientmultimodaldecisionmakingautoregressivemaskedlanguagemodeling`

**Where it fits.** Zhu et al. (2026), *Intern-Decision: Efficient Multimodal Decision Making with Autoregressive Masked Language Modeling*, supply the technical evidence behind the separately filed Intern-Decision model card. The model consumes a state, optional images and an ordered decision schema. It predicts supplied options rather than discovering actions or learning an environment policy.

**What it contains.** The assistant context is a complete JSON skeleton with one decision placeholder per field. The logit immediately before each placeholder predicts its answer; gold answers appear only in supervision, and neither gold nor predicted answers are fed into other fields. Training uses full-vocabulary cross-entropy at these shifted positions; inference normalizes only legal answer-token logits. The Qwen3.5 vision tower and projector remain frozen while the language backbone is trained. All three released sizes share 17,880 training samples and 23,500 decisions.

The 4B model reports 90.02% unweighted accuracy over seven suites versus 88.74% for Jev. A fixed 289-token, three-field request takes 44.16 ms on one RTX 4090. A separate 96-case known-distribution pilot evaluates full probability vectors: the uncalibrated 4B model's expected Brier (0.628) is worse than Jev's (0.595), and temperature scaling brings it to 0.550, better than Jev overall (Table 6). A 111-item handoff experiment improves correct answers from 82 to 97 while escalating 42 cases; the large model alone scores 99/111, so the hybrid is two items worse but about 53% faster by the authors' estimate (Table 7).

**Strengths.** Explicit causal alignment, target-exclusion checks, checkpoint-bound calibration and separated accuracy, latency and distributional evaluations make the interface auditable. The public code includes training and inference paths, scoring and deterministic pilot generation.

**Limitations.** The 96 cases contain paired order variants of only 48 settings, not 96 independent mechanisms. The latency result is one request shape and device. Public task-family exposure and development choices limit independence of headline comparisons; baselines do not all receive newly fitted temperatures. The routing result is one operating point, and visual demos do not establish sequential policy quality. Training data and private calibration records are not fully released.

**Evidence locations.** §§3–5; Eqs. 1–3; Tables 1–7 (latency in Table 5, pilot in Table 6, handoff in Table 7); Appendices A–C. See [Intern-Decision source map](REPOSITORIES.md#interndecisiontxt).

<a id="system1-arena-which-decisions-can-be-left-to-system-1"></a>

## 2026-10 — Chen et al. — System1-Arena: Which Decisions Can Be Left to System 1?

**Venue/provenance.** arXiv preprint 2610.21244v1, 15 October 2026; University of Texas at Austin. [Primary record](https://arxiv.org/abs/2610.21244).

**Zotero citation key:** `2026.CHEN.system1arenawhichdecisionscanbeleftsystem1`. **PDF:** [open](papers/2026/10_Chen_et_al._System1_Arena_Which_Decisions_Can_Be_Left_to_System_1.pdf).

**Where it fits.** Extends Duan et al. 2026 (*General Decision Models: Benchmarking and Insights Beyond Jev*) to a common interface spanning static tasks and closed loops. It tests whether fast, accurate local readout actually produces successful control.

**What it contains.** Sections 3–5 define 92,125 questions across 105 tasks from 268 public sources and 138 environments in 18 families. Thirty systems comprise seven closed LLMs, thirteen open answer-token LLMs and ten System-1 models. Accuracy, Brier score, latency and cost are measured; real-time environments advance during inference. Strong System-1 models match fast closed LLMs on non-agentic tasks with better probability quality at about one-quarter of their latency. A reasoning LLM is more accurate at about 70 times the cost. Closed-loop success reaches 32.9% for a large open LLM, while small System-1 models rarely succeed. The headline closed-loop table uses 127 environments, a subset of the 138 supplied.

**Strengths.** Identical decision requests, explicit probability scoring and static/closed-loop comparisons reveal ranking reversals. [S1-Arena source](https://github.com/TianyuCodings/S1-Arena) and a dataset are released.

**Limitations.** Section 7 notes inherited label noise, some authored instructions, possible pretraining exposure and changing hosted APIs. One draw per request does not estimate run-to-run variability. Static accuracy is not closed-loop success or evidence of an optimal policy.

---

## Web-source overview

These fifteen selected sources have no PDF attachment. Their curated metadata,
original URLs, date precision and review dates are retained in
[the web-source registry](papers/web_sources.json). They have source summaries,
not fabricated PDFs. Year-only dates mean the original publication day is
unconfirmed; Hub creation times are not treated as public launch dates.
See [DECISION_MODELS.md](DECISION_MODELS.md) for model specifications and costs.

| Date | Authors | Title | Contribution | Summary |
|---|---|---|---|---|
| 2026 | H2O.ai | H2O-Lightning-4B | A multimodal decision checkpoint exposes calibrated option scoring and checkpoint-specific attention/serving settings. | [source summary](#web-skwpxqtg) |
| 2026 | Inception | Mercury Decide: Create a decision | A hosted decision endpoint specifies typed probabilities, multimodal request rules and input-only promotional billing. | [source summary](#web-ps2pzgda) |
| 2026-09-15 | Diogo Almeida | Introducing System One Models & Jev | A provider release defines the typed probabilistic interface. | [source summary](#web-qezz55x7) |
| 2026-09-22 | Upstage | Solar Decide | A Solar Mini 4 decision endpoint provides typed probabilities with a documented 512K context. | [source summary](#web-qzkmbk7l) |
| 2026-09-23 | Together AI | Tev1-4B-experimental | An experimental supervised fine-tune selects an answer letter using the ordinary language-model head. | [source summary](#web-rgvmcn25) |
| 2026-09-26 | InternLM | Intern-Decision-4B | A multimodal model card specifies multi-field candidate readout and calibration. | [source summary](#web-x58irxca) |
| 2026-09-30 | Sahibzada Allahyar, Mary Newhauser | Introducing GLiDE: The First Thinking Decision Model | Adaptive reasoning adds computation when direct structured scoring is uncertain. | [source summary](#web-msejsvgw) |
| 2026-09-30 | Jared Palmer | Kev-27B | A public pointer-head model provides typed probabilities and a tested long-document serving contract. | [source summary](#web-q9s5d6r2) |
| 2026-10-01 | Michelle Chen, Alex Reneau, Kevin Flansburg | Introducing Clef: our open-source decision models, and new RL fine-tuning platform | A release combines schema scoring, cross-field attention and adaptation. | [source summary](#web-mwjhy75j) |
| 2026-10-01 | Marc Brooker, Mike Chambers, Fabio Nonato de Paula | Introducing Strands Decider 2B: a small, open source, decision model | A small pointer-head model exposes a training and experimentation path. | [source summary](#web-gi68ips2) |
| 2026-10-03 | vLLM Semantic Router Team | Decision-2.0-Vega-27B | An Apache-licensed model family scores multiple typed questions over a shared request without prose generation. | [source summary](#web-bh58bep7) |
| 2026-10-06 | Perplexity AI | pplx-decider-v1.1-27b | A model card makes attention and calibration part of the inference contract. | [source summary](#web-de9kqqlx) |
| 2026-10-07 | Liquid AI | Open d1: Edge decision models for text, vision, and audio | An edge-focused release adds text, image and audio decision variants. | [source summary](#web-4u52t7rc) |
| 2026-10-09 | Achint Srivastava | Introducing Microsoft-Decision-1, our model for fast decision-making | A hosted release emphasizes scoring, perturbation robustness and benchmark breadth. | [source summary](#web-lelm4ubr) |
| 2026-10-22 | OpenAI | Build more responsive apps with the Decisions API | Hosted predicate, choice and rubric scoring with text, image and native JSON inputs. | [source summary](#web-q9x2h26h) |

## Web sources

<a id="web-skwpxqtg"></a>

### 2026 — H2O-Lightning-4B

**Venue / provenance:** H2O.ai; report. [Primary source](https://huggingface.co/h2oai/h2o-lightning-4b). Reviewed 2026-10-23. Undated live model card, accessed 2026-10-23. Hub repository created 2026-10-02; creation time alone is not proof of public release date. Apache-2.0 for this Qwen-based checkpoint.

**Zotero citation key:** `2026.H2O.AI.h2olightning4b`

**Where it fits.** H2O.ai (2026), *H2O-Lightning-4B*, documents an Apache-licensed Qwen3.5-4B decision model.

**What it contains.** A serving shim returns choice, yes/no and ordinal-score probabilities for text and images. The current release distinguishes one-way and two-way reading, saved calibration and yes/no adjustments. Serving examples use a 40,960-token engine context and a separate 32,000-token state cap.

**Strengths.** Code, configuration and revision-specific checks expose reproduction hazards beyond the weights.

**Limitations.** Provider leaderboard results are not independent validation. State truncation and billing differ from processed-input length; the full backbone configuration is not a validated serving limit. The live card is undated, and repository creation alone does not establish its public launch date.

<a id="web-ps2pzgda"></a>

### 2026 — Mercury Decide: Create a decision

**Venue / provenance:** Inception Platform; report. [Primary source](https://docs.inceptionlabs.ai/api-reference/decisions/create-a-decision). Reviewed 2026-10-23. Undated model/API reference, accessed 2026-10-23. Exact original public release date not confirmed from the primary reference. Pricing source: https://docs.inceptionlabs.ai/get-started/models .

**Zotero citation key:** `2026.INCEPTION.mercurydecidecreatedecision`

**Where it fits.** Inception (2026), *Mercury Decide: Create a decision*, defines a hosted structured-decision interface.

**What it contains.** Shared state and named questions produce binary probabilities, categorical choices or ordinal scores. The reference permits base64 images in state/instructions with explicit image and request-body limits. The model/pricing page lists input-only billing at a promotional rate.

**Strengths.** A dedicated request/response reference separates decision scoring from chat completions and tool execution.

**Limitations.** The selected sources disclose neither weights nor a reproducible training implementation. A body-size limit is not a token-context guarantee. The exact original public-release day and parameter count remain unconfirmed; Mercury's general diffusion branding does not establish this endpoint's architecture.

<a id="web-qezz55x7"></a>

### 2026-09 — Introducing System One Models & Jev

**Venue / provenance:** TypeSafe AI Blog; blogPost. [Primary source](https://typesafe.ai/blog/introducing-system-one-models-and-jev). Reviewed 2026-10-20. The primary page displays September 15, 2026; the existing Zotero record was corrected to 2026-09-15 with its citation key preserved.

**Zotero citation key:** `2026.ALMEIDA.introducingsystemonemodelsjev`

**Where it fits.** Almeida (2026), *Introducing System One Models & Jev*, provides the vendor's rationale for replacing generated answers with typed decisions.

**What it contains.** It introduces Jev, parallel probabilistic outputs and RLCD, and evaluates fixed workflows against reference probabilities from stronger LLMs.

**Strengths.** The interface and evaluation assumptions are explicit, including developer-created workflows and the reference-model choice.

**Limitations.** This is a provider announcement. Type validity does not establish factual correctness, calibration or reliable action selection. Its workflow evidence is agreement with reference models rather than independent outcome truth; reported efficiency should not be generalized beyond those workloads.

<a id="web-qzkmbk7l"></a>

### 2026-09 — Solar Decide

**Venue / provenance:** Upstage Console; report. [Primary source](https://console.upstage.ai/docs/models/solar-decide). Reviewed 2026-10-23. Live model card/API documentation. Its Versions section explicitly dates solar-decide beta to 2026-09-22. Accessed 2026-10-23.

**Zotero citation key:** `2026.UPSTAGE.solardecide`

**Where it fits.** Upstage (2026), *Solar Decide*, adds a hosted System One interface built on Solar Mini 4.

**What it contains.** State and typed questions return a choice, yes/no probability or ordinal score. The card dates the beta to 22 September 2026, advertises 512K context and lists input, cached-input and free-output rates. It emphasizes Korean understanding for routing and policy checks.

**Strengths.** The provider states version, endpoint, context and billing explicitly.

**Limitations.** The release is beta, with no public weights or verified parameter count in the selected card. Language and context claims are provider specifications; they do not establish probability quality or accuracy across all supported lengths.

<a id="web-rgvmcn25"></a>

### 2026-09 — Tev1-4B-experimental

**Venue / provenance:** Together AI; report. [Primary source](https://huggingface.co/togethercomputer/Tev1-4B-experimental). Reviewed 2026-10-23. Model card. Public launch on 2026-09-23 corroborated by https://www.together.ai/blog/how-to-train-your-own-jev . Fine-tuned weight license is being finalized; the base-model license alone does not establish open-source status.

**Zotero citation key:** `2026.TOGETHERAI.tev14bexperimental`

**Where it fits.** Together AI (2026), *Tev1-4B-experimental*, supplies a lightweight adaptation baseline alongside specialized decision heads.

**What it contains.** A Qwen3.5-4B fine-tune reads state, a question and 2–24 labelled options, then generates an answer letter. The official recipe releases training code and describes ordinary LoRA supervision with the existing LM head. A smaller 0.8B variant is available.

**Strengths.** Public weights and a concrete data/training recipe make the adaptation path inspectable.

**Limitations.** The endpoint returns a letter; native multi-question probability vectors are not established by that example. The card calls the release experimental and says the fine-tuned weight license is still being finalized. Development benchmarks and base-model context configuration do not establish independent transfer or validated long-context operation.

<a id="web-x58irxca"></a>

### 2026-09 — Intern-Decision-4B

**Venue / provenance:** InternLM; model card. [Primary source](https://huggingface.co/internlm/Intern-Decision-4B). Reviewed 2026-10-20. Zotero now records 2026-09-26. The official [first substantive upload](https://huggingface.co/internlm/Intern-Decision-4B/commit/0e5e6aa7d6d750e2b1504ba11a8136cb58aeb3cd) added the card, inference source and checkpoint that day. A [same-day public demo announcement](https://huggingface.co/internlm/Intern-Decision-4B/discussions/1) by Hugging Face's open-source team corroborates public availability; the discussion API records 2026-09-26 at 11:33:37 UTC. The date is not inferred from Git history alone.

**Zotero citation key:** `2026.INTERNLM.interndecision4b`

**Where it fits.** InternLM (2026), *Intern-Decision-4B*, documents a Qwen-derived alternative with explicit multi-field inference.

**What it contains.** A complete output skeleton contains decision placeholders; one causal forward pass reads the preceding logits, restricts them to field-specific candidate symbols and applies temperature calibration. The card describes separate calibration/validation cases and a 96-case known-distribution pilot.

**Strengths.** It specifies inference semantics, limits and calibration, making reproduction less ambiguous than generic text-generation examples.

**Limitations.** Provider benchmarks and a small diagnostic pilot do not establish broad distributional correctness. Generic Hub generation snippets are not the documented decision-scoring path.

<a id="web-msejsvgw"></a>

### 2026-09 — Introducing GLiDE: The First Thinking Decision Model

**Venue / provenance:** Fastino Blog; blogPost. [Primary source](https://fastino.ai/blog/introducing-glide-the-first-thinking-decision-model). Reviewed 2026-10-23. Announcement date and byline from the primary page. Current model catalog and capability documentation supersede the announcement's older 40k context claim: https://docs.fastino.ai/concepts/models and https://docs.fastino.ai/concepts/glide-capabilities .

**Zotero citation key:** `2026.ALLAHYAR.introducingglidefirstthinkingdecisionmodel`

**Where it fits.** Allahyar and Newhauser (2026), *Introducing GLiDE: The First Thinking Decision Model*, extend direct readout with selective additional reasoning.

**What it contains.** GLiDE first scores caller-defined options and can reason further on uncertain cases. Current capability documentation supports choice, yes/no and score outputs, images and a 65,536-token rendered-prompt limit; this supersedes the announcement's older 40k description.

**Strengths.** The design makes computation conditional on decision difficulty while retaining structured probabilities.

**Limitations.** The benchmark comparison is provider-run. Multiple internal passes and questions affect usage, so one request is not necessarily one forward pass. Current HTML and Markdown catalogs disagree on parameter disclosure; a firm count is unconfirmed. No public-weight release was verified.

<a id="web-q9s5d6r2"></a>

### 2026-09 — Kev-27B

**Venue / provenance:** Jared Palmer / Kev; report. [Primary source](https://github.com/jaredpalmer/kev/blob/main/docs/model-cards/kev-27b.md). Reviewed 2026-10-23. Model card for Kev-27B v2 (Kev 1.0), explicitly released on 2026-09-30. This dates the documented release rather than the whole family's first experiment. Weights: https://huggingface.co/jaredpalmer/kev-27b .

**Zotero citation key:** `2026.PALMER.kev27b`

**Where it fits.** Palmer (2026), *Kev-27B*, documents the large member of a self-hosted decision-model family.

**What it contains.** The 30 September v2 combines a fully fine-tuned Qwen3.8-27B torso with a small pointer head and fitted temperature. It supports choice, yes/no and ordinal-score questions. The card distinguishes 65,536-token states from question overhead and publishes training/serving code.

**Strengths.** Public weights, code and a dedicated context-validation protocol make the release inspectable.

**Limitations.** The card acknowledges checkpoint selection after earlier test results, so reported margins can be optimistic. Calibration and knowledge remain domain-dependent. Family size names are rounded backbone labels, not exact loaded parameter totals; the large checkpoint requires substantial memory.

<a id="web-mwjhy75j"></a>

### 2026-10 — Introducing Clef: our open-source decision models, and new RL fine-tuning platform

**Venue / provenance:** Cloudflare Blog; blogPost. [Primary source](https://blog.cloudflare.com/clef-decision-models/). Reviewed 2026-10-20. Publication date and provider byline verified against the primary page; no immutable PDF version.

**Zotero citation key:** `2026.CHEN.introducingclefouropensourcedecisionmodelsnewrlfinetuningplatform`

**Where it fits.** Chen et al. (2026), *Introducing Clef: our open-source decision models, and new RL fine-tuning platform*, describes an open implementation of schema-bound scoring.

**What it contains.** Qwen backbones feed option-specific evidence routing and cross-field attention. Training combines smoothed cross-entropy, Brier loss, adapters and a later RL objective. The release includes Clef and Clef-flash, vision inputs and provider-run benchmark comparisons.

**Strengths.** Released inference artifacts make architectural details inspectable; the post connects multi-field outputs to a concrete training design.

**Limitations.** The training data are internal and the comparisons are provider-run. Public benchmark wins and typed outputs do not validate general calibration or sequential reliability. The adaptation platform is a product capability, not independent evidence of improved downstream outcomes.

<a id="web-gi68ips2"></a>

### 2026-10 — Introducing Strands Decider 2B: a small, open source, decision model

**Venue / provenance:** Strands Agents; blogPost. [Primary source](https://strandsagents.com/blog/introducing-strands-decider/). Reviewed 2026-10-20. Publication date and provider byline verified against the primary page; no immutable PDF version.

**Zotero citation key:** `2026.BROOKER.introducingstrandsdecider2bsmallopensourcedecisionmodel`

**Where it fits.** Brooker et al. (2026), *Introducing Strands Decider 2B: a small, open source, decision model*, offers a local experimentation-oriented implementation.

**What it contains.** A Qwen3.5-2B torso uses a pointer head to score option positions against an answer position, with LoRA adaptation. The release links code, training scripts/data and architecture iterations; it reports accuracy, Brier scores and hardware-specific latency.

**Strengths.** The public development history and training materials support inspection and reproduction beyond a hosted API.

**Limitations.** Iterative tuning against a public benchmark risks benchmark-specific selection. Local timing depends on hardware and input length; an illustrative guardrail integration does not establish safe or reliable deployment. This is a release article, not a controlled independent study.

<a id="web-bh58bep7"></a>

### 2026-10 — Decision-2.0-Vega-27B

**Venue / provenance:** vLLM Semantic Router; report. [Primary source](https://huggingface.co/vllm-sr/Decision-2.0-Vega-27B). Reviewed 2026-10-23. Model card. Public Decision 2.0 release corroborated by the official project announcement/implementation issue dated 2026-10-03: https://github.com/vllm-project/semantic-router/issues/4479 . Earlier Hub creation is not treated as the public release date.

**Zotero citation key:** `2026.VLLMSEMANTICROUTERTEAM.decision20vega27b`

**Where it fits.** vLLM Semantic Router Team (2026), *Decision-2.0-Vega-27B*, connects typed decisions to an established inference-routing project.

**What it contains.** Decision 2.0 spans 0.6B–27B size labels. Vega's card reports 29.37B actual parameters, 32,768-token context and simultaneous choice, yes/no and score probabilities. The official runtime specifies candidate readout and checkpoint-specific execution.

**Strengths.** Weights, licensing and runtime behavior are public, enabling local inspection and version pinning.

**Limitations.** The card's evaluation is release-specific and includes provider/maintainer comparisons. Nominal size labels are not exact parameter totals. A shared forward pass constrains latency, not correctness, calibration transfer or sequential planning quality.

<a id="web-de9kqqlx"></a>

### 2026-10 — pplx-decider-v1.1-27b

**Venue / provenance:** Perplexity AI; model card. [Primary source](https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b). Reviewed 2026-10-20. Zotero now records 2026-10-06, the date of the [official public announcement](https://community.perplexity.ai/t/pplx-decider-v1-1-27b-our-updated-open-weights-multimodal-decision-model-is-now-available/6286). The [checkpoint history](https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b/commits/main) records an earlier release commit on 2026-10-05; its original card explicitly described a private release. The registry preserves both dates rather than treating that private commit as the public announcement.

**Zotero citation key:** `2026.PERPLEXITYAI.pplxdeciderv1127b`

**Where it fits.** Perplexity AI (2026), *pplx-decider-v1.1-27b*, illustrates how checkpoint-specific execution affects decision behavior.

**What it contains.** The card describes a separate decision readout, noncausal full-attention layers, native linear-attention behavior and one application of the saved calibration temperature. It reports Decision Index gains and supplies source/checksum provenance.

**Strengths.** It identifies concrete reproduction hazards: changing the attention mask, using an incompatible output head or applying temperature twice.

**Limitations.** Its leaderboard comparison is a provider result and does not isolate additional training data from mask changes. Image settings can move beyond the evaluated distribution. The public announcement and earlier checkpoint commit are distinct events; neither dates later edits to the live card.

<a id="web-4u52t7rc"></a>

### 2026-10 — Open d1: Edge decision models for text, vision, and audio

**Venue / provenance:** Liquid AI Blog; blogPost. [Primary source](https://www.liquid.ai/blog/d1-open). Reviewed 2026-10-20. Publication date and provider byline verified against the primary page; no immutable PDF version.

**Zotero citation key:** `2026.LIQUIDAI.opend1edgedecisionmodelstextvisionaudio`

**Where it fits.** Liquid AI (2026), *Open d1: Edge decision models for text, vision, and audio*, broadens the deployment and modality axis.

**What it contains.** The release introduces d1-3B and experimental d1-omni-600M, describing distinct backbones, modality adaptation and benchmark results. It reports input-to-output latency across workstation and edge hardware, including longer states and packed workloads.

**Strengths.** The hardware/input breakdown makes latency claims more interpretable than a single headline speedup. Separate artifacts expose the two architectures.

**Limitations.** The smaller multimodal checkpoint is experimental. The post does not report the private vision split and identifies audio decision benchmarking as unresolved. Demonstrations and provider measurements do not establish broad multimodal decision reliability.

<a id="web-lelm4ubr"></a>

### 2026-10 — Introducing Microsoft-Decision-1, our model for fast decision-making

**Venue / provenance:** Command Line; blogPost. [Primary source](https://commandline.microsoft.com/microsoft-decision-1-model-foundry/). Reviewed 2026-10-20. Publication date and provider byline verified against the primary page; no immutable PDF version.

**Zotero citation key:** `2026.SRIVASTAVA.introducingmicrosoftdecision1ourmodelfastdecisionmaking`

**Where it fits.** Srivastava (2026), *Introducing Microsoft-Decision-1, our model for fast decision-making*, represents the hosted deployment branch.

**What it contains.** The announcement describes Qwen3.5-9B post-training for single-pass option probabilities and comparisons across 36 benchmarks. It reports perturbation tests, calibration and latency, and names Foundry/OpenRouter availability.

**Strengths.** It explicitly separates accuracy, robustness, probability quality and runtime, and states that evaluation benchmarks were blinded from training.

**Limitations.** These are provider claims; the selected source does not supply a reproducible training implementation. Its perturbation protocol differs from adaptive context search, so a low average flip rate cannot rebut JevOut's adversarial findings. The article was updated after release and has no immutable PDF in Zotero.

<a id="web-q9x2h26h"></a>

### 2026-10 — Build more responsive apps with the Decisions API

**Venue / provenance:** OpenAI; blogPost. [Primary source](https://openai.com/index/decisions-api/). Reviewed 2026-10-23. General-availability announcement. Public beta began on 2026-10-06; API specifications and pricing were checked on 2026-10-23.

**Zotero citation key:** `2026.OPENAI.buildmoreresponsiveappsdecisionsapi`

**Where it fits.** OpenAI (2026), *Build more responsive apps with the Decisions API*, documents a hosted alternative to local decision checkpoints.

**What it contains.** GPT-6 Luna answers predicates, choices and ordered-rubric scores through a dedicated endpoint. The general-availability release adds native JSON, shared-input caching, question-specific images and up to 400 questions per request. Current documentation charges input and cache operations, with no output-token charge.

**Strengths.** The provider specifies answer semantics and usage accounting rather than requiring applications to parse generated prose.

**Limitations.** Weights and training details are unavailable. Provider/customer latency examples are workload-specific; an API probability is not independently validated calibration. Beta and general-availability pricing differ, and a general Luna context window must not be assumed for this endpoint.
