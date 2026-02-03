from pathlib import Path

def get_root_path():
    """
    Get the path of the project root.
    """
    return Path(__file__).resolve().parent.parent.parent