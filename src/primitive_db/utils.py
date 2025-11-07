import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


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


def get_table_filepath(table_name):
    return os.path.join(DATA_DIR, f"{table_name}.json")


def load_table_data(table_name):
    filepath = get_table_filepath(table_name)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    filepath = get_table_filepath(table_name)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f)


