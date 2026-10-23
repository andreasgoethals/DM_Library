# Decision models

Verified **23 October 2026**. This is a comparison of released decision models:
systems that score supplied outcomes for classification, routing, ranking or
rubric-based judgments. It covers the major vendor, developer and research
families selected for this library, grouping minor revisions. General LLMs used
only as backbones, benchmarks and inference recipes such as AnyJev are outside
the table. A typed answer is a model prediction; the application decides what
action to execute.

**Open source** is a boolean with a practical, explicit meaning here:
`true` requires public inference code and downloadable decision weights under
a permissive license. It does not assert that all training data or the complete
training pipeline are released. `false` includes hosted-only models,
non-commercial/source-available weights and an unfinished release license.
The license/access column explains which case applies. B/M denote billion/million
parameters; nominal product sizes are distinguished from exact loaded counts.

Dates identify the named release or announcement, not the latest edit to a live
page. An unconfirmed public-release day stays unknown. Context values refer to
the documented serving path where possible; a backbone's position configuration
is labelled as such. **API prices are USD per one million tokens**, input/output,
checked on the verification date. Local weights have no universal token tariff:
hardware and hosting still cost money.

## Comparison

| Name | Open source (boolean) | Release date / evidence | Developer | Parameters | Source | Inputs | Outputs | Context limits | API token costs (USD / 1M input / output) | License / access |
|---|---|---|---|---|---|---|---|---|---|---|
| Jev family | false | 2026-09-15 launch; 1.14 available 2026-10-14 | TypeSafe | Not disclosed | [Release](https://typesafe.ai/blog/introducing-system-one-models-and-jev); [current models](https://docs.typesafe.ai/models) | Text or JSON state plus typed questions; image support requires clarification below | Choice probabilities, yes/no probability, ordinal score; confidence | Default 64k/request and 32k/question; explicit long-context mode raises both to 262k | $0.042 / $0; current 1.13/1.14 rate | Hosted weights; public SDKs do not make Jev itself open source |
| Solar Decide | false | 2026-09-22 beta | Upstage | Not disclosed; built on Solar Mini 4 | [Model card and pricing](https://console.upstage.ai/docs/models/solar-decide) | Text/JSON state and typed questions | Choice, yes/no and score probabilities | 512K advertised endpoint context | $0.10 / $0; cached input $0.10 | Hosted beta |
| Tev1 experimental family | false | 2026-09-23 public 4B launch | Together AI | Nominal 4B and 0.8B; full Hub tensors about 4.660B and 0.873B | [4B card](https://huggingface.co/togethercomputer/Tev1-4B-experimental); [launch/recipe](https://www.together.ai/blog/how-to-train-your-own-jev); [hosted specifications](https://www.together.ai/models/tev1-4b-experimental) | Text state, one question and 2–24 labelled options | One generated answer letter; probability readout requires an additional scoring interface | Hosted 4B: 32.8K advertised; configured positions 262,144; recipe sequence limit 2,048 | Together hosted 4B: $0.04 / $0; self-hosting also possible | Downloadable weights; fine-tuned weight license explicitly being finalized |
| Intern-Decision family | true | 2026-09-26 public 4B release | InternLM | Nominal 0.8B, 2B and 4B | [4B card](https://huggingface.co/internlm/Intern-Decision-4B); [paper](https://arxiv.org/abs/2610.22131); [code](https://github.com/InternLM/Intern-Decision) | Shared text/JSON state, named schema and optional images | Field-specific choice, yes/no and score probabilities | Official inference engine defaults to 8,192 total tokens; image tokens count; up to 8 images | Self-hosted; no universal token price | Apache-2.0, with upstream notices retained |
| Kev family (27B v2 reference) | true | 2026-09-30 for the documented 27B v2 / Kev 1.0 release | Jared Palmer | Family labels 0.8B/4B/9B/27B; referenced 27B loads 25.6B torso + 2.6M head | [Model card](https://github.com/jaredpalmer/kev/blob/main/docs/model-cards/kev-27b.md); [weights](https://huggingface.co/jaredpalmer/kev-27b) | Text/JSON state and named typed questions | Choice distribution, P(yes), score distribution/expected level and confidence | Referenced 27B serves states up to 65,536 tokens plus question overhead; do not transfer that limit to every family member | Self-hosted; no universal token price | Apache-2.0 weights and code for this release |
| GLiDE | false | 2026-09-30 announcement | Fastino | Unconfirmed: live HTML says undisclosed, Markdown catalog says 27B | [Release](https://fastino.ai/blog/introducing-glide-the-first-thinking-decision-model); [current limits](https://docs.fastino.ai/concepts/glide-capabilities); [pricing](https://docs.fastino.ai/pricing) | Text/JSON state; current API also permits images | Choice, yes/no and ordinal scores with probabilities/confidence; selective extra reasoning | 65,536 rendered tokens per state + question; 2–255 choice options; up to 4 images | $0.04 / $0; input usage sums internal passes/questions | Hosted; no verified public-weight release |
| Clef / Clef-flash | true | 2026-10-01 public announcement | Cloudflare | Nominal 27B / 9B; Hub totals about 27.357B / 9.410B | [Release](https://blog.cloudflare.com/clef-decision-models/); [Clef card/code](https://huggingface.co/Cloudflare/clef); [Workers Clef](https://developers.cloudflare.com/workers-ai/models/clef/); [Workers flash](https://developers.cloudflare.com/workers-ai/models/clef-flash/) | Text/JSON state, schema and images; Workers description also lists video | Multiple schema-bound choice, yes/no and score probabilities | Workers Clef 65,536 / flash 24,576; released local encoder defaults to 16,384 and truncates state to fit | Workers Clef $0.24 / $0; flash $0.038 / $0; images billed as input tokens | Apache-2.0; self-hosting also possible |
| Strands Decider (Qwen release) | true | 2026-10-01 public announcement | Strands Labs / Strands Agents | Original release about 1.9B plus pointer head; later backbones have separate cards | [Release](https://strandsagents.com/blog/introducing-strands-decider/); [code](https://github.com/strands-labs/strands-decider); [Qwen checkpoint](https://huggingface.co/StrandsAgents/strands-decider-2B-hobson-v21) | Text state and options; optional vision path depends on code/checkpoint version | Choice, yes/no and rubric-score probabilities | Original Qwen recipe 4,096-token window; some historical evaluations used 3,072; pin checkpoint and serving configuration | Self-hosted; no universal token price | Apache-2.0 for the referenced Qwen release; check later model cards individually |
| Decision 2.0 family | true | 2026-10-03 public release | vLLM Semantic Router Team | Family labels 0.6B–27B; Vega card reports 29.37B actual parameters | [Vega card](https://huggingface.co/vllm-sr/Decision-2.0-Vega-27B); [official runtime](https://github.com/vllm-project/semantic-router/blob/main/src/model-runtime/docs/design.md) | Text or JSON state and several named questions | Simultaneous choice, yes/no and score probabilities | Vega: 32,768 tokens; smaller checkpoints have their own limits | Self-hosted; no universal token price | Apache-2.0 |
| pplx-decider family (v1.1 reference) | true | 2026-10-06 public v1.1 announcement; checkpoint committed 2026-10-05 privately | Perplexity AI | Nominal 27B; full stored tensors about 26.085B | [Card/code](https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b); [public announcement](https://community.perplexity.ai/t/pplx-decider-v1-1-27b-our-updated-open-weights-multimodal-decision-model-is-now-available/6286) | Text/JSON state and images | Typed choice/yes-no/score probabilities using the released readout | Configured positions 262,144; a validated end-to-end decision context at that length is not established by the card | Self-hosted; no universal token price | Apache-2.0; exact mask/head/temperature behavior is checkpoint-specific |
| d1 family | false | 2026-10-07 open-weight release | Liquid AI | d1-3B: 3.12B; experimental omni: 587M | [Release](https://www.liquid.ai/blog/d1-open); [3B card](https://huggingface.co/LiquidAI/d1-3B); [omni card](https://huggingface.co/LiquidAI/d1-omni-600M) | Text/JSON and images; omni additionally supports text + audio | Choice, yes/no and ordinal-score probabilities in a forward pass | 3B: 32,768; omni: 16,384 combined positions, image mode cuts state/question text to 896 tokens; audio up to 30 s | Self-hosted weights; hosted d1 tariff not verified here | LFM Open License v1.0, including a commercial-revenue condition; not permissive open source under this table's definition |
| Microsoft-Decision-1 | false | 2026-10-09 announcement | Microsoft | Qwen3.5-9B-derived; exact deployed total not disclosed | [Official announcement](https://commandline.microsoft.com/microsoft-decision-1-model-foundry/); [OpenRouter offering](https://openrouter.ai/microsoft/microsoft-decision-1) | State/context and fixed options/rubrics | Yes/no, choice, rating and rubric-based probability scores | OpenRouter offering: 32,768 tokens; verify separate Foundry deployment terms | OpenRouter: $0.042 / $0; this is the reseller's published offering, not a verified universal Foundry rate | Hosted through Foundry/OpenRouter; no public decision weights verified |
| Jeff 1.0 family | false | 2026-10-12 technical report; exact first public checkpoint day unconfirmed | Jonathan Geuter, Andrew Cheng, David Alvarez-Melis; Harvard/Kempner | Qwen 4B/27B and Gemma 12B/31B bases plus decision heads | [Paper](https://arxiv.org/abs/2610.17205); [serving code](https://github.com/j-geuter/Jeff); [Qwen card](https://huggingface.co/jgeuter/Jeff-1.0-Qwen-27B); [large card](https://huggingface.co/jgeuter/Jeff-1.0-Large) | Text state, typed question and supplied options | Per-option probabilities; choice, yes/no and ordered score | 8,192 tokens; 2–16 choices/score levels | Self-hosted; no universal token price | Weights CC BY-NC 4.0; serving code Apache-2.0 |
| Decisions API / GPT-6 Luna | false | 2026-10-06 public beta; 2026-10-22 general availability | OpenAI | Not disclosed | [GA release](https://openai.com/index/decisions-api/); [current guide](https://developers.openai.com/api/docs/guides/decisions); [pricing](https://developers.openai.com/api/docs/pricing) | Text, images, native JSON and supported conversation/tool history | Predicate probability, choice distribution/confidence, rubric score/distribution, or refusal | Up to 400 questions/request; numeric Decisions-specific token context not verified here | $0.10 / $0; cached input $0.01; cache writes charged at current Luna rates; regional/long-context multipliers may apply | Hosted dedicated `/v1/decisions` endpoint |
| H2O-Lightning-4B | true | Public launch day unconfirmed; Hub repository created 2026-10-02 | H2O.ai | Nominal 4B; complete Hub tensors about 4.660B | [Model card/code](https://huggingface.co/h2oai/h2o-lightning-4b); [serving configuration](https://huggingface.co/h2oai/h2o-lightning-4b/blob/main/serve_config.json) | Text/JSON record and up to 4 images | Choice, P(yes), ordinal scores and probabilities | Documented engine 40,960 tokens; separate default state cap 32,000, with truncation; up to 255 options | Self-hosted; benchmark cost estimates are not a provider tariff | Apache-2.0 for this Qwen checkpoint |
| Mercury Decide | false | Exact public launch date unconfirmed from the selected primary documentation | Inception | Not disclosed | [API reference](https://docs.inceptionlabs.ai/api-reference/decisions/create-a-decision); [models/pricing](https://docs.inceptionlabs.ai/get-started/models) | Text/JSON shared state; base64 images in state/instructions | Binary probability, categorical choice and ordinal score | Numeric token limit not stated in selected reference; up to 16 images/upstream request, 10 MiB/image and default 20 MiB JSON-body limit | Promotional $0.02 / $0 (regular input $0.04); cached input $0 in current table | Hosted `/v1/decisions`; no public weights verified |

## What the models have in common

The common operation is to score caller-supplied outcomes against a state and
instructions. Choice selects from an unordered set; a yes/no primitive estimates
a binary probability; score assigns mass to ordered levels and may return their
expected index. A score is not automatically a business utility, and a model
cannot choose a useful action omitted from the options. Multiple named
questions usually describe several decisions about one state, not an autonomous
plan with environment feedback.

**Tev1 is an interface exception.** Its documented inference example generates an
answer letter through the ordinary language-model head. Converting that into
probability vectors or a multi-question System One endpoint requires an explicit
scoring/serving contract. Do not silently treat its output as interchangeable
with a model that directly returns every option's probability.

**Inference effort also differs.** Direct candidate heads, masked answer-token
readout and ordinary answer-token generation have different costs. GLiDE adds
reasoning selectively; its documented usage can include multiple internal passes.
A fixed JSON output shape does not imply a single pass, fixed latency or
calibration under a changed policy.

## Openness and licensing

The boolean describes the released decision artifact, not its base model.
Tev1's Qwen base is Apache-2.0 while the fine-tuned weight license is pending.
Jeff's source server is Apache-2.0 while its decision weights explicitly use
[CC BY-NC 4.0](https://huggingface.co/jgeuter/Jeff-1.0-Large).
Liquid's weights are downloadable under the
[LFM Open License](https://huggingface.co/LiquidAI/d1-3B/blob/main/LICENSE),
which includes a commercial-revenue limitation. These three cases therefore
remain `false` despite local-weight availability.

A `true` row still needs the exact checkpoint's notices and data provenance.
It does not promise a fully reproducible training corpus, an independent
evaluation or unrestricted rights to every upstream training source. Jeff's
public serving repository, for example, is not the complete training release.

## Context and input boundaries

Use a deployed limit instead of copying a tokenizer's maximum into an
application. Clef's default encoder truncates the state to fit its 16,384-token
budget. Intern-Decision's engine rejects over-limit requests. H2O separates
engine context, a truncatable state cap, billed input and processed input.
Liquid's omni checkpoint has a much tighter text allowance when images are
present. Schema, question and image positions consume context too.

Two live-documentation conflicts are left explicit. TypeSafe's current
[models page](https://docs.typesafe.ai/models) lists text inputs for Jev 1.13/1.14,
while its [images guide](https://docs.typesafe.ai/images) documents image-bearing
System One requests; image support should be checked for the exact deployed
model. Fastino's live HTML catalog says GLiDE's parameter count is undisclosed,
whereas its Markdown representation lists 27B. Its current capability reference
gives 65,536 rendered tokens, superseding the launch post's 40k claim. These are
not resolved by guessing.

Dates are similarly specific. The table uses verified public announcements
where available. H2O's repository-creation date is only an artifact timestamp.
Jeff's report date is not proof of its first checkpoint launch. The Kev row dates
the named large-model release. The primary-source dates of the H2O and Mercury
records remain year-only in Zotero.

## Comparing API costs

Only the explicitly named endpoint's rates apply. GPT-6 Luna's general
text-generation output price does not apply to Decisions, which does not charge
output tokens. OpenAI's general-availability caching policy also supersedes the
older beta wording that no cache operations were charged. Mercury's $0.02 input
rate is promotional; its stated regular rate is $0.04. A price not verified here
means unknown, never free.

For any model, count rendered state and schema, repeated questions/internal
passes, images, cache reads/writes, transport, retries and escalation. Equal
dollars per million tokens can therefore produce different dollars per completed
decision. For self-hosted models, report hardware, precision, throughput, batching
and serving overhead instead of assigning a universal API token price.

## Model quality and version identity

A probability field's presence establishes the interface, not its calibration
on a new domain. Entropy, top-two margin, P(yes), temperature-scaled probability
and a provider's confidence field have different semantics. Jeff's default
server additionally moves some uncertain yes/no probabilities outside
JevBench's abstention band; H2O has a saved yes/no adjustment too. Preserve those
settings when reproducing a release, and assess raw probabilities separately
when measuring calibration.

Pin checkpoint and runtime revisions, preserve the complete option wording/order
and record the returned hosted model version. Jev aliases and hosted releases can
move independently of application code. Compare accuracy, probability quality,
robustness, latency and total decision cost on the same representative requests;
provider leaderboard positions are not a universal ordering of these models.

All sixteen families have dedicated primary-source records in the selected
Decision Models Zotero collection. Their citation keys and source-specific
summaries are in [SUMMARIES.md](SUMMARIES.md). The broader collection also contains
evaluation papers and inference methods; those are intentionally not model rows.
