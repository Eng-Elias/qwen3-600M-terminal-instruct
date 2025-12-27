"""
stats.py
Generate statistics for the final dataset.
"""

import json
from pathlib import Path
from collections import Counter

def get_stats(data):
    stats = {
        "total": len(data),
        "os_distribution": Counter(),
        "json_outputs": 0,
        "instruction_lengths": [],
        "output_lengths": []
    }
    
    for item in data:
        # Check OS tag
        if "[LINUX]" in item["input"]:
            stats["os_distribution"]["linux"] += 1
        elif "[WINDOWS]" in item["input"]:
            stats["os_distribution"]["windows"] += 1
        elif "[MAC]" in item["input"]:
            stats["os_distribution"]["mac"] += 1
        elif "JSON" in item["input"]:
            stats["json_outputs"] += 1
        else:
            stats["os_distribution"]["implicit"] += 1
        
        stats["instruction_lengths"].append(len(item["instruction"]))
        stats["output_lengths"].append(len(item["output"]))
    
    if stats["instruction_lengths"]:
        stats["avg_instruction_length"] = sum(stats["instruction_lengths"]) / len(stats["instruction_lengths"])
    else:
        stats["avg_instruction_length"] = 0

    if stats["output_lengths"]:
        stats["avg_output_length"] = sum(stats["output_lengths"]) / len(stats["output_lengths"])
    else:
        stats["avg_output_length"] = 0
    
    return stats

def main():
    for split in ["train", "dev", "test"]:
        path = Path(f"datasets/generated/processed/{split}.json")
        if not path.exists():
            print(f"File not found: {path}")
            continue

        with open(path) as f:
            data = json.load(f)
        
        stats = get_stats(data)
        print(f"\n=== {split.upper()} ===")
        print(f"Total examples: {stats['total']}")
        print(f"OS distribution: {dict(stats['os_distribution'])}")
        print(f"JSON outputs: {stats['json_outputs']}")
        print(f"Avg instruction length: {stats['avg_instruction_length']:.1f} chars")
        print(f"Avg output length: {stats['avg_output_length']:.1f} chars")

if __name__ == "__main__":
    main()
