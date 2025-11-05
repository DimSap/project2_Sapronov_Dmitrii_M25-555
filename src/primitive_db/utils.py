import json
import os


def load_metadata(filepath):
    """Load metadata dictionary from a JSON file.

    Returns an empty dict if the file does not exist.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Persist metadata dictionary to a JSON file with pretty formatting."""
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f)


