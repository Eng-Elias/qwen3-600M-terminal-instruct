# Qwen3-0.6B Terminal Command Generator

A fine-tuned Qwen3-0.6B model that generates terminal commands from natural language instructions. Supports **Linux**, **Windows**, and **macOS**.

## 🎯 Project Overview

This project fine-tunes a [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) language model using **QLoRA** (Quantized Low-Rank Adaptation) to generate accurate terminal commands from natural language descriptions.

### Key Features

- **Multi-OS Support**: Generates commands for Linux, Windows, and macOS
- **JSON Output**: Can return commands for all operating systems in JSON format
- **High Accuracy**: Achieves ~93-97% exact match accuracy
- **Efficient Training**: Uses QLoRA for memory-efficient fine-tuning

## 📊 Performance

| Metric | Score |
|--------|-------|
| Exact Match Accuracy | ~93-97% |
| Fuzzy Match Accuracy | ~94-98% |

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Eng-Elias/qwen3-600M-terminal-instruct.git
cd qwen3-600M-terminal-instruct

# Install dependencies
pip install -r requirements.txt

# For CUDA support the command in cuda_requirements.txt
```

### Using the Model

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model from HuggingFace
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

### JSON Output (All OS)

```python
generate_command("Delete file named temp.txt", "Return the command for all operating systems as JSON")
# Output: {"description": "Delete file named temp.txt", "linux": "rm temp.txt", "windows": "del temp.txt", "mac": "rm temp.txt"}
```

## 📁 Project Structure

```
qwen3-600M-terminal-instruct/
├── notebooks/
│   ├── 01_train_evaluate_publish.ipynb  # Training and evaluation
│   ├── 02_evaluate_all_sources.ipynb    # Evaluate from all sources
│   ├── 03_load_and_test_all.ipynb       # Interactive testing
│   └── 04_push_model_cards.ipynb        # Push model cards to HF
├── dataset/
│   └── generated/                        # Training data
├── dataset_preprocessing_scripts/        # Data preparation scripts
├── model_cards/                          # HuggingFace model cards
├── outputs/
│   ├── lora_adapters/                   # Trained LoRA adapters
│   ├── merged_model/                    # Merged model
│   └── eval_results/                    # Evaluation results
├── requirements.txt                      # Python dependencies
├── cuda_requirements.txt                 # CUDA dependencies
└── README.md                            # This file
```

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| `01_train_evaluate_publish.ipynb` | Main training pipeline: loads data, trains model, evaluates, and publishes to HuggingFace |
| `02_evaluate_all_sources.ipynb` | Evaluates model from 4 sources: local adapters, local merged, HF adapters, HF merged |
| `03_load_and_test_all.ipynb` | Interactive testing playground for all model sources |
| `04_push_model_cards.ipynb` | Pushes README/model cards to HuggingFace repositories |

## 🔧 Training Details

| Parameter | Value |
|-----------|-------|
| Base Model | Qwen/Qwen3-0.6B |
| Method | QLoRA (4-bit NF4 quantization) |
| Dataset | Custom terminal command dataset (10000+ examples) |
| LoRA Rank (r) | 16 |
| LoRA Alpha | 32 |
| Target Modules | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj |
| Learning Rate | 2e-4 |
| Training Steps | ~1800 |
| Batch Size | 4 (×4 gradient accumulation) |

## 🌐 HuggingFace Models

| Repository | Description |
|------------|-------------|
| [Eng-Elias/qwen3-0.6b-terminal-instruct](https://huggingface.co/Eng-Elias/qwen3-0.6b-terminal-instruct) | Main model repository |
| [Eng-Elias/qwen3-0.6b-terminal-instruct-lora](https://huggingface.co/Eng-Elias/qwen3-0.6b-terminal-instruct-lora) | LoRA adapters only |

## 📋 Supported Command Categories

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

## ⚠️ Limitations

- Commands are based on common usage patterns; complex or obscure commands may not be accurate
- The model may occasionally generate slightly different but functionally equivalent commands
- JSON output format is consistent but may vary in structure for edge cases
- Trained primarily on English instructions

## 📄 License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit
- **NonCommercial** — You may not use the material for commercial purposes
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license

Full license: https://creativecommons.org/licenses/by-nc-sa-4.0/legalcode

## 📚 Citation

```bibtex
@misc{qwen3-terminal-instruct,
  author = {Eng-Elias},
  title = {Qwen3-0.6B Terminal Command Generator},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/Eng-Elias/qwen3-600M-terminal-instruct}
}
```

## 🙏 Acknowledgments

- [Qwen Team](https://github.com/QwenLM/Qwen) for the base model
- [Hugging Face](https://huggingface.co/) for the transformers and PEFT libraries
- [Ready Tensor](https://www.readytensor.ai/) for the LLM Engineering and Deployment program

## 👤 Author

**Eng. Elias Owis**

- GitHub: [@Eng-Elias](https://github.com/Eng-Elias)
- HuggingFace: [Eng-Elias](https://huggingface.co/Eng-Elias)
