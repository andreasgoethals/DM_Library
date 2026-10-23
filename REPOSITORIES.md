# Repository guide

These are greppable source snapshots for the selected Decision Models corpus. They
contain implementations, evaluation protocols, configuration and license notices;
they are reference material, not installed or executed model packages. Upstream
identity was checked against the paper or first-party release linked below on
19–23 October 2026. Each snapshot embeds its full immutable revision, revision date,
retrieval timestamp, original paths and per-file SHA256 hashes. These dates identify
code snapshots and need not equal the dates of the filed papers.

## Overview

| Snapshot | Official upstream | Purpose | Revision prefix | Files | License notice |
|---|---|---|---|---:|---|
| [VLLMDecision2.txt](repositories/VLLMDecision2.txt) | [official source](https://huggingface.co/vllm-sr/Decision-2.0-Vega-27B) | Decision 2.0 Vega renderer, readout and model wrapper | 71d6ae1db4a7 | 26 | Apache-2.0 |
| [Kev.txt](repositories/Kev.txt) | [official source](https://github.com/jaredpalmer/kev) | Kev pointer-head models, training and serving | 2074cc442562 | 253 | Apache-2.0; per-source data terms retained |
| [H2OLightning.txt](repositories/H2OLightning.txt) | [official source](https://huggingface.co/h2oai/h2o-lightning-4b) | H2O decision shim, calibration and attention-mode configuration | e7b32490c9d2 | 28 | Apache-2.0 |
| [Tev1.txt](repositories/Tev1.txt) | [official source](https://github.com/togethercomputer/tev1) | Together answer-token training recipe and inference examples | 1dde7782382c | 43 | MIT code; fine-tuned weight license pending |
| [System1Arena.txt](repositories/System1Arena.txt) | [TianyuCodings/S1-Arena](https://github.com/TianyuCodings/S1-Arena) | Common decision requests, metrics and closed-loop environment protocols | 28e16b16cdf6 | 265 | Apache-2.0 |
| [Jeff.txt](repositories/Jeff.txt) | [j-geuter/Jeff](https://github.com/j-geuter/Jeff) | Jeff decision-head readout, prompts and local serving | 12ba07920283 | 19 | Apache-2.0 |
| [JevOut.txt](repositories/JevOut.txt) | [xzx34/JevOut](https://github.com/xzx34/JevOut) | Context sensitivity and targeted decision flips | c8ab231728ab | 47 | Apache-2.0 |
| [SearchJev.txt](repositories/SearchJev.txt) | [EvoScientist/SearchJev](https://github.com/EvoScientist/SearchJev) | Search decision training, restricted scoring and calibration | 054ea81d4307 | 22 | Apache-2.0 |
| [SIIDecision.txt](repositories/SIIDecision.txt) | [amazingljy1206/SII-Decision](https://github.com/amazingljy1206/SII-Decision) | General decision training and JEVal evaluation | 1723d83cbda6 | 29 | Apache-2.0 |
| [JevBenchmarking.txt](repositories/JevBenchmarking.txt) | [AppliedMachineLearning-Lab/jev-benchmarking](https://github.com/AppliedMachineLearning-Lab/jev-benchmarking) | Benchmark tasks, response caching and probability metrics | 87562114d235 | 54 | MIT; response-specific notices retained |
| [StrandsDecider.txt](repositories/StrandsDecider.txt) | [strands-labs/strands-decider](https://github.com/strands-labs/strands-decider) | Pointer-head architecture, training recipes and calibration | d942e5515db7 | 206 | Apache-2.0; third-party notices retained |
| [InternDecision.txt](repositories/InternDecision.txt) | [InternLM/Intern-Decision](https://github.com/InternLM/Intern-Decision) | Masked decision training, inference and calibration pilot | 565350244af8 | 69 | Apache-2.0; benchmark notices retained |
| [TypeSafeSystemOneAdapter.txt](repositories/TypeSafeSystemOneAdapter.txt) | [typesafe-ai/system-one-adapter-python](https://github.com/typesafe-ai/system-one-adapter-python) | LLM baseline adapter for the TypeSafe decision interface | e1d4cc938204 | 40 | MIT |
| [Clef.txt](repositories/Clef.txt) | [Cloudflare/clef](https://huggingface.co/Cloudflare/clef) | Joint-schema decision head and inference | a30162b99d68 | 10 | Apache-2.0 |
| [LiquidD1_3B.txt](repositories/LiquidD1_3B.txt) | [LiquidAI/d1-3B](https://huggingface.co/LiquidAI/d1-3B) | Text/image decision inference | 051bcc464b01 | 12 | LFM Open License v1.0 |
| [LiquidD1_Omni600M.txt](repositories/LiquidD1_Omni600M.txt) | [LiquidAI/d1-omni-600M](https://huggingface.co/LiquidAI/d1-omni-600M) | Encoder-based text/image/audio decisions | 02b55d7076f1 | 9 | LFM Open License v1.0 |
| [PerplexityDecider.txt](repositories/PerplexityDecider.txt) | [perplexity-ai/pplx-decider-v1.1-27b](https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b) | Decision readout, training and data construction | 14c9d9013796 | 33 | Apache-2.0; NOTICE retained |
| [AnyJev.txt](repositories/AnyJev.txt) | [nokia-applied-research/AnyJev](https://github.com/nokia-applied-research/AnyJev) | Training-free typed readout, order marginalization and selective prediction | 35311c589557 | 66 | Apache-2.0; third-party notices retained |
| [StartLuxDecision.txt](repositories/StartLuxDecision.txt) | [StartLuxLabs/StartLux-Decision](https://github.com/StartLuxLabs/StartLux-Decision) | Instant/deliberative inference, readout controls and adaptation | a99977d9332d | 136 | Apache-2.0 |

## `JevOut.txt`

**Identity:** the code link in Xu et al. (2026), *JevOut: Natural Context Can Flip
Decision Models*, points to this [repository](https://arxiv.org/html/2609.30243v1).
It provides an audit of input-context sensitivity, not a new model implementation.

- `context_optimization/optimize.py` — `optimize_context` searches for context that
  changes a decision while retaining the underlying question.
- `context_optimization/independent.py` — `sample_independent_context` supplies the
  independent sampling comparison needed to distinguish adaptivity from a budget effect.
- `context_optimization/metrics.py` — `targeted_flip_rate` and `target_margin`
  define the reported attack-oriented endpoints.
- `context_optimization/targets.py` — `JevTarget`, `HttpDecisionTarget` and
  `CachedTarget` separate the tested interface from query reuse.
- `docs/paper_protocol.md` and `context_optimization/prompts/checker.txt` preserve
  protocol and checker wording, which matter when interpreting label preservation.

Use this source map to inspect the intervention and denominator before comparing
its flip rates with ordinary benchmark error rates. Model weights and response
trajectories are not part of the snapshot.

## `SearchJev.txt`

**Identity:** Cao et al. (2026), *SearchJev: A Fast and Calibrated System-1 Model
for Search Agents*, links [EvoScientist/SearchJev](https://arxiv.org/html/2610.05107v1).
This release contains training and inference code, including the task schema.

- `training/modeling.py` — `restricted_menu_logits` exposes candidate-restricted
  scoring; `apply_lora` and `load_for_inference` connect training to deployment.
- `training/loss.py` — `jev_loss` is the concrete training objective.
- `training/calibration.py` — `fit_calibration`, `fit_temperature` and
  `temperature_for` show how learned temperatures are fitted and selected.
- `training/inference.py` — `JEVPredictor`, `decide_batch_tta` and `answer_jev`
  connect option permutation handling, batched inference and the typed interface.
- `start_training.py` and `config.yaml` retain the executable training entry and
  configuration instead of relying only on paper descriptions.

Use these paths to distinguish architecture, calibration and test-time permutation
averaging. This source archive alone does not reproduce trained checkpoints or scores.

## `SIIDecision.txt`

**Identity:** the filed v2 of Duan et al. (2026), *General Decision Models:
Benchmarking and Insights Beyond Jev*, identifies [SII-Decision](https://arxiv.org/html/2610.03935v2).
The earlier InnerJev URL redirects to this canonical GitHub repository; it is one
implementation, so only one stable snapshot is registered.

- `sii_decision/learning.py` — `Readout` and `loss_terms` define the decision
  readout and training loss terms.
- `sii_decision/train.py` — training, validation and export entry point.
- `sii_decision/infer.py` — `DecisionEngine` maps model outputs to predictions.
- `sii_decision/evaluation.py` — `evaluate_predictions` computes the evaluation
  outputs used by the implementation.
- `configs/4B/full.json`, `configs/4B/lora.json` and
  `scripts/train_27b_lora.sh` preserve full-rank versus adapter configuration.
- `docs/VALIDATION.md` records implementation validation context.

Use this source to investigate the proposed training recipe and its evaluation
contract. JEVal data and checkpoint files remain upstream.

## `JevBenchmarking.txt`

**Identity:** Section 3.7 of Deußer et al. (2026), *Evaluating and Benchmarking
the System One Model Jev*, gives this [official repository](https://arxiv.org/html/2609.37647v1).
The snapshot retains the harness and analysis while excluding the large response
archive and generated result tables.

- `jev_benchmarking/cache.py` — `request_key` and `ResponseCache` determine reuse
  of exact requests.
- `jev_benchmarking/runner.py` — `run_examples` handles asynchronous requests.
- `jev_benchmarking/tasks/base.py` — `Task`, `choice`, `noul` and `score` expose
  the translation from datasets into decision contracts.
- `jev_benchmarking/metrics.py` — `ece`, `aurc`, `binary_metrics` and
  `score_metrics` distinguish calibration, selective accuracy and task metrics.
- `jev_benchmarking/thresholds.py` — `best_threshold` and `tune` implement
  development-set threshold selection.
- `jev_benchmarking/openmodel/scorer.py` — `HFScorer` is the open-model baseline
  scoring path; `scripts/make_paper_assets.py` regenerates paper outputs.

Use it to check denominators, threshold fitting and baseline comparability.
Response-specific license notices are retained even though response data are excluded.

## `StrandsDecider.txt`

**Identity:** the [Strands launch article](https://strandsagents.com/blog/introducing-strands-decider/)
links this repository directly. The snapshot is newer than the launch article and
includes subsequent configurations; it should not be mistaken for a frozen launch release.

- `src/strands_decider/modeling.py` — `PointerHead`, `SlotHead` and
  `StrandsDeciderModel` permit direct comparison of the two readout designs.
- `src/strands_decider/infer.py` — `SystemOneEngine` and `load_engine` implement
  request evaluation and model loading.
- `training/train.py` — `TrainConfig` and `train` define optimization.
- `training/evaluate.py` — `fit_temperature_by_kind` and
  `expected_calibration_error` expose the calibration procedure.
- `training/data/recipes.py`, `data/generators/llm_client.py` and
  `training/recipe.sh` preserve data-construction code and training orchestration.
- `configs/experiments/v19.yaml` and `docs/architecture.md` retain the launch-era
  configuration and architectural account within the current source tree.

Keep this snapshot for a comparatively complete training path. Raw corpora,
generated figures and deployment-specific cloud provisioning are excluded.

## `InternDecision.txt`

**Identity:** the selected [Intern-Decision-4B model card](https://huggingface.co/internlm/Intern-Decision-4B)
links the InternLM repository. One code snapshot covers the model family; separate
weight-size copies would duplicate its implementation.

- `src/inputs/schema.py` — `compile_row` constructs the decision representation.
- `src/inputs/masked.py` — `MaskedOpenaiTokenizeFunction` and
  `masked_sft_llm_collator` define masked training inputs.
- `src/model/qwen.py` — `DecisionQwen` supplies the model adaptation.
- `src/inference/hf_backend.py` — `HFBackend` implements the inference backend;
  `src/inference/temperature.py` supplies `scale_probabilities`.
- `src/eval/calibration.py` — `fit_temperature` fits calibration;
  `src/eval/known_distribution.py` builds the known-distribution pilot.
- `docs/CALIBRATION_BENCHMARK.md` and `configs/training/qwen35.py` connect the
  pilot's protocol to the concrete training setup.

Read the calibration pilot separately from general benchmark accuracy. Its
known reference distributions support a narrower claim than universal calibration.

## `TypeSafeSystemOneAdapter.txt`

**Identity:** TypeSafe's [introduction article](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
links this adapter as its LLM comparison interface. It is not Jev's proprietary
architecture, training code or weights.

- `src/system_one_adapter/_client.py` — `SystemOneAdapterClient` and
  `AsyncSystemOneAdapterClient` implement the public client surface.
- `src/system_one_adapter/_schema.py` — `create_llm_output_model` compiles the
  constrained output schema supplied to generative providers.
- `src/system_one_adapter/_utils/probability_normalization.py` —
  `rescale_probabilities` makes probability postprocessing inspectable.
- `src/system_one_adapter/_utils/confidence_metrics.py` — `choice_confidence`
  and `score_confidence` define the exposed confidence summaries.
- `src/system_one_adapter/providers/openai.py` and
  `src/system_one_adapter/_utils/error_handling.py` expose provider requests and retries.

This is useful for checking whether a comparison uses native probabilities or
elicited and normalized LLM outputs. Recorded API cassettes are excluded.

## `Clef.txt`

**Identity:** Cloudflare's [Clef release article](https://blog.cloudflare.com/clef-decision-models/)
links the Hugging Face model repository, which contains its inference implementation.

- `joint_schema_model.py` — `EvidenceRoutingLayer`, `JointSchemaHead` and
  `ClefModel` define the specialized head.
- The same file contains `encode_record`, `collate_records`,
  `load_release_model` and `systemone`, connecting schema rendering to responses.
- `joint_head_config.json`, `config.json` and `chat_template.jinja` retain the
  head settings, backbone configuration and prompt template.

This snapshot covers the released inference path. Training claims in the article
are not established merely by finding this inference code. Clef-flash's
corresponding model source had the same SHA256 on the inspection date, so its
duplicate implementation is omitted; its checkpoint/configuration identity is
still distinct. Neither model's weights nor tokenizer vocabulary is included.

## `LiquidD1_3B.txt`

**Identity:** Liquid AI's [open d1 announcement](https://www.liquid.ai/blog/d1-open)
links this model repository. The license retained here is LFM Open License v1.0.

- `modeling_d1.py` — `D1Model` supplies the model integration.
- `api.py` — `SystemOneApi` converts probabilities into typed answers.
- `runner.py` — `SystemOne`, `_readout` and `plan_batches` expose scoring and
  batching mechanics.
- `prompt.py`, `hybrid.py`, `lfm2_vl.py`, `config.json` and
  `chat_template.jinja` preserve input construction and the backbone adaptation.

Use this to inspect the text/image inference implementation. Timing figures and
training details in the announcement remain release claims rather than locally
reproduced measurements. This implementation is distinct from the Omni encoder.

## `LiquidD1_Omni600M.txt`

**Identity:** the same [Liquid AI announcement](https://www.liquid.ai/blog/d1-open)
links this second, architecturally different model. Its separate snapshot is
intentional; it is not a smaller copy of the 3B inference path.

- `modeling_d1.py` — `D1OmniConfig` and `D1OmniModel` integrate modality inputs
  with typed decisions.
- `encoder.py` — `Trunk` and `DecisionHead` define the encoder and decision head.
- `audio.py` and `vision.py` contain the audio and visual encoders.
- `prompt.py` and `config.json` preserve rendering and configuration.

The model interface accepts images or audio for a request, with constraints
documented in the upstream model card. The snapshot contains source and the LFM
Open License v1.0, while weights and tokenizers remain upstream.

## `PerplexityDecider.txt`

**Identity:** the selected [pplx-decider-v1.1-27b card](https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b)
ships code inside the model repository. Keeping it here preserves the evaluated
implementation, not just a model-card summary.

- `source/src/autojev/model.py` — `DecisionModel`, `prepare` and
  `enable_noncausal_full_attention` expose the readout, input limits and attention change.
- `source/src/autojev/data.py` — `NearDuplicates`, `Families` and `build` make
  data preparation and exclusion mechanics inspectable.
- `source/src/autojev/train.py` — `ScheduledRows`, `augment` and
  `save_selected` connect data scheduling, augmentation and checkpoint selection.
- `training/config.json`, `training/train.sbatch`, `decision_config.json` and
  `release-manifest.json` retain training and release provenance.

The data pipeline refers to external sources, including Nimble. Those dependencies
are not copied into a second snapshot; the source retains the relevant references
and license notices. No training data, vocabulary or weights are downloaded.

## `AnyJev.txt`

**Identity:** Zhang et al. (2026), *AnyJev Technical Report*, links the Nokia
[official implementation](https://arxiv.org/html/2610.00831v1). It adds a substantial
training-free alternative to the model-specific implementations already covered.

- `anyjev/decider.py` — `Decider` connects prompt construction, backend scoring
  and the typed decision interface.
- `anyjev/readout.py` — `resolve_labels`, `build_prompt` and `PromptSpec` define
  legal answer labels and prompt structure.
- `anyjev/calibrate/permute.py` — `cyclic_shifts`, `spread_order` and `marginalize`
  implement option-order handling and aggregation.
- `anyjev/calibrate/stopping.py` — `choose_threshold`, `cp_upper`, `stop_step`
  and `log_margin` expose the selective-prediction controls. A confidence bound
  still depends on the sampling and threshold-selection protocol.
- `anyjev/backends/hf.py`, `anyjev/backends/vllm.py`,
  `anyjev/backends/llamacpp.py` and `anyjev/backends/sglang.py` provide inference
  backends; `anyjev/serve.py` exposes serving.
- `tests/test_stopping.py` and `tests/test_decider_fake.py` retain useful checks.
  `anyjev/tacit.py` contains `Tacit`, a later implementation extension; its
  presence does not make it part of the filed technical report's experiments.

The snapshot keeps source, tests, configuration, `LICENSE` and `THIRD_PARTY.md`.
Recorded benchmark runs, outputs, parity artifacts and demo deployment assets
are excluded. This is reusable probability-readout and evaluation infrastructure,
not a release of a newly trained foundation model.

## `StartLuxDecision.txt`

**Identity:** Zhuang et al. (2026), *StartLux-Decision: AutoThink Decision Models
with Reinforcement Learning for Calibrated Deliberative Decisions*, links the
[official implementation](https://arxiv.org/html/2610.17309v1). It adds both
instant and deliberative decision inference with multiple supported backends.

- `startlux_decide/pipeline.py` — `Decider`, `Decision` and `default_controls`
  organize the public decision interface.
- `startlux_decide/readout.py` — `probabilities`, `mixture`, `retemper`,
  `knockout_groups` and `knockout_combine` implement probability readout,
  temperature controls and grouped selection for larger option sets.
- `startlux_decide/controls.py` — `parse_controls` and `Controls` define
  inference settings; `startlux_decide/vllm_plugin.py` supplies `install`
  and `plugin`.
- `startlux_decide/backends/transformers.py`, `startlux_decide/backends/vllm.py`,
  `startlux_decide/backends/llamacpp.py` and `startlux_decide/backends/mlx.py`
  retain the backend-specific paths.
- `v1/finetune/finetune_lora.py` — `step_loss` retains adaptation code;
  `v1/finetune/calibrate.py`, `v1/eval/suites.py` and
  `v1/startlux_decision/model.py` preserve calibration, evaluation and the
  earlier implementation.

The snapshot keeps source, configurations, backend patches and license notices,
while excluding weights, responses and generated results, including nested v1
directories. Public inference and adaptation code do not establish that the full
three-stage training pipeline, reinforcement-learning data or all reported runs
have been released.

## Coverage boundaries

The earlier eight-paper expansion added AnyJev and StartLux-Decision to the snapshot
set. Intern-Decision was already registered. The 23 October additions include
System1Arena, Jeff, Tev1, H2OLightning, Kev and VLLMDecision2. Narrow study-specific evaluation
supplements can be linked from paper summaries without adding another maintained
dump; model websites and duplicative adapters do not qualify merely by existing.

Rechecked against primary sources on **2026-10-20**:

Li et al. (2026), *JEV-as-a-Judge: Accept When Confident, Escalate When Unsure*,
describes a supplementary reproduction package in
[the filed v5 paper](https://arxiv.org/html/2609.26550v5).
The [author project repository](https://github.com/yubol-bobo/jev-as-a-judge)
and its README identify it as a static website with a manuscript and figures;
they do not supply the experimental implementation or the anonymous supplement.
The similarly named [RoundTable02 project](https://github.com/RoundTable02/Jev-as-a-judge)
describes a different frozen pairwise-evaluation study, and
[the third-party cascade scaffold](https://github.com/dataelvisliang/jev-as-a-judge-scaffold)
explicitly says it does not reproduce Li et al.'s experiments. None is registered
as the missing implementation. The remaining limitation is experimental-code
availability, not the absence of an author website.

The [Microsoft-Decision-1 release article](https://commandline.microsoft.com/microsoft-decision-1-model-foundry/)
links Microsoft Foundry and OpenRouter access. No public official model
implementation or training release was verified in that article or the targeted
repository search. Client demonstrations and third-party alternatives do not
expose the released model's internals. TypeSafe's adapter similarly does not expose
Jev internals. These are documented availability boundaries, not missing refresh
registrations; the unsuccessful search is not proof that no future release exists.

The owner-requested OpenAI, Inception, Upstage and Fastino sources document hosted
decision endpoints. No official implementation or weight release for those exact
decision models was verified on 23 October. General client SDKs are not substitutes
for model internals. The Tev1 source snapshot's MIT notice likewise does not settle
its unfinished weight license. See [DECISION_MODELS.md](DECISION_MODELS.md) for
the model-level access distinctions, including Jeff's non-commercial weights.

## Refresh and regeneration

```powershell
python scripts/dumps/refresh_repositories.py
python scripts/dumps/refresh_repositories.py --only SearchJev
python scripts/dumps/refresh_repositories.py --only SIIDecision --timeout 180
python scripts/checks/check_symbols.py
```

The mapping in [refresh_repositories.py](scripts/dumps/refresh_repositories.py)
is authoritative. All nineteen snapshots participate in a normal refresh and the
consolidated maintenance command. Repeat `--only` for several targets. For exact
historical regeneration, pass one target and `--revision` with the full revision
embedded in its header. The source files and their hashes can be reproduced;
the retrieval timestamp naturally changes.

GitHub trees are fetched through shallow, blob-free Git clones with no checkout;
selected files are fetched by immutable raw URLs. Hugging Face trees are paginated
through its API at a resolved revision. Source/configuration extensions, executable
scripts, patches and license notices are retained. Dataset/weight formats,
vocabularies, response archives, generated outputs and unrelated deployment assets
are excluded. Each selected source download is bounded at 2 MB; unexpected larger
source fails safely for review rather than replacing a good snapshot incompletely.
Gitingest flattens the selected temporary tree with its default ignore patterns
overridden, so selected scripts and lockfiles are retained. The refresh refuses to publish
a dump if it omitted a nonempty selected source file.

Replacement is atomic. Failed retrievals and snapshots smaller than half the old
file keep the previous snapshot. Use `--force-shrink` only after checking that the
upstream reduction is legitimate. Unknown target names and invalid arguments return
exit code 2; a failed refresh returns 1; a complete refresh returns 0.

All current snapshots are below 95 MB. If a future selected snapshot exceeds
95,000,000 bytes, refresh refuses to install it until its exact
`/repositories/<filename>.txt` path appears in `.gitignore`. Document that exception
here and regenerate it with the same targeted command. There are no inherited
large-repository exceptions or infrastructure snapshots.

After refresh, run symbol and documentation checks, update this guide when paths
or behavior changed, and record substantive changes in `CHANGELOG.md`. Cite source
paths and symbols, never flattened dump line numbers. Snapshot presence verifies
source availability; it does not establish that upstream code or benchmarks run
successfully in a local model environment.

## `System1Arena.txt`

Common decision requests, metrics and closed-loop environment protocols. Source identity is linked from the filed paper; revision `28e16b16cdf68800a4cba148c3c6ea036f75bda3`. Read `s1arena/runner.py` and `s1arena/models/openai_decisions.py` for implementation details. These are source snapshots, not locally executed benchmarks or models.

## `Jeff.txt`

Jeff decision-head readout, prompts and local serving. Source identity is linked from the filed paper; revision `12ba07920283231fb9bab46359679a70e3f9eb1e`. Read `src/jeff/head.py` and `src/jeff/model.py` for implementation details. These are source snapshots, not locally executed benchmarks or models.

The filed Typed Decision Models on Tabular Data PDF does not identify an author-owned implementation repository. This is an availability boundary, not evidence that no future release will appear. Jeff serves the separately released trained models; it should not be confused with the independently registered SII-Decision implementation.

## `Tev1.txt`

Together answer-token training recipe and inference examples. Identity is verified from the owner-selected primary record; exact source revision `1dde7782382c9f49d627153759b8d1deab426ce0`. Read `README.md`, `DATA_SOURCES.md`, `examples/decide.py` and `examples/train_together.py`. The code recipe uses an ordinary language-model output head. Source-code licensing does not finalize the separate Hub weight license.

## `H2OLightning.txt`

H2O decision shim, calibration and attention-mode configuration. Identity is verified from the owner-selected primary record; exact source revision `e7b32490c9d2a994bd75a4d1ea7e45716080175e`. Read `h2o_lightning_shim.py`, `pooled_readout.py`, `serve_config.json` and `serve.sh`. Saved temperatures, the yes/no adjustment, state truncation and the selected one-way/two-way engine are part of reproduction. Weights, vision assets and generated evaluation results are excluded.

## `Kev.txt`

Kev pointer-head models, training and serving. Identity is verified from the owner-selected primary record; exact source revision `2074cc44256200bb37540103fa4572901faa10f3`. Read `kev/model.py`, `kev/train.py`, `kev/serve.py` and `docs/model-cards/kev-27b.md`. The snapshot retains implementation and model documentation while excluding training runs, checkpoint files and bulk data. Upstream agent/skill text, when present, is reference material and never workspace instructions.

## `VLLMDecision2.txt`

Decision 2.0 Vega renderer, readout and model wrapper. Identity is verified from the owner-selected primary record; exact source revision `71d6ae1db4a786d98775d65c68c41be0e39bfe7c`. Read `modeling_decision2.py`, `decision_config.json`, `decision2/api.py` and `decision2/shared_ctx.py`. This is the released Vega artifact implementation rather than a snapshot of the entire semantic-router project. Model tensors are excluded.
