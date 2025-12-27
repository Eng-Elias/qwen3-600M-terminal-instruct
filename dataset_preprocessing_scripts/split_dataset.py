"""
split_dataset.py
Splits the full dataset into train, dev, and test sets.
"""

import json
import random
from pathlib import Path

def split_dataset(data: list, train_ratio=0.85, dev_ratio=0.10, test_ratio=0.05, seed=42):
    """Split data into train, dev, test sets."""
    random.seed(seed)
    random.shuffle(data)
    
    total = len(data)
    train_end = int(total * train_ratio)
    dev_end = train_end + int(total * dev_ratio)
    
    return {
        "train": data[:train_end],
        "dev": data[train_end:dev_end],
        "test": data[dev_end:]
    }

def main():
    merged_path = Path("datasets/generated/merged/full_dataset.json")
    processed_dir = Path("datasets/generated/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    if not merged_path.exists():
        print(f"File not found: {merged_path}")
        return

    with open(merged_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Total examples: {len(data)}")
    
    splits = split_dataset(data)
    
    for split_name, split_data in splits.items():
        output_path = processed_dir / f"{split_name}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(split_data, f, indent=2, ensure_ascii=False)
        print(f"{split_name}: {len(split_data)} examples -> {output_path}")

if __name__ == "__main__":
    main()
