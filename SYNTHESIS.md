# Decision models: cross-source synthesis

This selected corpus studies **fast decisions over supplied options**. Restricting
outputs can reduce decoding cost, while reliability still depends on evidence,
tasks, probability semantics and the surrounding controller. A valid option is not
necessarily correct, and a correct local choice need not produce a successful
sequence of actions.

The thirteen papers are arXiv preprints; the seven other sources are provider releases
or model cards. [SUMMARIES.md](SUMMARIES.md) records evidence locations, limitations
and Zotero citation keys. [REPOSITORIES.md](REPOSITORIES.md) maps official code
snapshots. This project-neutral synthesis distinguishes reported results from
interpretation. The selected corpus does not constitute a general survey of
classical decision theory, optimization or causal policy learning.

## Timeline & lineage

Dates follow the **filed PDF version**, not initial publication. Same-month
entries follow the confirmed version day. Connections below are conceptual and
are not claims about training-data inheritance or priority.

| Date | Paper | What it added | Builds on |
|---|---|---|---|
| 2026-09 | Li et al. (2026), [Beyond Calibration: Do a Typed-Decision Model's Probabilities Obey the Probability Axioms?](SUMMARIES.md#beyond-calibration-do-a-typed-decision-model-s-probabilities-obey-the-probability-axioms) | Label-free logical checks expose inconsistency between negation, disjunction, yes/no and categorical probabilities. | Probability coherence beyond marginal calibration |
| 2026-09 | Deußer et al. (2026), [Evaluating and Benchmarking the System One Model Jev](SUMMARIES.md#deusser-benchmark) | Frozen-template evaluation distinguishes calibration across output primitives | Typed choice, binary and ordinal interfaces |
| 2026-09 | Zhang et al. (2026), [AnyJev Technical Report](SUMMARIES.md#anyjev-technical-report) | Frozen-LLM readouts separate label-prior correction, option-order averaging, calibration and adaptive rotation cost. | Restricted next-token probabilities and permutation averaging |
| 2026-10 | Cao et al. (2026), [SearchJev: A Fast and Calibrated System-1 Model for Search Agents](SUMMARIES.md#searchjev) | Search-specific probability learning and delegation; filed 4 October | Direct readout and hybrid search control |
| 2026-10 | Rafe and Das (2026), [Benchmarking System One decision models against trained classifiers and language models for automated decision gates](SUMMARIES.md#benchmarking-system-one-decision-models-against-trained-classifiers-and-language-models-for-automated-decision-gates) | Matched decision gates compare specialist models, trained classifiers and LLM readouts under calibration, rejection and cascade costs. | Supervised baselines, selective risk and application-level routing |
| 2026-10 | Xu et al. (2026), [JevOut: Natural Context Can Flip Decision Models](SUMMARIES.md#jevout) | Answer-preserving context search exposes confident errors; filed 8 October | Input invariance and robustness |
| 2026-10 | Li et al. (2026), [JEV-as-a-Judge: Accept When Confident, Escalate When Unsure](SUMMARIES.md#jev-judge) | Frozen and prospective escalation tests; filed 9 October | Selective prediction and cascaded judging |
| 2026-10 | Sharma et al. (2026), [TypedBench: A Benchmark for Calibration, Framing Sensitivity, and Cost in System One Decision Models](SUMMARIES.md#typedbench-a-benchmark-for-calibration-framing-sensitivity-and-cost-in-system-one-decision-models) | Policy-generated tasks evaluate wording robustness, calibration noise floors and decisions under asymmetric costs. | Typed interfaces, programmatic ground truth and selective prediction |
| 2026-10 | Duan et al. (2026), [General Decision Models: Benchmarking and Insights Beyond Jev](SUMMARIES.md#general-decision-models) | Analytic uncertainty, system failures and reasoning distillation; filed 12 October | Typed decisions and agent evaluation |
| 2026-10 | Zhuang et al. (2026), [StartLux-Decision: AutoThink Decision Models with Reinforcement Learning for Calibrated Deliberative Decisions](SUMMARIES.md#startlux-decision-autothink-decision-models-with-reinforcement-learning-for-calibrated-deliberative-decisions) | Instant and AutoThink models combine bidirectional readout, selective reasoning and decision-weighted probability rewards. | Direct option scoring, reasoning supervision and proper scoring rules |
| 2026-10 | Li and Wagle (2026), [LLM-as-Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them](SUMMARIES.md#llm-as-jev-llms-are-already-jev-style-decision-models-when-and-how-to-fine-tune-them) | Prefix-free candidate scoring tests when frozen LLMs suffice and when anchored fine-tuning or bounded reasoning helps. | Joint candidate likelihood, constrained readout and KL-regularized adaptation |
| 2026-10 | Imperatrice et al. (2026), [Are AI Decision Models Biased? A Case Study of Jev](SUMMARIES.md#are-ai-decision-models-biased-a-case-study-of-jev) | Behavioral tasks distinguish selected answers from probability shifts under irrelevant context, framing and option order. | Cognitive-bias paradigms and controlled input variation |
| 2026-10 | Zhu et al. (2026), [Intern-Decision: Efficient Multimodal Decision Making with Autoregressive Masked Language Modeling](SUMMARIES.md#intern-decision-efficient-multimodal-decision-making-with-autoregressive-masked-language-modeling) | Multimodal masked decision training scores multiple fields in one causal pass, with separate calibration and handoff evaluations. | Native LM-head scoring, multimodal inputs and post-hoc calibration |

## Web-source timeline

These selected records have no PDFs. Dates follow verified public announcements
or model-card release history, not retrieval dates. Intern-Decision's 26 September
release is corroborated by its upload and a same-day public demo announcement.
Perplexity uses its 6 October public announcement, not its 5 October
private checkpoint commit. The [web registry](papers/web_sources.json) retains
the separate dates and evidence.
Each summary links its original source. Release claims are not independent replications.

| Date | Source | Role |
|---|---|---|
| 2026-09-15 | Almeida 2026 — [Introducing System One Models & Jev](SUMMARIES.md#web-qezz55x7) | Provider interface and motivation |
| 2026-09-26 | InternLM 2026 — [Intern-Decision-4B](SUMMARIES.md#web-x58irxca) | Multi-field readout and calibration; 26 September upload and public demo |
| 2026-10-01 | Chen et al. 2026 — [Introducing Clef: our open-source decision models, and new RL fine-tuning platform](SUMMARIES.md#web-mwjhy75j) | Open architecture and adaptation |
| 2026-10-01 | Brooker et al. 2026 — [Introducing Strands Decider 2B: a small, open source, decision model](SUMMARIES.md#web-gi68ips2) | Local model and public development materials |
| 2026-10-06 | Perplexity AI 2026 — [pplx-decider-v1.1-27b](SUMMARIES.md#web-de9kqqlx) | Checkpoint-specific inference contract; public announcement |
| 2026-10-07 | Liquid AI 2026 — [Open d1: Edge decision models for text, vision, and audio](SUMMARIES.md#web-4u52t7rc) | Edge and modality expansion |
| 2026-10-09 | Srivastava 2026 — [Introducing Microsoft-Decision-1, our model for fast decision-making](SUMMARIES.md#web-lelm4ubr) | Hosted release and provider evaluation |

## Decisions and available information

Deußer et al. 2026 (*Evaluating and Benchmarking the System One Model Jev*) and
Duan et al. 2026 (*General Decision Models: Benchmarking and Insights Beyond Jev*)
evaluate mappings from state, instruction and finite options to probabilities.
The application supplies the candidates; the model neither discovers a feasible
set nor proves that all useful actions were offered. Expected rubric scores are
not automatically economic utilities.

Cao et al. 2026 (*SearchJev: A Fast and Calibrated System-1 Model for Search Agents*)
make the controller explicit: bounded relevance, sufficiency and verification
judgments guide search while a larger model generates queries and answers.
Li et al. 2026 (*JEV-as-a-Judge: Accept When Confident, Escalate When Unsure*) choose
whether to accept a cheap verdict or pay for a fallback. Their threshold procedure
seeks low expense under an empirical accuracy tolerance, not an optimum under
arbitrary error costs. Xu et al. 2026 (*JevOut: Natural Context Can Flip Decision
Models*) show that context additions can preserve the answer yet redirect selection.
A schema constrains output form, not correct interpretation of the evidence.

| Axis | Supported evidence | Unestablished claim |
|---|---|---|
| Objective | Accuracy, probability quality, selective risk, fees, latency | A shared utility function across studies |
| Decision variables | Labels, rubric levels, tool choices, escalation | General continuous or combinatorial optimization |
| Constraints | Schemas, input limits, controller rules, empirical tolerances | Guaranteed real-world constraint satisfaction |
| Uncertainty | Top-label confidence, binary and full distributions, analytic probes | Universal calibration under shift |
| Information | Text, evidence, history and some multimodal inputs | Sufficient state for an underlying environment |
| Sequential behavior | Search and tool-agent experiments | Optimal-policy or cumulative-regret guarantees |
| Causal assumptions | Controlled component comparisons within harnesses | Identification of counterfactual policy value |
| Cost | Measured fees and runtime under stated protocols | Hardware-independent efficiency rankings |

## Readout, adaptation and selective computation

Zhang et al. 2026 (*AnyJev Technical Report*) and Li and Wagle 2026
(*LLM-as-Jev: LLMs Are Already Jev-Style Decision Models -- When and How to
Fine-Tune Them*) make unchanged backbones essential controls. The former averages
option rotations and divides out a label prior estimated by batch calibration;
the latter scores prefix-free numeric suffixes jointly. Both show that readout
alone recovers much capability: AnyJev's adaptive stopping reads 7.3 of 18
rotations and serves 2.22× as many decisions per second on vLLM, and a frozen
4B backbone reaches 81.4% on public JevBench, or 94.8% with budgeted native
thinking, matching GPT-5.6 Sol. Their computation differs: one prefill per
rotation is not one prefill for a decision, and suffix scoring or thinking adds
forward steps. Neither procedure creates new model knowledge.

Zhu et al. 2026 (*Intern-Decision: Efficient Multimodal Decision Making with
Autoregressive Masked Language Modeling*) instead train masked answer positions
in a shared causal schema. Zhuang et al. 2026 (*StartLux-Decision: AutoThink
Decision Models with Reinforcement Learning for Calibrated Deliberative
Decisions*) process questions separately and distinguish bidirectional Instant
from causal AutoThink. Multiple fields per request, candidate normalization,
prompt attention and reasoning budgets therefore need separate accounting.
Large candidate lists may require grouping or additional scoring, even when all
systems expose a similarly shaped API.

The adaptation evidence is substantial but conditional. LLM-as-Jev and
StartLux-Decision find large benefits on represented task families and limited
transfer elsewhere. StartLux's AutoThink gains 11.5–18.4 points of DecisionPivot
pair accuracy over Instant (86.9% at 27B), and RLCD² cuts reasoning length by up
to 65%. Duan et al. 2026 (*General Decision Models: Benchmarking and Insights
Beyond Jev*) show that an open self-distilled model, SII-Decision-27B, slightly
exceeds Jev on JEVal (79.24 versus 78.38) with the lowest ECE in that benchmark.
Intern-Decision's pilot evaluates exact distributions separately from task
accuracy. Improvements from supervision, temperature scaling, changed attention,
longer reasoning or a different backbone should not be pooled into a single
claim about the typed interface.

## Calibration has several meanings

Deußer et al. 2026 (*Evaluating and Benchmarking the System One Model Jev*) find
low pooled Choice ECE but weaker rare-label fan-out and a gap between ranking
and fixed-threshold decisions. Duan et al. 2026 (*General Decision Models:
Benchmarking and Insights Beyond Jev*) show that identifying the most likely
option can coexist with severe overstatement of its probability. These measure
different objects: confidence that a selected label is correct across a task
distribution differs from recovering the stipulated distribution for each problem.

Cao et al. 2026 (*SearchJev: A Fast and Calibrated System-1 Model for Search Agents*)
train against soft targets with proper scoring losses and calibrate temperatures
on held-out examples. The targets inherit the annotation/teacher process, and
Table 5 shows that OOD accuracy can remain high while calibration worsens.
Li et al. 2026 (*JEV-as-a-Judge: Accept When Confident, Escalate When Unsure*)
therefore validate the downstream acceptance rule by workload instead of treating
one ECE value as a deployment certificate.

Sharma et al. 2026 (*TypedBench: A Benchmark for Calibration, Framing
Sensitivity, and Cost in System One Decision Models*) add a matched finite-sample
calibration reference and show that asymmetric decision cost can rank systems
differently from accuracy: Jev is systematically under-confident yet ranks its
own errors best, while acting on its probabilities under a 2:1 cost doubles its
cost relative to its top answer. Li, He and Li 2026 (*Beyond Calibration: Do a
Typed-Decision Model's Probabilities Obey the Probability Axioms?*) test a
different requirement: probabilities assigned to related questions should obey
the explicitly stated partition. Their controls show that the LLM readout
affects both the size and direction of violations. Low ECE on one question form
does not authorize combining yes/no and categorical probabilities into one belief.

Zhuang et al. 2026 (*StartLux-Decision: AutoThink Decision Models with
Reinforcement Learning for Calibrated Deliberative Decisions*) further show why
calibration must be checked after selection and probability fusion. Rafe and Das
2026 (*Benchmarking System One decision models against trained classifiers and
language models for automated decision gates*) distinguish empirical held-out
thresholds from statistically controlled risk thresholds, which can lose
substantial coverage. An in-scope risk target does not by itself reject
out-of-scope inputs.

The resulting methodological recommendation is to record the probability object,
task mixture, aggregation, label prevalence and calibration split. Evaluate a
frozen threshold on disjoint data with both coverage and error. For expected-value
uses, check the full distribution: argmax accuracy cannot validate probability-
weighted scores or population estimates.

## Where the papers disagree

**Local speed versus system reliability.** Cao et al. 2026 (*SearchJev: A Fast and
Calibrated System-1 Model for Search Agents*) improve final answer accuracy and
active search time: on 100 BrowseComp-Plus questions, hybrids with SearchJev-4B
reach 54% versus 45% for System 2 alone and 46% for a Jev 1.13 hybrid, while
SearchJev-0.8B ties the Jev hybrid at lower time. The SearchJev runs record no
explicit short-decision fallback calls, so these gains do not isolate the
confidence gate. Duan et al. 2026 (*General Decision Models: Benchmarking and
Insights Beyond Jev*) lower τ-bench success and worsen tail latency after replacing
action selection, although median episode time falls. These are different
outcomes, but not matched replications: SearchJev is task-trained and embedded in
a search controller, whereas the τ-bench intervention uses general Jev while
another model generates arguments. Together they support measuring whole-
controller success, recovery and tail latency rather than extrapolating call speed.

**Useful confidence versus confident failure.** Li et al. 2026 (*JEV-as-a-Judge:
Accept When Confident, Escalate When Unsure*) find Jev within three points of GPT-6
as a standalone judge wherever the verdict can be read off the text, at 0.36% of
its fee, and a frozen cascade that beats GPT-6 by 0.9 points at 41% of its fee;
confidence routes most errors to the stronger judge. Xu et al. 2026 (*JevOut:
Natural Context Can Flip Decision Models*) obtain confident wrong answers through
adaptive context search. Useful ranking on ordinary examples does not imply
robustness to optimized inputs. JevOut's conditional search-success rate is not a
natural-traffic error rate; average calibration is not an invariance test. The
JEV-as-a-Judge results on style-adversarial pairs and reference-free prose expose a
related boundary using a different protocol.

**Reasoning versus benchmark success.** Deußer et al. 2026 (*Evaluating and
Benchmarking the System One Model Jev*) report unusually strong MMLU mathematics
and leave contamination unresolved. Duan et al. 2026 (*General Decision Models:
Benchmarking and Insights Beyond Jev*) construct numerical tasks where Jev often
gets near the answer but misses exact computation. Neither result refutes the
other: benchmark recognition, fresh computation and training exposure differ.
Direct readout and reasoning-enabled inference require explicit matched settings.

**Stable choices versus stable probabilities.** Imperatrice et al. 2026
(*Are AI Decision Models Biased? A Case Study of Jev*) find input manipulations
that move probabilities even when the chosen answer remains unchanged.
Sharma et al. 2026 (*TypedBench: A Benchmark for Calibration, Framing
Sensitivity, and Cost in System One Decision Models*) vary wording of the same
policy and observe large accuracy shifts. These are complementary to Xu et al.
2026 (*JevOut: Natural Context Can Flip Decision Models*): controlled behavioral
probes, generated paired stress tests and adaptive attacks have different
denominators and cannot be read as the same deployment failure rate.

## Evaluation protocols and comparative evidence

Deußer et al. 2026 (*Evaluating and Benchmarking the System One Model Jev*) use
exact option-logit probabilities for open baselines. Cao et al. 2026 (*SearchJev:
A Fast and Calibrated System-1 Model for Search Agents*) compare trained readouts
with autoregressive JSON baselines before task-specific training. Duan et al. 2026
(*General Decision Models: Benchmarking and Insights Beyond Jev*) include thinking
and non-thinking configurations and reasoning-to-readout self-distillation. Their
comparisons therefore answer different questions about interfaces, supervision
and compute; improvements should not all be attributed to a new architecture.

Li et al. 2026 (*JEV-as-a-Judge: Accept When Confident, Escalate When Unsure*)
separate post hoc sweeps, frozen held-out policies, live replication and prospective
testing. Strong savings on a favorable mixture shrink on harder new workloads,
yet the prospectively selected cascade still matches the fallback's accuracy at
75.5% of its fee.
Xu et al. 2026 (*JevOut: Natural Context Can Flip Decision Models*) make the
initially-correct denominator and accepted-query budget essential to robustness
interpretation. Neither an exploratory optimum nor a conditional attack rate is
an unconditional deployment estimate.

Rafe and Das 2026 (*Benchmarking System One decision models against trained
classifiers and language models for automated decision gates*) introduce an
application-relevant supervision comparison: when labels and a stable taxonomy
exist, a trained classifier can be preferable. Without labels, no open decision
model is significantly more accurate than Jev, while a large generative model
can match it at higher cost. This does not establish a
supervision-matched architectural advantage. Their offline cascade costs also
depend on utilization and composed latency rather than a live end-to-end run.
Sharma et al. 2026 (*TypedBench: A Benchmark for Calibration, Framing
Sensitivity, and Cost in System One Decision Models*) trade natural text for
derivable labels; fresh generation limits exact-item contamination while leaving
task-family familiarity relevant.

Zhu et al. 2026 (*Intern-Decision: Efficient Multimodal Decision Making with
Autoregressive Masked Language Modeling*) report a small paired distribution
pilot and one handoff point. Zhuang et al. 2026 (*StartLux-Decision: AutoThink
Decision Models with Reinforcement Learning for Calibrated Deliberative
Decisions*) disclose that public Decision Index guided development and identify
DecisionPivot as independent. Zhang et al. 2026 (*AnyJev Technical Report*)
explicitly exclude irregular benchmark items and separate disjoint threshold
verification from earlier same-sample experiments. These qualifications belong
beside their results, not just in a generic warning about preprints.

Useful comparisons preserve versions, prompts/options, splits, threshold selection,
metric definitions, hardware, batch size, input length and transport overhead.
Report per-task results alongside pooled averages; separate replay from live runs;
measure P95, retries and final success alongside median time. Filed PDFs and code
revisions are retained because these conditions change across releases.

## Open questions

Uncertainty and routing transfer across changed tasks, contexts and adversarial
inputs remain unresolved. Cao et al. 2026 (*SearchJev: A Fast and Calibrated
System-1 Model for Search Agents*), Li et al. 2026 (*JEV-as-a-Judge: Accept When
Confident, Escalate When Unsure*) and Xu et al. 2026 (*JevOut: Natural Context Can
Flip Decision Models*) expose OOD calibration, threshold-transfer and context-
sensitivity problems respectively. Duan et al. 2026 (*General Decision Models:
Benchmarking and Insights Beyond Jev*) leave open how much exact computation can
be distilled into one pass without inheriting teacher weaknesses.

The added evidence leaves three connected questions open: how much adaptation
transfers to unrepresented decision families; whether calibration and coherence
survive a changed wording, option set or routing policy; and whether local
readout savings remain useful after reasoning, rejection and fallback costs.
These require matched compute and supervision, independent policy selection, and
application-specific outcomes rather than a single leaderboard position.

The seven release sources add implementation and deployment diversity; they do
not settle these empirical questions. No included source establishes general
causal policy value, optimal action selection under an external utility, or regret
guarantees. Those topics require additional owner-selected literature and evidence.
