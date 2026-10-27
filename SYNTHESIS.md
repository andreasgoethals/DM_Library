# Decision models: cross-source synthesis

This selected corpus studies **fast decisions over supplied options**: a model
receives a state, one or more typed questions and a finite option set, and returns
a probability for each option instead of generating text. It contains sixteen
arXiv preprints and fifteen provider release posts, model cards or API references,
all dated September–October 2026. [SUMMARIES.md](SUMMARIES.md) records evidence
locations, limitations and Zotero citation keys; [DECISION_MODELS.md](DECISION_MODELS.md)
lists release dates, licenses, context limits and prices;
[REPOSITORIES.md](REPOSITORIES.md) maps official code snapshots. The corpus is not
a survey of classical decision theory, optimization or causal policy learning.

**Attribution convention.** "Reports", "finds" and "measures" introduce results
observed in a paper under its stated protocol. "States", "describes" and "claims"
introduce provider statements that no source in this library independently
verifies. *Interpretation* marks this synthesis's own reading. Numbers are taken
from the sources, not rerun here.

## TL;DR

- **What it is.** A decision model maps (state, instruction, supplied options) to
  a probability vector over those options, usually through choice, yes/no and
  ordinal-score primitives. The application supplies the options and decides what
  to execute; a valid typed answer is not necessarily a correct one.
