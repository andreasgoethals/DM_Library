---
license: apache-2.0
library_name: peft
base_model: Qwen/Qwen3.5-9B
base_model_relation: adapter
language:
- en
tags:
- lora
- qwen3.5
- text-classification
- structured-prediction
- evidence-grounding
---

<p align="center">
  <img src="./Bespoke-Labs-Logo.png" alt="Bespoke Labs" width="550">
</p>

# Bespoke-Nimble-9B

> **Update (September 24, 2026):** Updated to our latest 9B checkpoint, with an 8,192-token context limit and up to 255 choices per field. This release uses T=1.0; the earlier checkpoint remains available at `revision="original-2676"`, and [v2](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B-v2) is unchanged.

A Qwen3.5-9B LoRA adapter for context-grounded choices, booleans, and rubric score levels. It scores the allowed answer tokens directly; the evaluated workflow does not generate reasoning or free-form answers.

This repository contains the adapter (about 165 MiB), tokenizer, exact prompt builder, reference inference code, and release metadata. It requires the [Qwen3.5-9B base checkpoint](https://huggingface.co/Qwen/Qwen3.5-9B/tree/c202236235762e1c871ad0ccb60c8ee5ba337b9a). The full base weights are not duplicated here.

**License:** [Apache 2.0](./LICENSE).

More info: https://github.com/bespokelabsai/nimble

## Loading and scoring

Use a CUDA GPU with BF16 support. The original run used PyTorch 2.8.0 with CUDA 12.8. Install an appropriate CUDA build of PyTorch, then the remaining pinned requirements. The helper processes fields individually and preserves the training prompt and probability calculation.

```bash
hf download bespokelabs/Bespoke-Nimble-9B --local-dir nimble-model
pip install -r nimble-model/requirements.txt
```

Authenticate with a Hugging Face token that can read this repository if it is private. Review the included helper before importing it; no `trust_remote_code=True` is required.

```python
import sys
sys.path.insert(0, "nimble-model")
from inference import NimbleModel

model = NimbleModel("nimble-model")
result = model.score(
    context="The store accepts returns within 30 days. This item was bought 12 days ago.",
    schema={
        "eligible": {
            "type": "boolean",
            "description": "Is this item within the store return window?"
        }
    },
)
print(result["output"])
print(result["fields"]["eligible"]["probabilities"])
```

For choices, use `type="enum"`, a `choices` list of strings, a description, and optional `choice_descriptions`. For rubric scores, use integer-valued enum strings such as `["0", "1", "2"]`, describe each level, and pass that field name in `score_fields=["quality"]`. This returns the selected integer and its probability-weighted expected score. Each field supports at most 255 choices. Prompts exceeding 8,192 tokens are rejected rather than truncated.

The included scorer applies `softmax(candidate_logits / temperature)` once, with a default of **T=1.0**. This checkpoint has not had a separate temperature fit; do not reuse the older model’s 2.179 calibration. For Mac/MLX and Linux loaders, use the current [GitHub quickstart](https://github.com/bespokelabsai/nimble#quickstart).
