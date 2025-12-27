"""
convert_to_alpaca.py
Converts validated data to Alpaca format for training.
"""

import json
import random
from pathlib import Path
from typing import List, Dict

def create_single_os_examples(entry: dict) -> List[dict]:
    """Create 3 examples (one per OS) from a single entry."""
    examples = []
    
    os_mapping = {
        "linux": entry["linux"],
        "windows": entry["windows_cmd"],
        "mac": entry["mac"]
    }
    
    for os_name, command in os_mapping.items():
        # Format 1: Explicit OS tag in input
        examples.append({
            "instruction": entry["instruction"],
            "input": f"[{os_name.upper()}]",
            "output": command
        })
        
        # Format 2: OS mentioned in instruction (50% of the time)
        if random.random() < 0.5:
            os_phrases = {
                "linux": ["on Linux", "in Linux", "using Linux", "for Linux"],
                "windows": ["on Windows", "in Windows", "using Windows CMD", "for Windows"],
                "mac": ["on Mac", "on macOS", "using Mac terminal", "for macOS"]
            }
            phrase = random.choice(os_phrases[os_name])
            examples.append({
                "instruction": f"{entry['instruction']} {phrase}",
                "input": "",
                "output": command
            })
    
    return examples

def create_json_output_example(entry: dict) -> dict:
    """Create JSON output format example."""
    json_output = {
        "description": entry["instruction"],
        "linux": entry["linux"],
        "windows": entry["windows_cmd"],
        "mac": entry["mac"]
    }
    
    # Vary the input phrases
    input_phrases = [
        "Return the command for all operating systems as JSON",
        "Give me commands for all platforms in JSON format",
        "Output as JSON with commands for Linux, Windows, and Mac",
        "Return JSON with multi-platform commands",
        "Format: JSON"
    ]
    
    return {
        "instruction": entry["instruction"],
        "input": random.choice(input_phrases),
        "output": json.dumps(json_output, ensure_ascii=False)
    }

def convert_category_to_alpaca(entries: List[dict]) -> List[dict]:
    """Convert all entries in a category to Alpaca format."""
    alpaca_data = []
    
    for entry in entries:
        # Add single OS examples (3 per entry)
        alpaca_data.extend(create_single_os_examples(entry))
        
        # Add JSON format example (1 per entry)
        alpaca_data.append(create_json_output_example(entry))
        
        # Add additional JSON format example with different phrasing (50% chance)
        if random.random() < 0.5:
            alpaca_data.append(create_json_output_example(entry))
    
    return alpaca_data

def main():
    validated_dir = Path("datasets/generated/validated")
    processed_dir = Path("datasets/generated/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    if not validated_dir.exists():
        print(f"Directory not found: {validated_dir}")
        return

    all_alpaca_data = []
    
    for filepath in validated_dir.glob("*.json"):
        if "_issues" in filepath.name:
            continue
            
        print(f"Converting: {filepath.name}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            entries = json.load(f)
        
        alpaca_entries = convert_category_to_alpaca(entries)
        all_alpaca_data.extend(alpaca_entries)
        
        print(f"  Generated {len(alpaca_entries)} Alpaca examples from {len(entries)} entries")
    
    print(f"\nTotal Alpaca examples: {len(all_alpaca_data)}")
    
    # Shuffle all data
    random.shuffle(all_alpaca_data)
    
    # Save merged dataset
    merged_dir = Path("datasets/generated/merged")
    merged_dir.mkdir(parents=True, exist_ok=True)
    
    with open(merged_dir / "full_dataset.json", 'w', encoding='utf-8') as f:
        json.dump(all_alpaca_data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved to: {merged_dir / 'full_dataset.json'}")

if __name__ == "__main__":
    main()