- **How it differs from a chat LLM.** The same pretrained decoders are used, but
  output is a *restricted readout* rather than free generation: option-letter
  logits from the existing LM head, a learned pointer or marker head, or joint
  suffix likelihood. Some releases also change attention (bidirectional prompt
  attention), score several fields in one pass, or train specifically for
  calibration (proper-scoring losses, temperature fitting). See the
  [comparison table](#model-and-architecture-comparison).
- **Much of the capability is already in open LLMs.** Li and Wagle 2026
  (*LLM-as-Jev: LLMs Are Already Jev-Style Decision Models -- When and How to
  Fine-Tune Them*) and Geuter et al. 2026 (*Releasing the Inner Jev: A Simple
  Recipe for Open Decision Models*) report frozen open models, read at the answer
  position, within about 0.5–5 points of Jev on JevBench-style sets; short LoRA
  training closes or reverses the gap on represented task families. Zhang et al.
  2026 (*AnyJev Technical Report*) show that readout corrections alone change
  order sensitivity and cost without retraining.
- **Established by independent evaluation.** On bounded tasks whose evidence is in
  the input, the best decision models match fast general LLMs at a fraction of
  their latency and cost, with useful confidence rankings for selective
  prediction and cascades (Chen et al. 2026, *System1-Arena: Which Decisions Can
  Be Left to System 1?*; Li et al. 2026, *JEV-as-a-Judge: Accept When Confident,
  Escalate When Unsure*; Deußer et al. 2026, *Evaluating and Benchmarking the
  System One Model Jev*).
- **Also established, negatively.** They trail reasoning LLMs where the answer
  must be derived (computation, expert knowledge, forecasting); good local
  choices do not produce good closed-loop control; probabilities can be badly
  distorted, logically incoherent across question forms and costly to act on;
  and wording, option names, table layout or adversarially chosen context can
  flip confident answers. See [calibration](#calibration-has-several-meanings)
  and [robustness](#robustness-and-input-sensitivity).
- **Trained classifiers remain a strong baseline.** When labels and a stable
  taxonomy exist, a fine-tuned encoder was the most accurate system on most
  labelled tasks in the one study that tested this (Rafe and Das 2026,
  *Benchmarking System One decision models against trained classifiers and
  language models for automated decision gates*).
- **Provider claims dominate the release record.** Of fifteen web sources, none
  is an independent evaluation; benchmark wins, context limits and calibration
  statements in them are provider claims. Several research benchmarks are
  authored by teams whose own model leads them. See
  [which evidence to trust](#which-evidence-to-trust).
- **Open problems.** Calibration and threshold transfer under shift; coherence
  across question forms; robustness to natural and adversarial context;
  closed-loop reliability; matched-compute and matched-supervision comparisons;
  and whether one-pass savings survive reasoning, rejection and fallback costs.

## What a decision model is

The interface named by Almeida 2026 ([*Introducing System One Models & Jev*](SUMMARIES.md#web-qezz55x7))
and adopted across the corpus takes a **state** (text, JSON and, for some
releases, images or audio), one or more **questions** with a primitive type and
an explicit option set, and returns a probability per option. Choice selects
from an unordered set; yes/no returns one binary probability; score assigns mass
to ordered levels and may report their expected index. Expected rubric scores
are not economic utilities, and the model cannot choose an action that was not
offered.

The corpus documents five design levers that distinguish these systems from a
chat LLM. They are independent, so improvements from one should not be credited
to another (*interpretation*):

1. **Restricted readout.** Probabilities come from a constrained scoring step
   rather than generated text: legal option-letter logits from the unchanged LM
   head (Cao et al. 2026, *SearchJev: A Fast and Calibrated System-1 Model for
   Search Agents*; Duan et al. 2026, *General Decision Models: Benchmarking and
   Insights Beyond Jev*; Geuter et al. 2026, *Releasing the Inner Jev: A Simple
   Recipe for Open Decision Models*), a learned pointer or option-marker head
   (Kev, Strands Decider and Laya, as described by their releases and by Rafe and
   Das 2026, *Benchmarking System One decision models against trained
   classifiers and language models for automated decision gates*), masked answer
   placeholders (Intern-Decision, below) or joint likelihood of prefix-free
   candidate suffixes (Li and Wagle 2026, *LLM-as-Jev: LLMs Are Already Jev-Style
   Decision Models -- When and How to Fine-Tune Them*). Tev1 is an exception
   that still generates an answer letter.
2. **Attention changes.** Zhuang et al. 2026 (*StartLux-Decision: AutoThink
   Decision Models with Reinforcement Learning for Calibrated Deliberative
   Decisions*) remove the causal mask in full-attention layers of their Instant
   models and report gains of up to 2.4 Decision Index points at four of five
   scales in matched runs; they note that this prevents reusing a
   question-independent document encoding. The pplx-decider card describes
   noncausal full-attention layers as part of its inference contract.
3. **Multi-field single pass.** Zhu et al. 2026 (*Intern-Decision: Efficient
   Multimodal Decision Making with Autoregressive Masked Language Modeling*)
   read every schema field from one causal pass without feeding answers between
   fields. Clef, Decision 2.0 and hosted APIs describe several questions per
   request; whether those share one pass is a provider statement or undisclosed.
   StartLux instead scores questions as separate rows.
4. **Calibration training.** Proper-scoring losses (SearchJev's soft-target
   cross-entropy plus Brier; Clef's smoothed cross-entropy plus Brier, per its
   release post), RL against proper scores (RLCD² in StartLux; RLCD as described
   by Laya's developers and by the Jev launch post), self-distilled teacher
   distributions (SII-Decision) and post-hoc temperature scaling, which nearly
   every open release ships as a checkpoint-specific constant.
5. **Selective computation.** Direct readout can be followed by gated reasoning
   (StartLux AutoThink; GLiDE), option-rotation averaging (Zhang et al. 2026,
   *AnyJev Technical Report*) or escalation to a larger model (SearchJev; Li et
   al. 2026, *JEV-as-a-Judge: Accept When Confident, Escalate When Unsure*).
   These change cost and accuracy together and must be accounted per decision,
   not per call.

## Model and architecture comparison

Facts below come only from sources in this library; "n.d." means not disclosed
or not established by those sources. Release dates, licenses, prices and
context limits are maintained in [DECISION_MODELS.md](DECISION_MODELS.md) and
are not repeated. Evidence keys name the sources:
**[DB]** Deußer et al. 2026, [*Evaluating and Benchmarking the System One Model Jev*](SUMMARIES.md#deusser-benchmark);
**[BC]** Li, He and Li 2026, [*Beyond Calibration: Do a Typed-Decision Model's Probabilities Obey the Probability Axioms?*](SUMMARIES.md#beyond-calibration-do-a-typed-decision-model-s-probabilities-obey-the-probability-axioms);
**[AJ]** Zhang et al. 2026, [*AnyJev Technical Report*](SUMMARIES.md#anyjev-technical-report);
**[SJ]** Cao et al. 2026, [*SearchJev: A Fast and Calibrated System-1 Model for Search Agents*](SUMMARIES.md#searchjev);
**[RD]** Rafe and Das 2026, [*Benchmarking System One decision models against trained classifiers and language models for automated decision gates*](SUMMARIES.md#benchmarking-system-one-decision-models-against-trained-classifiers-and-language-models-for-automated-decision-gates);
**[TB]** Sharma et al. 2026, [*TypedBench: A Benchmark for Calibration, Framing Sensitivity, and Cost in System One Decision Models*](SUMMARIES.md#typedbench-a-benchmark-for-calibration-framing-sensitivity-and-cost-in-system-one-decision-models);
**[GDM]** Duan et al. 2026, [*General Decision Models: Benchmarking and Insights Beyond Jev*](SUMMARIES.md#general-decision-models);
**[SL]** Zhuang et al. 2026, [*StartLux-Decision: AutoThink Decision Models with Reinforcement Learning for Calibrated Deliberative Decisions*](SUMMARIES.md#startlux-decision-autothink-decision-models-with-reinforcement-learning-for-calibrated-deliberative-decisions);
**[IJ]** Geuter et al. 2026, [*Releasing the Inner Jev: A Simple Recipe for Open Decision Models*](SUMMARIES.md#releasing-the-inner-jev-a-simple-recipe-for-open-decision-models);
**[LJ]** Li and Wagle 2026, [*LLM-as-Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them*](SUMMARIES.md#llm-as-jev-llms-are-already-jev-style-decision-models-when-and-how-to-fine-tune-them);
**[ID]** Zhu et al. 2026, [*Intern-Decision: Efficient Multimodal Decision Making with Autoregressive Masked Language Modeling*](SUMMARIES.md#intern-decision-efficient-multimodal-decision-making-with-autoregressive-masked-language-modeling);
**[S1A]** Chen et al. 2026, [*System1-Arena: Which Decisions Can Be Left to System 1?*](SUMMARIES.md#system1-arena-which-decisions-can-be-left-to-system-1).
Provider records are linked by title in the first column; "card" denotes that record.

| Model (provider) | Backbone / size | Readout | Attention | Several fields in one pass? | Weights | Calibration method | Evidence type |
|---|---|---|---|---|---|---|---|
| Jev 1.13 (TypeSafe; [*Introducing System One Models & Jev*](SUMMARIES.md#web-qezz55x7)) | n.d. [RD] | n.d.; probabilities on a two-decimal grid [BC, RD] | n.d. | Launch post describes parallel outputs; bundling ten questions moved answers no more than repeating a request [BC] | Hosted only | Launch post describes RLCD; under-confident on TypedBench [TB] | Provider claim; independent black-box evaluations |
| Laya (Convai Innovations; no primary record in library) | ModernBERT-large 421M encoder; mmBERT-base 322M multilingual [RD, TB] | Option-marker scorer [RD] | Encoder | n.d. | Apache-2.0 [TB] | RLCD per its developers; per-question-type temperatures [RD, TB] | Third-party evaluations only |
| Kev family (Palmer; [*Kev-27B*](SUMMARIES.md#web-q9s5d6r2)) | Qwen3.5 0.8B/4B/9B + LoRA rank 16 [RD, TB]; 27B v2 fully fine-tuned Qwen3.8-27B torso (card) | Pointer head | Causal backbone; Qwen3.5 interleaves linear- and full-attention layers [TB] | n.d. | Open (card) | Stored temperatures 2.1–2.4 [RD, TB] | Model card; third-party evaluations |
| Tev1-4B-experimental (Together AI; [*Tev1-4B-experimental*](SUMMARIES.md#web-rgvmcn25)) | Qwen3.5-4B LoRA; 0.8B variant | Generates an answer letter through the ordinary LM head | Causal | No: one question, 2–24 options | Downloadable; weight license pending | n.d. | Model card |
| Intern-Decision 0.8B/2B/4B (InternLM; [*Intern-Decision-4B*](SUMMARIES.md#web-x58irxca)) | Qwen3.5; vision tower frozen [ID] | Native LM-head logit before each masked placeholder, restricted to legal symbols [ID] | Causal | **Yes**, no answers fed between fields [ID] | Open | Post-hoc temperature scaling [ID] | Paper + card |
| SearchJev 0.8B/4B (research) | Qwen3.5 + LoRA [SJ] | Single-token option labels via existing LM head [SJ] | Causal | n.d. | Code snapshot; weight release not established | Soft-target cross-entropy + Brier; held-out temperature per output type [SJ] | Paper |
| SII-Decision 4B/27B (research) | Qwen3.5-4B / Qwen3.8-27B [GDM] | Backbone's single-token label readout [GDM] | Causal | n.d. | Open [GDM] | Reasoning-to-readout self-distillation with KL anchor; no gold labels [GDM] | Paper (authors' own benchmark) |
| StartLux-Decision Instant / AutoThink 4B/9B/27B (research) | Qwen3.5 / Qwen3.8 [SL] | Option letter at final prompt position; ≤26 options, grouping beyond [SL] | Instant: bidirectional in full-attention layers; AutoThink: causal, gated reasoning [SL] | No: questions scored independently [SL] | Open [SL] | RLCD² decision-weighted proper-score reward; policy-aware calibration [SL] | Paper |
| Jeff 1.0 (research) | Gemma 4 12B/31B, Qwen3.5-4B, Qwen3.6-27B [IJ] | Head initialized from answer-letter LM-head rows + LoRA [IJ] | Causal | n.d. | Non-commercial weights | Temperature scaling [IJ] | Paper |
| AnyJev (readout recipe) | Any frozen open LLM [AJ] | Restricted label logits, label-prior division, cyclic option rotations [AJ] | Unchanged | No: one prefill per rotation [AJ] | Code only; no new weights | Separately fitted temperature [AJ] | Paper |
| LLM-as-Jev (readout + fine-tuning recipe) | Qwen3.5-4B, Qwen3-0.6B [LJ] | Joint likelihood of prefix-free numeric suffixes [LJ] | Unchanged | No | No verified code | KL-anchored listwise LoRA [LJ] | Paper |
| Clef / Clef-flash (Cloudflare; [*Introducing Clef: our open-source decision models, and new RL fine-tuning platform*](SUMMARIES.md#web-mwjhy75j)) | Qwen backbones, nominal 27B / 9B | Joint-schema head with option-specific evidence routing | Cross-field attention in head | Yes (provider) | Open | Smoothed cross-entropy + Brier; later RL objective | Provider claim + inference code |
| Strands Decider 2B ([*Introducing Strands Decider 2B: a small, open source, decision model*](SUMMARIES.md#web-gi68ips2)) | Qwen3.5-2B torso | Pointer head (an earlier slot-head alternative was removed upstream in October) | Causal | n.d. | Open | Temperature fitted per question kind (code) | Provider claim + training code |
| Decision 2.0 family (vLLM Semantic Router; [*Decision-2.0-Vega-27B*](SUMMARIES.md#web-bh58bep7)) | Size labels 0.6B–27B; Vega 29.37B actual | Candidate readout | n.d. | Yes: simultaneous choice, yes/no and score (card) | Open | n.d. | Model card + code |
| pplx-decider-v1.1-27b (Perplexity; [*pplx-decider-v1.1-27b*](SUMMARIES.md#web-de9kqqlx)) | Nominal 27B | Separate decision readout | Noncausal full-attention layers (card; also noted in [SL]) | n.d. | Open | One saved temperature | Model card + code |
| H2O-Lightning-4B ([*H2O-Lightning-4B*](SUMMARIES.md#web-skwpxqtg)) | Qwen3.5-4B | Serving shim over choice, yes/no and score | One-way or two-way reading mode | n.d. | Open | Saved calibration plus yes/no adjustment | Model card + code |
| d1-3B / d1-omni-600M (Liquid AI; [*Open d1: Edge decision models for text, vision, and audio*](SUMMARIES.md#web-4u52t7rc)) | Distinct backbones; omni is a 587M encoder | Decision head | Omni: encoder | n.d. | Downloadable, commercial-use condition | n.d. | Provider claim + inference code |
| Microsoft-Decision-1 ([*Introducing Microsoft-Decision-1, our model for fast decision-making*](SUMMARIES.md#web-lelm4ubr)) | Qwen3.5-9B post-trained | Single-pass option probabilities | n.d. | n.d. | Hosted only | n.d. (provider reports calibration) | Provider claim; evaluated in [S1A] |
| GLiDE (Fastino; [*Introducing GLiDE: The First Thinking Decision Model*](SUMMARIES.md#web-msejsvgw)) | Unconfirmed | Direct option scoring, extra reasoning when uncertain | n.d. | Several questions; usage counts internal passes | Hosted only | n.d. | Provider claim |
| Solar Decide (Upstage; [*Solar Decide*](SUMMARIES.md#web-qzkmbk7l)) | Built on Solar Mini 4 | n.d. | n.d. | n.d. | Hosted beta | n.d. | Provider claim |
| Mercury Decide (Inception; [*Mercury Decide: Create a decision*](SUMMARIES.md#web-ps2pzgda)) | n.d. | n.d. | n.d. | Shared state, named questions | Hosted only | n.d. | Provider API reference |
| Decisions API, GPT-6 Luna (OpenAI; [*Build more responsive apps with the Decisions API*](SUMMARIES.md#web-q9x2h26h)) | n.d. | n.d. | n.d. | Up to 400 questions per request; pass structure n.d. | Hosted only | n.d. | Provider claim; evaluated in [S1A] |

*Interpretation:* the open releases converge on a Qwen-family decoder with a
restricted readout and a stored temperature; they differ mainly in head design,
attention mask, how questions share a pass and how much task-family data they
saw. None of the hosted systems discloses architecture, so differences between
hosted and open models cannot be attributed to any of the five levers.

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
| 2026-10 | Geuter et al. 2026 — [Releasing the Inner Jev: A Simple Recipe for Open Decision Models](SUMMARIES.md#releasing-the-inner-jev-a-simple-recipe-for-open-decision-models) | Answer-letter readout and short LoRA training yield competitive open decisions on OpenDecisions and JevBench. | Frozen instruction-tuned LMs, temperature calibration and supervised LoRA |
| 2026-10 | Li and Wagle (2026), [LLM-as-Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them](SUMMARIES.md#llm-as-jev-llms-are-already-jev-style-decision-models-when-and-how-to-fine-tune-them) | Prefix-free candidate scoring tests when frozen LLMs suffice and when anchored fine-tuning or bounded reasoning helps. | Joint candidate likelihood, constrained readout and KL-regularized adaptation |
| 2026-10 | Imperatrice et al. (2026), [Are AI Decision Models Biased? A Case Study of Jev](SUMMARIES.md#are-ai-decision-models-biased-a-case-study-of-jev) | Behavioral tasks distinguish selected answers from probability shifts under irrelevant context, framing and option order. | Cognitive-bias paradigms and controlled input variation |
| 2026-10 | Zhang et al. 2026 — [Typed Decision Models on Tabular Data](SUMMARIES.md#typed-decision-models-on-tabular-data) | Four decision models and three LLMs separate option-format robustness from table-serialization robustness. | Semantic-preserving rewrites of tabular decisions and selective re-querying |
| 2026-10 | Zhu et al. (2026), [Intern-Decision: Efficient Multimodal Decision Making with Autoregressive Masked Language Modeling](SUMMARIES.md#intern-decision-efficient-multimodal-decision-making-with-autoregressive-masked-language-modeling) | Multimodal masked decision training scores multiple fields in one causal pass, with separate calibration and handoff evaluations. | Native LM-head scoring, multimodal inputs and post-hoc calibration |
| 2026-10 | Chen et al. 2026 — [System1-Arena: Which Decisions Can Be Left to System 1?](SUMMARIES.md#system1-arena-which-decisions-can-be-left-to-system-1) | Shared probability-scoring requests separate strong static decisions from weak closed-loop control across 30 models. | Typed decisions, broad benchmarks and latency-aware closed-loop evaluation |

## Web-source timeline

These fifteen selected records have no PDFs. Verified announcement dates and
year-only undated cards are distinguished in the [web registry](papers/web_sources.json).
A checkpoint upload is not automatically a public release. Source dates and
current model specifications are separate; see [DECISION_MODELS.md](DECISION_MODELS.md).

| Date | Source | Role |
|---|---|---|
| 2026 | H2O.ai 2026 — [H2O-Lightning-4B](SUMMARIES.md#web-skwpxqtg) | Open-weight probability readout with a concrete serving contract |
| 2026 | Inception 2026 — [Mercury Decide: Create a decision](SUMMARIES.md#web-ps2pzgda) | Hosted decision contract and modality/request-size boundaries |
| 2026-09-15 | Almeida 2026 — [Introducing System One Models & Jev](SUMMARIES.md#web-qezz55x7) | Provider interface and motivation |
| 2026-09-22 | Upstage 2026 — [Solar Decide](SUMMARIES.md#web-qzkmbk7l) | Hosted long-context typed scoring and Korean-language deployment |
| 2026-09-23 | Together AI 2026 — [Tev1-4B-experimental](SUMMARIES.md#web-rgvmcn25) | Native answer-token readout and reproducible adaptation recipe |
| 2026-09-26 | InternLM 2026 — [Intern-Decision-4B](SUMMARIES.md#web-x58irxca) | Multi-field readout and calibration; 26 September upload and public demo |
| 2026-09-30 | Sahibzada Allahyar, Mary Newhauser 2026 — [Introducing GLiDE: The First Thinking Decision Model](SUMMARIES.md#web-msejsvgw) | Variable inference effort behind a typed decision interface |
| 2026-09-30 | Jared Palmer 2026 — [Kev-27B](SUMMARIES.md#web-q9s5d6r2) | Open-source candidate readout, adaptation and context validation |
| 2026-10-01 | Chen et al. 2026 — [Introducing Clef: our open-source decision models, and new RL fine-tuning platform](SUMMARIES.md#web-mwjhy75j) | Open architecture and adaptation |
| 2026-10-01 | Brooker et al. 2026 — [Introducing Strands Decider 2B: a small, open source, decision model](SUMMARIES.md#web-gi68ips2) | Local model and public development materials |
| 2026-10-03 | vLLM Semantic Router Team 2026 — [Decision-2.0-Vega-27B](SUMMARIES.md#web-bh58bep7) | Serving-integrated open decision models across several model sizes |
| 2026-10-06 | Perplexity AI 2026 — [pplx-decider-v1.1-27b](SUMMARIES.md#web-de9kqqlx) | Checkpoint-specific inference contract; public announcement |
| 2026-10-07 | Liquid AI 2026 — [Open d1: Edge decision models for text, vision, and audio](SUMMARIES.md#web-4u52t7rc) | Edge and modality expansion |
| 2026-10-09 | Srivastava 2026 — [Introducing Microsoft-Decision-1, our model for fast decision-making](SUMMARIES.md#web-lelm4ubr) | Hosted release and provider evaluation |
| 2026-10-22 | OpenAI 2026 — [Build more responsive apps with the Decisions API](SUMMARIES.md#web-q9x2h26h) | Hosted typed decisions, shared-input caching and explicit endpoint billing |

## Decisions and available information

Deußer et al. 2026 (*Evaluating and Benchmarking the System One Model Jev*) and
Duan et al. 2026 (*General Decision Models: Benchmarking and Insights Beyond Jev*)
evaluate mappings from state, instruction and finite options to probabilities.
The application supplies the candidates; the model neither discovers a feasible
set nor shows that all useful actions were offered.

Cao et al. 2026 (*SearchJev: A Fast and Calibrated System-1 Model for Search
Agents*) make the controller explicit: bounded relevance, sufficiency and
verification judgments guide search while a larger model generates queries and
answers. Li et al. 2026 (*JEV-as-a-Judge: Accept When Confident, Escalate When
Unsure*) decide whether to accept a cheap verdict or pay for a fallback; their
threshold rules minimize expense under an empirical accuracy tolerance, not an
optimum under arbitrary error costs. Xu et al. 2026 (*JevOut: Natural Context Can
Flip Decision Models*) show that answer-preserving context can redirect selection:
a schema constrains output form, not interpretation of the evidence.

| Axis | Supported by the corpus | Not established by the corpus |
|---|---|---|
| Objective | Accuracy, probability quality, selective risk, fees, latency | A shared utility function across studies |
| Decision variables | Labels, rubric levels, tool choices, escalation | General continuous or combinatorial optimization |
| Constraints | Schemas, input limits, controller rules, empirical tolerances | Guaranteed real-world constraint satisfaction |
| Uncertainty | Top-label confidence, binary and full distributions, analytic probes | Universal calibration under shift |
| Information | Text, evidence, history and some multimodal inputs | Sufficient state for an underlying environment |
| Sequential behavior | Search and tool-agent experiments, closed-loop environments | Optimal-policy or cumulative-regret guarantees |
| Causal assumptions | Controlled component comparisons within harnesses | Identification of counterfactual policy value |
| Cost | Measured fees and runtime under stated protocols | Hardware-independent efficiency rankings |

## Readout, adaptation and selective computation

**Readout alone recovers much capability.** Zhang et al. 2026 (*AnyJev Technical
Report*) average option rotations and divide out a label prior estimated without
gold labels; adaptive stopping reads 7.3 of 18 rotations and serves 2.22× as many
decisions per second on vLLM, but the disjoint selection/verification analysis
that supports a reliable bound reads 10.6. Li and Wagle 2026 (*LLM-as-Jev: LLMs
Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them*) score
prefix-free numeric suffixes jointly: frozen Qwen3.5-4B reaches 81.4% on the 231
public JevBench items (Jev 1.13.0: 86.6% in the same table), beats isolated
scoring on the same backbone (81.4% versus 76.2%) and reaches 94.8% with
budgeted native thinking, matching GPT-5.6 Sol. Geuter et al. 2026 (*Releasing
the Inner Jev: A Simple Recipe for Open Decision Models*) report zero-shot Gemma 4
31B at 79.6 Capability on their OpenDecisions set against Jev's 80.1. Computation
differs across these procedures: one prefill per rotation, extra suffix steps or
a reasoning trace are not one forward pass, and none creates new knowledge.

**Adaptation helps where the task family is represented.** Geuter et al. find
that head-only training adds little while short LoRA training lifts Gemma 4 31B
to 84.4 on OpenDecisions and 81.5 on the JevBench v1.7 leaderboard. Li and
Wagle's gains concentrate in represented domains (the 0.6B model's Banking77
accuracy rises from 22.2% to 60.5%), and training only on intents without
anchors lowers JevBench accuracy from 81.4% to 74.9%. Zhuang et al. 2026
(*StartLux-Decision: AutoThink Decision Models with Reinforcement Learning for
Calibrated Deliberative Decisions*) report that added training families improve
the corresponding tasks of DecisionPivot's reused-task track by 8.6 points,
against 0.3 points on tasks outside those families.
Duan et al. 2026 (*General Decision Models: Benchmarking and Insights Beyond
Jev*) self-distil reasoning into a readout: SII-Decision-27B slightly exceeds
Jev on JEVal (79.24 versus 78.38) with the lowest ECE there (0.0149).

**Architecture and inference effort are separate levers.** Zhu et al. 2026
(*Intern-Decision: Efficient Multimodal Decision Making with Autoregressive
Masked Language Modeling*) read several schema fields in one causal pass.
StartLux's Instant models change the attention mask, while AutoThink reasons up
to 4,096 tokens only when top probability is below 0.9; on DecisionPivot it gains
11.5–18.4 pair-accuracy points over Instant (86.9% at 27B), and RLCD² cuts mean
reasoning length by up to 65%. Restrictive reasoning budgets lower accuracy on
the longest computations. *Interpretation:* supervision, temperature scaling,
attention changes, reasoning budgets and backbone choice should each be
reported separately; none of these papers isolates "the typed interface" as the
cause of a gain.

## Calibration has several meanings

**Marginal calibration can look good while the distribution is wrong.**
Deußer et al. 2026 (*Evaluating and Benchmarking the System One Model Jev*) find
pooled Choice ECE of 0.028 but a mean per-dataset ECE of 0.061, under-confident
yes/no probabilities and over-predicting multi-label fan-out; thresholds fitted
on separate data raise UNFAIR-ToS micro-F1 from 0.499 to 0.748. Duan et al. 2026
(*General Decision Models: Benchmarking and Insights Beyond Jev*) show Jev
selecting the prior mode on every analytic item while assigning it 89.35% on
average when the true value is 35.60%. Confidence that a selected label is
correct across a task distribution differs from recovering each problem's
distribution.

**Calibration under shift and after selection.** Cao et al. 2026 (*SearchJev: A
Fast and Calibrated System-1 Model for Search Agents*) train against soft targets
with proper-scoring losses; held-out families keep accuracy while calibration
worsens (Table 5). Zhuang et al. 2026 (*StartLux-Decision: AutoThink Decision
Models with Reinforcement Learning for Calibrated Deliberative Decisions*) show
that selection and routing shift confidence–accuracy gaps, and policy-aware
calibration narrows them from [−11.7, +20.5] to [−2.7, +2.1] points while still
leaving up to 6.1 points of overconfidence on unseen datasets. Li et al. 2026
(*JEV-as-a-Judge: Accept When Confident, Escalate When Unsure*) therefore
validate the acceptance rule per workload rather than treating one ECE as a
deployment certificate.

**Calibration is not decision value or coherence.** Sharma et al. 2026
(*TypedBench: A Benchmark for Calibration, Framing Sensitivity, and Cost in System
One Decision Models*) compare ECE with a finite-sample null and find almost every
model and question above it; Jev is systematically under-confident yet ranks its
own errors best, while acting on its probabilities under a 2:1 cost costs 2,300
versus 1,080 per 10⁴ decisions for its top answer. Li, He and Li 2026 (*Beyond
Calibration: Do a Typed-Decision Model's Probabilities Obey the Probability
Axioms?*) find mean negation violation of 0.064 for Jev (about five times its
repeat-noise floor), 0.293 for first-token Qwen3.8-27B and 0.122 for its
verbalized probabilities; Jev's three single-label yes/no probabilities sum to
about 1.14. Rafe and Das 2026 (*Benchmarking System One decision models against
trained classifiers and language models for automated decision gates*) show that
a statistically guaranteed 5% risk leaves Jev only 0.528 coverage, and that an
in-scope risk target does not reject out-of-scope inputs.

*Interpretation:* record the probability object, task mixture, aggregation,
label prevalence and calibration split. Evaluate frozen thresholds on disjoint
data with coverage and error. For expected-value uses, test the full distribution
and its coherence across question forms; argmax accuracy cannot validate
probability-weighted scores or population estimates.

## Robustness and input sensitivity

The corpus separates four kinds of perturbation whose denominators differ and
which must not be pooled into one failure rate:

- **Adaptive context search.** Xu et al. 2026 (*JevOut: Natural Context Can Flip
  Decision Models*) flip 61.4% of Jev's 508 initially correct decisions under a
  64-call budget, and 45.5% of those held at gold probability ≥ 0.9; independent
  target-aware generation alone reaches 48.0%. These are conditional search
  successes, not natural error rates; 91.6% of 250 sampled successes passed a
  blinded validity audit.
- **Controlled behavioral probes.** Imperatrice et al. 2026 (*Are AI Decision
  Models Biased? A Case Study of Jev*) find choices largely free of classic human
  biases, but probabilities that move under irrelevant anchors, loss framing and
  option order; an edited conjunction item is answered wrongly in all 500
  responses at about 95% confidence.
- **Rewording and option naming.** Sharma et al. 2026 (*TypedBench: A Benchmark
  for Calibration, Framing Sensitivity, and Cost in System One Decision Models*)
  report that restating the same ticket-priority policy moves Jev accuracy by 24
  points. Rafe and Das 2026 (*Benchmarking System One decision models against
  trained classifiers and language models for automated decision gates*) find
  that swapping yes and no flips 50.5 answers per hundred for Jev and at least
  16.8 for every generative model, against at most 6.5 for four fine-tuned
  decision checkpoints.
- **Representation of structured inputs.** Zhang et al. 2026 (*Typed Decision
  Models on Tabular Data*) find three decision models relatively stable to option
  rewrites, while all seven evaluated systems remain sensitive to table format or
  ordering; every model changes at least a third of row decisions under some
  rewrite despite stable aggregate accuracy. Low-confidence rows are the most
  likely to change, so selective re-querying recovers much of full re-querying,
  but stable confident errors remain.

The provider record *Introducing Microsoft-Decision-1, our model for fast
decision-making* reports perturbation tests with a different protocol; a low
average flip rate there does not rebut adaptive-search results.

## Where the evidence conflicts

**Local speed versus system reliability.** Cao et al. 2026 (*SearchJev: A Fast
and Calibrated System-1 Model for Search Agents*) report that on 100
BrowseComp-Plus questions, hybrids with SearchJev-4B reach 54% versus 45% for
System 2 alone and 46% for a Jev 1.13 hybrid, at far lower active time. The
SearchJev runs record no explicit short-decision fallback calls, so the gain does
not isolate the confidence gate. Duan et al. 2026 (*General Decision Models:
Benchmarking and Insights Beyond Jev*) replace τ-bench action selection with Jev:
success falls from 77.6% to 66.1% and P95 time rises, although median time falls.
Chen et al. 2026 (*System1-Arena: Which Decisions Can Be Left to System 1?*) find
nine models within 67.4–71.3% single-step accuracy whose closed-loop success
ranges from 5.7% to 32.9%. *Interpretation:* these are not matched replications
(task-trained component in a search controller versus general model in a tool
agent), but together they require whole-controller success, recovery and tail
latency rather than extrapolation from call speed.

**Useful confidence versus confident failure.** Li et al. 2026 (*JEV-as-a-Judge:
Accept When Confident, Escalate When Unsure*) find Jev within three points of
GPT-6 wherever the verdict can be read off the text, at 0.36% of its fee, and a
frozen cascade that beats GPT-6 by 0.9 points at 41.4% of its fee. Xu et al. 2026
(*JevOut: Natural Context Can Flip Decision Models*) obtain confident wrong
answers by adaptive search. Useful ranking on ordinary traffic does not imply
robustness to optimized inputs, and JEV-as-a-Judge itself reports weaker routing
on style-adversarial pairs and reference-free prose.

**Benchmark strength versus fresh computation.** Deußer et al. 2026 (*Evaluating
and Benchmarking the System One Model Jev*) report unusually strong MMLU
mathematics and leave contamination unresolved; Duan et al. construct numerical
tasks where Jev gets near but misses exact computation. Neither refutes the
other: recognition, computation and training exposure differ.

**Who leads overall.** Duan et al. place their SII-Decision-27B above Jev on
JEVal; Geuter et al. 2026 (*Releasing the Inner Jev: A Simple Recipe for Open
Decision Models*) place Jeff above Jev on OpenDecisions and the JevBench
leaderboard; Zhuang et al. 2026 (*StartLux-Decision: AutoThink Decision Models
with Reinforcement Learning for Calibrated Deliberative Decisions*) place
StartLux 27B Instant at 75.4% DecisionPivot pair accuracy against 31.0% for
hosted Jev; Chen et al. find Decision-2.0-Vega-27B
and Jev with the best System-1 Brier scores. *Interpretation:* each ranking is on
a benchmark built or selected by the winning team, or with different protocols,
so no overall ordering follows. See [which evidence to trust](#which-evidence-to-trust).

## Which evidence to trust

Evidence types, from strongest to weakest for a general claim
(*interpretation*): (1) pre-registered or frozen protocols evaluated
prospectively on new data; (2) third-party evaluations with released requests
and responses; (3) authors' benchmarks that are not used for development;
(4) public leaderboards used during development; (5) provider posts and cards.
The table lists the benchmarks and indices in the corpus with their
denominators and the conflicts that limit them.

| Benchmark or index | Scope and denominator | Conflict or limitation |
|---|---|---|
| JevBench public subset | 231 items, 2–6 options (mean 3.6), per Zhang et al. 2026 (*AnyJev Technical Report*) | One system's Capability has a bootstrap SD of about 3 points (Geuter et al. 2026, *Releasing the Inner Jev: A Simple Recipe for Open Decision Models*); widely used for development and checkpoint selection |
| JevBench leaderboard | Hidden set; Jeff measured on 1,500 items, each system on its own draw (Geuter et al.) | Scores yes/no answers with 0.2 < P(yes) < 0.8 as wrong abstentions; Jeff's submission moved such answers out of the band. Papers attribute maintenance inconsistently |
| Decision Index | Community leaderboard: 70 open models plus Jev, 120,340 frozen requests from 38 benchmarks, native prompts (Rafe and Das 2026, *Benchmarking System One decision models against trained classifiers and language models for automated decision gates*) | Public part guided StartLux development (Zhuang et al. 2026, *StartLux-Decision: AutoThink Decision Models with Reinforcement Learning for Calibrated Deliberative Decisions*) and is cited in provider cards; no per-item answers released |
| DecisionPivot | 13 generated families × 600 items, mostly contrast pairs; 34,104-item reused-task track (Zhuang et al.) | Introduced by the StartLux authors; independent of their development choices, not of their team |
| OpenDecisions | 2,352 questions, eleven families, 23 languages, built to mirror JevBench composition (Geuter et al.) | Authors' own validation set; includes synthetic and model-labelled items; Capability is a composite |
| JEVal | 11,257 bilingual instances from 36 datasets (Duan et al. 2026, *General Decision Models: Benchmarking and Insights Beyond Jev*) | Authors' own benchmark, on which their model leads |
| SearchDecision-Bench | Search routing, relevance, sufficiency, navigation and verification (Cao et al. 2026, *SearchJev: A Fast and Calibrated System-1 Model for Search Agents*) | Authors' own, task-specific; end-to-end test is one run on 100 questions |
| TypedBench | Seven rule-based generators, nine suites; null-ECE reference and cost matrices (Sharma et al. 2026, *TypedBench: A Benchmark for Calibration, Framing Sensitivity, and Cost in System One Decision Models*) | Evaluates others' models; templated inputs trade naturalness for derivable labels |
| System1-Arena | 92,125 questions, 105 tasks, 268 sources; 138 environments, 127 in the headline loop table; 30 models (Chen et al. 2026, *System1-Arena: Which Decisions Can Be Left to System 1?*) | Evaluates others' models; one draw per request, inherited label noise, changing hosted APIs |
| Deußer harness | 37 datasets, 346,009 Jev requests, frozen templates, released raw responses (Deußer et al. 2026, *Evaluating and Benchmarking the System One Model Jev*) | Single hosted version; open baselines without reasoning; no run-to-run variance |
| JevOut flips | Initially correct items per model, 64 accepted calls per decision (Xu et al. 2026, *JevOut: Natural Context Can Flip Decision Models*) | Different populations per model, so not a leaderboard |
| Provider benchmarks | Release posts and cards (for example *Kev-27B*, *Introducing Strands Decider 2B: a small, open source, decision model*, *pplx-decider-v1.1-27b*) | Provider-run; the Kev card acknowledges checkpoint selection after test results; Strands tuned iteratively against a public benchmark |

**Protocol checklist.** Compare systems on identical requests with pinned model,
checkpoint and runtime revisions, the full option wording and order, and stated
temperature and yes/no adjustments. Prefer exact option-logit probabilities for
open baselines (as Deußer et al. do) over verbalized JSON confidences. Report
per-task results beside pooled scores, uncertainty intervals, the denominator of
any robustness rate, and whether thresholds were chosen on the test data. Li et
al. 2026 (*JEV-as-a-Judge: Accept When Confident, Escalate When Unsure*) are the
corpus model for this: post hoc sweeps, frozen held-out policies, live
replication and prospective workload testing are reported separately, and their
favorable savings shrink to 75.5% of fallback cost prospectively. For cost,
count internal passes, reasoning, rotations, cache operations, retries and
escalation, and record hardware, batch size and transport; measure P95 and final
success as well as median latency.

## When to use a decision model, an LLM or a trained classifier

This guidance is *interpretation* grounded in the cited results; each row names
the evidence and its limits.

| Situation | Better default | Evidence |
|---|---|---|
| Stable taxonomy with labelled training data | Fine-tuned classifier | Rafe and Das 2026 (*Benchmarking System One decision models against trained classifiers and language models for automated decision gates*): DeBERTa-v3-large most accurate on every labelled task but one. Sharma et al. 2026 (*TypedBench: A Benchmark for Calibration, Framing Sensitivity, and Cost in System One Decision Models*): per-question DistilBERT reaches 1.000 on a rule-derived priority task. Not a supervision-matched architecture test |
| No labels, evidence in the input, bounded options, high volume or tight latency | Decision model | Duan et al. 2026 (*General Decision Models: Benchmarking and Insights Beyond Jev*): decision models lead on long-context and document tasks. Chen et al. 2026 (*System1-Arena: Which Decisions Can Be Left to System 1?*): best System-1 models match fast closed LLMs on static accuracy with better Brier scores at about one-quarter of the latency. Zhang et al. 2026 (*Typed Decision Models on Tabular Data*): comparable accuracy at lower cost |
| Answer must be derived: computation, code, expert knowledge, forecasting | Reasoning LLM, or a decision model with gated reasoning | Li et al. 2026 (*JEV-as-a-Judge: Accept When Confident, Escalate When Unsure*): Jev trails GPT-6 by 7–28 points on derived verdicts. Duan et al.: 3–6 points behind in medicine, finance and law. Chen et al.: reasoning LLM most accurate at about 70× a fast LLM's cost. Zhuang et al. 2026 (*StartLux-Decision: AutoThink Decision Models with Reinforcement Learning for Calibrated Deliberative Decisions*) and Li and Wagle 2026 (*LLM-as-Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them*): reasoning lifts decision accuracy substantially |
| Mixed easy and hard traffic | Confidence cascade with a threshold frozen on separate data | Li et al.: frozen and prospective cascades match or beat the fallback at lower cost. Rafe and Das: an intent-trained first stage escalating to Gemma-4-31B matches Gemma at about Jev's price. Zhu et al. 2026 (*Intern-Decision: Efficient Multimodal Decision Making with Autoregressive Masked Language Modeling*): one handoff point is two items worse than the large model but faster. Sharma et al.: uncertain answers can be spread across nearly all requests, so per-answer savings may not become per-request savings |
| Multi-step or closed-loop control | Planner LLM; decision model only for bounded sub-judgments | Duan et al.: τ-bench success falls from 77.6% to 66.1% with Jev choosing actions. Chen et al.: small System-1 models rarely succeed in closed loops (at most 3.1%). Cao et al. 2026 (*SearchJev: A Fast and Calibrated System-1 Model for Search Agents*): gains come from a hybrid that keeps a larger planner |
| An open LLM is already deployed, or weights must be controlled | Frozen restricted readout first, then anchored LoRA on represented families | Li and Wagle; Geuter et al. 2026 (*Releasing the Inner Jev: A Simple Recipe for Open Decision Models*); Zhang et al. 2026 (*AnyJev Technical Report*). Check transfer outside trained families and general-behavior drift |
| Probabilities feed expected values, costs or combined beliefs | Validate the full distribution before use, whatever the model | Duan et al.: distorted analytic distributions. Li, He and Li 2026 (*Beyond Calibration: Do a Typed-Decision Model's Probabilities Obey the Probability Axioms?*): incoherence across question forms. Sharma et al.: acting on probabilities can double cost |
| Out-of-scope inputs are likely | Explicit out-of-scope option plus separately validated rejection | Rafe and Das: an explicit option cuts accepted out-of-scope inputs from 0.310 to 0.195. Sharma et al.: Jev abstains on only about half of out-of-scope items |
| Inputs are user-controlled or adversarial | Treat confidence as attackable; add input controls and audits | Xu et al. 2026 (*JevOut: Natural Context Can Flip Decision Models*) |

## Released model contracts and deployment cost

The fifteen release records widen deployment choices without making interfaces
equivalent. Together AI 2026 (*Tev1-4B-experimental*) generates an answer letter
through an ordinary LM head; OpenAI 2026 (*Build more responsive apps with the
Decisions API*), Upstage 2026 (*Solar Decide*) and Inception 2026 (*Mercury
Decide: Create a decision*) specify hosted typed endpoints whose architecture is
undisclosed. Their common routing use does not establish identical probability
semantics, multi-question execution or billing.

H2O.ai 2026 (*H2O-Lightning-4B*), Palmer 2026 (*Kev-27B*), Perplexity AI 2026
(*pplx-decider-v1.1-27b*) and vLLM Semantic Router Team 2026
(*Decision-2.0-Vega-27B*) expose readout and serving artifacts. Attention masks,
truncation, temperature and yes/no adjustments belong to the evaluated model
contract; the pplx-decider card names changing the mask, swapping the head and
applying temperature twice as reproduction hazards. Size labels, configured
position limits, validated state lengths and deployed request limits measure
different things.

Allahyar and Newhauser 2026 (*Introducing GLiDE: The First Thinking Decision
Model*) make extra reasoning conditional on uncertainty, and current
documentation supersedes the announcement's older context limit. A fair cost
comparison counts internal passes, repeated state, schema overhead, cache
operations and any fallback. Public weights, permissive code and an unrestricted
weight license are separate properties: Tev1's pending weight license, the
commercial-use condition in Liquid AI 2026 (*Open d1: Edge decision models for
text, vision, and audio*) and the non-commercial Jeff weights from Geuter et al.
2026 (*Releasing the Inner Jev: A Simple Recipe for Open Decision Models*) cannot be inferred
from base-model or serving-code licenses. [DECISION_MODELS.md](DECISION_MODELS.md)
records the specifics.

## Open questions

- **Transfer.** How far do calibration, thresholds and routing transfer across
  changed tasks, contexts and fallback models? Cao et al. 2026 (*SearchJev: A
  Fast and Calibrated System-1 Model for Search Agents*), Li et al. 2026
  (*JEV-as-a-Judge: Accept When Confident, Escalate When Unsure*) and Zhuang et
  al. 2026 (*StartLux-Decision: AutoThink Decision Models with Reinforcement
  Learning for Calibrated Deliberative Decisions*) all show degradation under
  shift.
- **Coherence.** Can one model return probabilities that remain consistent across
  yes/no, choice and negated forms (Li, He and Li 2026, *Beyond Calibration: Do a
  Typed-Decision Model's Probabilities Obey the Probability Axioms?*)?
- **Robustness.** Which training or inference procedures reduce adaptive context
  flips (Xu et al. 2026, *JevOut: Natural Context Can Flip Decision Models*) and
  representation sensitivity (Zhang et al. 2026, *Typed Decision Models on
  Tabular Data*) rather than only average wording effects?
- **Distillation limits.** How much exact computation can be distilled into one
  pass without inheriting teacher weaknesses (Duan et al. 2026, *General Decision
  Models: Benchmarking and Insights Beyond Jev*)?
- **Closed loops.** What makes strong step-level decisions produce closed-loop
  success (Chen et al. 2026, *System1-Arena: Which Decisions Can Be Left to
  System 1?*)?
- **Fair comparison.** Matched supervision and compute between decision models,
  prompted LLMs and trained classifiers; independent benchmarks not used for
  development; and end-to-end costs including reasoning, rejection and fallback.

No included source establishes general causal policy value, optimal action
selection under an external utility or regret guarantees. Those topics would
require additional owner-selected literature.
