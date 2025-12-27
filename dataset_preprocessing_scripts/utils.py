"""
utils.py
Helper functions for data processing scripts.
"""

import json
from pathlib import Path
from typing import Any, Union

def load_json(filepath: Union[str, Path]) -> Any:
    """Load data from a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: Any, filepath: Union[str, Path], indent: int = 2) -> None:
    """Save data to a JSON file."""
    # Ensure directory exists
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

def ensure_dir(path: Union[str, Path]) -> None:
    """Ensure a directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)
