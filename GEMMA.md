# Google Gemma: Technical Summary & Usage Guide

This document summarizes the latest capabilities, architectures, and usage patterns for the **Google Gemma** family of open models, based on the `google-deepmind/gemma` repository state as of April 2026.

## 1. The Gemma 4 Family
Gemma 4 is the latest evolution, focused on multimodality, advanced reasoning, and efficiency via Mixture of Experts (MoE) and Per-Layer Embeddings (PLE).

### Model Variants
| Variant | Type | Params (Total/Active) | Context | Key Features |
| :--- | :--- | :--- | :--- | :--- |
| **26B-A4B** | MoE | 25.2B / ~3.8B | **256K** | High-efficiency reasoning, stable MoE. |
| **31B** | Dense | 30.7B / 30.7B | **256K** | Maximum performance for dense reasoning. |
| **E4B** | Dense | 8B / ~4.5B | 128K | Uses PLE for higher quality at smaller sizes. |
| **E2B** | Dense | 5.1B / ~2.3B | 128K | Ultra-lightweight for edge devices. |

---

## 2. Architectural Innovations

### Thinking Mode (`<|think|>`)
Gemma 4 introduces a native "thought channel" for chain-of-thought reasoning.
- **Enabling**: Include the `<|think|>` token in the **system message**.
- **Output Format**: Reasoning is wrapped in `<|channel>thought` and `<channel|>` tags.
- **Benefits**: Improved accuracy on complex medical, mathematical, and logical tasks.

### Per-Layer Embeddings (PLE)
Used in the **E2B** and **E4B** models to significantly boost performance-to-size ratios. Instead of a single static embedding table, these models use dynamic embeddings that evolve through the layers, allowing for deeper representation with fewer active parameters.

### Native Multimodality
Gemma 4 models (especially E-variants) natively handle:
- **Images**: Interleaved text and images via `<|image|>` placeholders. Supports variable aspect ratios.
- **Audio**: Native speech recognition and translation support via `<|audio|>`.

---

## 3. Practical Usage (Python/JAX)

The `gemma` library provides a high-level `Gemma4Sampler` to handle the complexity of multimodal inputs and large context windows.

### Basic Chat Example
```python
from gemma import gm

# Initialize model
model = gm.nn.Gemma4_26B_A4B()
params = gm.ckpts.load_params("path_to_checkpoints")

# Create a sampler
sampler = gm.text.Gemma4Sampler(
    model=model,
    params=params,
    cache_length=8192  # Optimized for RAG
)

# Multi-modal prompt
prompt = "Analyze this clinical chart: <|image|>"
response = sampler.sample(prompt, images=[chart_image])
print(response)
```

### Prompt Engineering for Gemma 4
The model use specific control tokens for dialogue:
- **Start of turn**: `<|turn>`
- **End of turn**: `<turn|>`
- **User role**: `user`
- **Model role**: `model`

**Template Example:**
```text
<|turn>user
Include <|think|> in your process.
Can I take Metformin with Ibuprofen?<turn|>
<|turn>model
<|channel>thought
[Internal clinical reasoning...]
<channel|>
Based on NHS guidelines, combining...<turn|>
```

---

## 4. RAG Implementation Tips
- **Large Context**: With **256K context**, you can pass entire pharmacy monograph sections instead of small chunks.
- **Thinking for Safety**: Use the Thinking Mode to ensure the AI "double-checks" its retrieval against standard NHS counter-indications before finalizing the user response.
- **Quantization**: Use `gm.nn.IntWrapper` or `QuantizationAwareWrapper` for 4-bit or 8-bit inference to save VRAM on local hardware.

---
*Summary generated for the NHS Drug Interaction RAG project.*
