---
license: cc-by-nc-sa-4.0
base_model: Qwen/Qwen3-0.6B
tags:
  - terminal
  - command-line
  - cli
  - bash
  - powershell
  - fine-tuned
  - lora
  - peft
  - qwen
language:
  - en
pipeline_tag: text-generation
library_name: peft
---

# Qwen3-0.6B Terminal Command Generator - LoRA Adapters

This repository contains **LoRA adapters** for generating terminal commands from natural language instructions.

## Model Description

- **Base Model:** [Qwen/Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B)
- **Fine-tuning Method:** QLoRA (4-bit quantization + LoRA)
- **Task:** Natural language to terminal command generation
- **Supported OS:** Linux, Windows, macOS

## Performance

| Metric | Score |
|--------|-------|
| Exact Match Accuracy | ~93-97% |
| Fuzzy Match Accuracy | ~94-98% |

## Quick Start

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model and apply LoRA adapters
base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-0.6B")
model = PeftModel.from_pretrained(base_model, "Eng-Elias/qwen3-0.6b-terminal-instruct-lora")
tokenizer = AutoTokenizer.from_pretrained("Eng-Elias/qwen3-0.6b-terminal-instruct-lora")

# Generate command
def generate_command(instruction, os_tag="[LINUX]"):
    prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{os_tag}\n\n### Response:\n"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100, do_sample=False)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("### Response:")[-1].strip()

# Example usage
print(generate_command("List all files including hidden ones", "[LINUX]"))
# Output: ls -a
```

## Supported Commands

The model can generate commands for various tasks including:

- **File Operations:** list, copy, move, delete, find files
- **Directory Operations:** create, remove, navigate directories
- **System Information:** disk usage, memory, processes
- **Text Processing:** grep, sed, awk operations
- **Network:** ping, curl, wget, netstat
- **Compression:** tar, zip, gzip operations
- **And more...**

## Input Format

The model uses an Alpaca-style prompt format:

```
### Instruction:
{natural language description}

### Input:
{OS tag: [LINUX], [WINDOWS], [MAC], or JSON request}

### Response:
{generated command}
```

### OS-Specific Commands

```python
# Linux
generate_command("Show disk usage", "[LINUX]")  # df -h

# Windows
generate_command("Show disk usage", "[WINDOWS]")  # wmic logicaldisk get size,freespace

# macOS
generate_command("Show disk usage", "[MAC]")  # df -h
```

### JSON Output (All OS)

```python
generate_command("Delete file named temp.txt", "Return the command for all operating systems as JSON")
# {"description": "Delete file named temp.txt", "linux": "rm temp.txt", "windows": "del temp.txt", "mac": "rm temp.txt"}
```

## Training Details

- **Dataset:** Custom terminal command dataset with 10000+ examples
- **Training Steps:** ~1800
- **LoRA Rank (r):** 16
- **LoRA Alpha:** 32
- **Target Modules:** q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
- **Learning Rate:** 2e-4
- **Batch Size:** 4
- **Gradient Accumulation:** 4

## Related Models

- **Merged Model:** [Eng-Elias/qwen3-0.6b-terminal-instruct](https://huggingface.co/Eng-Elias/qwen3-0.6b-terminal-instruct)

## Experiment Tracking

Training metrics and hyperparameters are logged to Weights & Biases:
- **Project:** qwen3-terminal-instruct
- **Run:** qwen3-0.6b-terminal-20251230_2244
- **Dashboard:** [View on W&B](https://wandb.ai/engelias-/qwen3-terminal-instruct/runs/3xs0ylca)

## Limitations

- Commands are based on common usage patterns; complex or obscure commands may not be accurate
- The model may occasionally generate slightly different but functionally equivalent commands
- JSON output format is consistent but may vary in structure for edge cases
- Trained primarily on English instructions

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit
- **NonCommercial** — You may not use the material for commercial purposes
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license

Full license: https://creativecommons.org/licenses/by-nc-sa-4.0/legalcode

## Citation

```bibtex
@misc{qwen3-terminal-instruct,
  author = {Eng-Elias},
  title = {Qwen3-0.6B Terminal Command Generator},
  year = {2025},
  publisher = {HuggingFace},
  url = {https://huggingface.co/Eng-Elias/qwen3-0.6b-terminal-instruct-lora}
}
```

## Acknowledgments

- [Qwen Team](https://github.com/QwenLM/Qwen) for the base model
- [Hugging Face](https://huggingface.co/) for the transformers and PEFT libraries
