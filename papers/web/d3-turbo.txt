---
pipeline_tag: zero-shot-classification
license: apache-2.0
library_name: transformers
tags:
- zero-shot-classification
- decision-model
- classification
- system-one
- multimodal
- vision
- video
- object-detection
- safetensors
---

![d3-turbo: Decision 3.0](assets/banner.png)

# d3-turbo

**d3-turbo** is the upgraded 27B multimodal decision model of Decision 3.0, the decision models of [vLLM Semantic Router](https://github.com/vllm-project/semantic-router). Give it an input (text or JSON, optionally with images and videos) and the questions you need answered: pick one of several options, say yes or no, rate on a scale, or point to where something is in an image or a video. It reads the input once per request, answers every question on it, and returns a probability for every answer, without generating text.

**Try it free** at [decision.vllm-sr.ai](https://decision.vllm-sr.ai): the free API serves d3-turbo · Official Space: [vllm-sr/d3-turbo](https://huggingface.co/spaces/vllm-sr/d3-turbo)

| | |
| --- | --- |
| **Parameters** | 26.09B, including the 0.46B vision encoder |
| **Inputs** | Text or JSON, plus images and videos (several per request); images can also sit inside questions and options |
| **Decision types** | Choice · Yes / No · Score · Box (images and video moments) · Track (whole videos) |
| **Context** | 131,072 tokens per question with `long_context=True`; 32,768 by default |
| **License** | Apache-2.0 |

## Highlights

- **Text: 70.2 on the Jev Decision Index, +4.0 over d3 (66.3).** Our estimate, not an official board result. On the public suite, measured with the official 0.3 kit: 71.7 against d3's 65.5, ahead in all five areas.
- **Vision: 72.9 on the Jev Decision Index vision board, +1.7 over d3 (71.3).** Our estimate, measured the same way.
- **State once:** d3-turbo reads the input once and answers every question from it; d3-flash re-reads it for each question. Asking 1 to 255 questions about the same photo, d3-turbo takes 302 ms to 2.12 s and d3-flash 154 ms to 32.94 s: d3-flash is faster at 1 question, d3-turbo from 4 on, and 15.5× faster at 255 (one AMD Instinct MI325X, AutoModel; [Serving performance](#serving-performance)).
- **Box:** ask where something is and get one box with a calibrated confidence: 0.90 accuracy at IoU 0.5 on our Box test set, confidence AUROC 0.96.
- **Video tracking:** a box at any moment of a video, or a track over the whole clip at 1 or 2 updates per second with the probability that the target is visible: success AUC 0.79 / 0.80 and presence F1 0.97 on our tracking test clips.
- **Images in questions and options:** put an image inside a question or an option, not only in the input; only that question sees it: 0.96 accuracy on our test questions with images in them, +0.31 over d3 reading every image in the input.
- **Long context:** up to 131,072 tokens per question with `long_context=True`, served on a single AMD Instinct MI325X; 32,768 tokens by default.

## Examples

Real answers of this release, drawn as returned. The [Quickstart](#quickstart) below runs these same requests.

![Box: four Box questions about one photo in one request, each answer one box with its confidence](assets/example-box.jpg)

![Images in options: which picture shows the same kind of animal? Each option is an image that only this question sees](assets/example-options.jpg)

![Video tracking: the hummingbird over an 11-second clip, two boxes per second, each with its confidence and the probability that it is visible](assets/example-track.jpg)

<sub>Media from Wikimedia Commons: [Australian Shepherd catching a frisbee](https://commons.wikimedia.org/wiki/File:Australian_Shepherd_catching_a_frisbee.jpg) by Sally Wehner ([CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)); two red panda photos by Mathias Appel ([one](https://commons.wikimedia.org/wiki/File:Red_Panda_(24986761703).jpg), [two](https://commons.wikimedia.org/wiki/File:Red_Panda_(25193861686).jpg); [CC0](https://creativecommons.org/publicdomain/zero/1.0/)), a [raccoon](https://commons.wikimedia.org/wiki/File:Common_Raccoon_in_a_Tree.jpg) (CC0) and an [owl](https://commons.wikimedia.org/wiki/File:An_owl_portrait_(52264733713).jpg) by Ted Moravec (CC0); [Anna's hummingbird in Arizona](https://commons.wikimedia.org/wiki/File:Anna%27s_hummingbird_(Calypte_anna)_in_Arizona.webm) by Larry & Teddy Page ([CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)). The pictures in `assets/` are resized, and the clip is its first 11 seconds, re-encoded.</sub>

## Quickstart

```bash
pip install "transformers==5.17.0" torch torchvision pillow opencv-python-headless safetensors accelerate
pip install flash-linear-attention  # optional: fast GPU kernels for the linear-attention layers
```

```python
from huggingface_hub import hf_hub_download
from transformers import AutoModel

model = AutoModel.from_pretrained("vllm-sr/d3-turbo", trust_remote_code=True)


def asset(name):
    return hf_hub_download("vllm-sr/d3-turbo", f"assets/{name}")


# Text: several questions, one call
print(model.system_one(
    state="Ticket: the invoice total is wrong after the plan change.",
    questions={
        "route": {"type": "choice", "instructions": "Which team handles this?",
                  "criteria": {"billing": "Billing", "tech": "Technical support"}},
        "urgent": {"type": "noul", "instructions": "Is the customer asking for an urgent fix?"},
    },
))

# Box: where is it in the image? Four questions, one read of the photo
print(model.system_one(
    state="A photo from a dog festival.",
    images=[asset("example-frisbee.jpg")],  # local paths, http(s) URLs, PIL images or base64-encoded images
    questions={
        "frisbee": {"type": "box", "instructions": "The frisbee"},
        "tail": {"type": "box", "instructions": "The dog's tail"},
        "cone": {"type": "box", "instructions": "The orange cone"},
        "camera": {"type": "box", "instructions": "The camera on the tripod"},
    },
))

# Images in options: each option is an image that only this question sees
print(model.system_one(
    state="This animal: <animal>",
    questions={"pick": {"type": "choice", "instructions": "Which picture shows the same kind of animal?",
                        "criteria": {"a": "<a>", "b": "<b>", "c": "<c>"}}},
    assets={"<animal>": asset("example-panda.jpg"), "<a>": asset("example-option-a.jpg"),
            "<b>": asset("example-option-b.jpg"), "<c>": asset("example-option-c.jpg")},
))

# Video: a track over the whole clip, two boxes per second
print(model.system_one(
    state="A bird at a feeder.",
    videos=[asset("example-hummingbird.mp4")],  # local paths, http(s) URLs, base64-encoded videos or frame arrays
    questions={"target": {"type": "track", "instructions": "The hummingbird", "rate": 2}},
))
```

A Box answer is `{"type": "box", "box": {"top", "bottom", "left", "right"}, "confidence"}` (edges as fractions of the image's height and width); a track answer is `{"type": "track", "track": [{"time", "box", "confidence", "visible"}, ...]}`. With one video in the input, a `box` question with `"at"` (seconds) gives the box at that moment. There is always exactly one box, even when the object is absent, so pair a Box question with a yes / no question when it may be missing. For inputs longer than 32,768 tokens per question, pass `long_context=True`; a question over its limit is answered with the error `max_length_exceeded`, and nothing is truncated.

## Try it free: the API

Get a free key on the home page of [decision.vllm-sr.ai](https://decision.vllm-sr.ai) (one click, no account), then:

```bash
curl -s https://decision.vllm-sr.ai/v1/systemone \
  -H "Authorization: Bearer $DECISION_API_KEY" \
  -H 'content-type: application/json' -d '{
  "model": "vllm-sr/d3-turbo",
  "state": "Write a Python function that reverses a string.",
  "questions": {
    "kind": {"type": "choice", "instructions": "What kind of work is this?",
             "criteria": {"code": "Writing or fixing code", "math": "Mathematics", "chat": "Anything else"}},
    "reasoning": {"type": "noul", "instructions": "Does answering this need multi-step reasoning?"}
  }
}'
```

On the API, `vllm-sr/d3` names the same model. The free API has its own limits, below the model's own: up to 131,072 characters of input and 131,072 estimated tokens per request (the estimate counts the text's UTF-8 bytes, so a request holds fewer real tokens than that), 64 questions, 16 images of up to 16 MiB and one video of up to 60 seconds. The current values are at [decision.vllm-sr.ai/api/info](https://decision.vllm-sr.ai/api/info).

## Run with vLLM SR Engine

[vLLM Semantic Router](https://github.com/vllm-project/semantic-router)'s Engine mode serves d3-turbo behind the same System One API, on one AMD Instinct MI325X:

```bash
curl -fsSL https://vllm-sr.ai/install.sh | bash -s -- --channel dev --no-launch
vllm-sr serve vllm-sr/d3-turbo --engine --platform rocm
```

The first start pulls the `vllm-sr-rocm` image and downloads the model (about 2.5 minutes on our test host); later starts take about 35 seconds. Then send it the request above:

```bash
curl -s localhost:8899/v1/systemone -H 'content-type: application/json' -d '{
  "model": "vllm-sr/d3-turbo",
  "state": "Write a Python function that reverses a string.",
  "questions": {
    "kind": {"type": "choice", "instructions": "What kind of work is this?",
             "criteria": {"code": "Writing or fixing code", "math": "Mathematics", "chat": "Anything else"}},
    "reasoning": {"type": "noul", "instructions": "Does answering this need multi-step reasoning?"}
  }
}'
```

```json
{"answers": {"kind": {"type": "choice", "choice": "code", "probabilities": {"code": 0.9996, "math": 0.00004, "chat": 0.0003}, "confidence": 0.9995},
             "reasoning": {"type": "noul", "noul": 0.040}},
 "model": "vllm-sr/d3-turbo", "usage": {"input_tokens": 158, "output_tokens": 0}}
```

The engine reads each request's input once for all of its questions, up to 255, and answers Box and track questions too: 64 questions about one photo take 0.50 s. Images and videos go in as base64 data URLs ([Router and Engine modes](https://github.com/vllm-project/semantic-router/blob/main/src/vllm-sr/INSTANCE_MODES.md#find-things-in-images-and-videos)).

## Serving performance

**Ask once, answer many.** d3-turbo reads the input once per request and answers every question on it, so more questions about the same input add little time. On one AMD Instinct MI325X with AutoModel, 255 questions about one photo take 2.12 s, 15.5× less than d3-flash (32.94 s), which reads the photo again for each question; at 64 questions the gap is 9.5× (867 ms against 8.26 s). With a single question, the smaller d3-flash is faster (154 ms against 302 ms); from 4 questions on, d3-turbo is. The free API takes up to 64 questions per request, so the 128 and 255 rows apply when you run the model yourself.

![Ask once, answer many: median time to answer 1, 4, 16, 64, 128 and 255 questions about one photo, d3-turbo and d3-flash on one AMD Instinct MI325X](assets/ask-once.png)

| Questions about one photo | d3-turbo, p50 / p90 | d3-flash, p50 / p90 | d3-flash p50 ÷ d3-turbo p50 |
| ---: | ---: | ---: | ---: |
| 1 | 302 / 302 ms | 154 / 156 ms | 0.5× |
| 4 | 328 / 329 ms | 541 / 542 ms | 1.6× |
| 16 | 426 / 427 ms | 2.07 / 2.10 s | 4.9× |
| 64 | 867 / 910 ms | 8.26 / 8.27 s | 9.5× |
| 128 | 1.29 / 1.29 s | 16.50 / 16.56 s | 12.8× |
| 255 | 2.12 / 2.13 s | 32.94 / 33.11 s | 15.5× |

## Evaluation

### Text: Jev Decision Index 0.3.2

| Model | Jev Decision Index ↑ |
| --- | ---: |
| **d3-turbo** (our estimate) | **70.2** |
| d3 (official board) | 66.3 |

![Jev Decision Index 0.3.2 snapshot of 2026-10-16: rank on the official text and vision boards, d3 (official) and d3-turbo (our estimate)](assets/index-rank.png)

<sub>The Jev Decision Index 0.3.2 boards, snapshot of 2026-10-16: d3's official ranks and d3-turbo's estimated ranks on those boards.</sub>

On the public suite, measured with the official 0.3 kit for both models, d3-turbo scores 71.7 against d3's 65.5 (+6.2), ahead in all five areas: Knowledge +3.7, Language +6.4, Retrieval +9.1, Tools +4.3 and Arts +9.6.

![Jev Decision Index by area: public-suite skill of d3-turbo and d3](assets/index-areas.png)

### Images: Jev Decision Index vision board 0.3.2

| Model | Vision Index ↑ |
| --- | ---: |
| **d3-turbo** (our estimate) | **72.9** |
| d3 (official board) | 71.3 |

### Images: Box and images in options

| Measure | d3-turbo |
| --- | ---: |
| Box: accuracy at IoU 0.5 | 0.90 |
| Box: confidence AUROC | 0.96 |
| Images in questions and options: accuracy | 0.96 |
| The same, against d3 reading every image in the input | +0.31 |

### Videos: tracking

| Measure | d3-turbo |
| --- | ---: |
| Track, 1 update per second: success AUC / at-time accuracy at IoU 0.5 / presence F1 | 0.79 / 0.89 / 0.97 |
| Track, 2 updates per second: success AUC / at-time accuracy at IoU 0.5 / presence F1 | 0.80 / 0.89 / 0.97 |

## License

Apache-2.0 ([LICENSE](LICENSE)).

## Citation

```bibtex
@misc{d3turbo_2026,
  title        = {{d3-turbo}: A Multimodal Decision Model that Reads Once},
  author       = {{vLLM Semantic Router Team}},
  year         = {2026},
  howpublished = {\url{https://huggingface.co/vllm-sr/d3-turbo}}
}
```
