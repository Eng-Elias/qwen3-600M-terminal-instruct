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

# Qwen3-0.6B Terminal Command Generator

A fine-tuned Qwen3-0.6B model for generating terminal commands from natural language instructions. Supports Linux, Windows, and macOS.

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

# Load model (base + adapters)
base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-0.6B")
model = PeftModel.from_pretrained(base_model, "Eng-Elias/qwen3-0.6b-terminal-instruct")
tokenizer = AutoTokenizer.from_pretrained("Eng-Elias/qwen3-0.6b-terminal-instruct")

# Generate command
def generate_command(instruction, os_tag="[LINUX]"):
    prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{os_tag}\n\n### Response:\n"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100, do_sample=False)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("### Response:")[-1].strip()

# Examples
print(generate_command("List all files including hidden ones", "[LINUX]"))
# Output: ls -a

print(generate_command("Create a new folder named projects", "[WINDOWS]"))
# Output: mkdir projects

print(generate_command("Show disk usage", "[MAC]"))
# Output: df -h
```

## Features

### OS-Specific Commands

Generate commands tailored for specific operating systems:

```python
# Linux
generate_command("Find all Python files", "[LINUX]")
# find . -name '*.py'

# Windows  
generate_command("Find all Python files", "[WINDOWS]")
# dir /s /b *.py

# macOS
generate_command("Find all Python files", "[MAC]")
# find . -name '*.py'
```

### JSON Output (All OS)

Get commands for all operating systems in JSON format:

```python
generate_command("Delete file named temp.txt", "Return the command for all operating systems as JSON")
```

Output:
```json
{
  "description": "Delete file named temp.txt",
  "linux": "rm temp.txt",
  "windows": "del temp.txt",
  "mac": "rm temp.txt"
}
```

## Supported Command Categories

| Category | Examples |
|----------|----------|
| **File Operations** | list, copy, move, delete, find, rename |
| **Directory Operations** | create, remove, navigate, list contents |
| **System Info** | disk usage, memory, CPU, processes |
| **Text Processing** | grep, sed, awk, sort, uniq |
| **Network** | ping, curl, wget, netstat, ssh |
| **Compression** | tar, zip, gzip, unzip |
| **Permissions** | chmod, chown, icacls |
| **Package Management** | apt, yum, brew, choco |

## Prompt Format

The model uses an Alpaca-style prompt format:

```
### Instruction:
{natural language description of the command}

### Input:
{OS tag or special request}

### Response:
{generated terminal command}
```

### Input Options

| Input | Description |
|-------|-------------|
| `[LINUX]` | Generate Linux/Unix command |
| `[WINDOWS]` | Generate Windows command |
| `[MAC]` | Generate macOS command |
| `Return the command for all operating systems as JSON` | Get JSON with all OS commands |

## Training Details

| Parameter | Value |
|-----------|-------|
| Dataset | Custom terminal command dataset with 10000+ examples |
| Base Model | Qwen/Qwen3-0.6B |
| Method | QLoRA (4-bit NF4) |
| LoRA Rank | 16 |
| LoRA Alpha | 32 |
| Target Modules | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj |
| Learning Rate | 2e-4 |
| Training Steps | ~1800 |
| Batch Size | 4 (×4 gradient accumulation) |

## Related Models

- **LoRA Adapters:** [Eng-Elias/qwen3-0.6b-terminal-instruct-lora](https://huggingface.co/Eng-Elias/qwen3-0.6b-terminal-instruct-lora)

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
  url = {https://huggingface.co/Eng-Elias/qwen3-0.6b-terminal-instruct}
}
```

## Acknowledgments

- [Qwen Team](https://github.com/QwenLM/Qwen) for the base model
- [Hugging Face](https://huggingface.co/) for the transformers and PEFT libraries
