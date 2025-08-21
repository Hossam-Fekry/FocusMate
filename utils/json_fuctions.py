import json
import os

def load_json(filename, default_data=None):
    """Load JSON file safely, return default_data if not found."""
    if not os.path.exists(filename):
        return default_data if default_data is not None else {}
    with open(filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    """Save dictionary to JSON file safely."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
