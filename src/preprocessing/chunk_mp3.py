from pydub import AudioSegment
from src.utils.get_root_path import get_root_path
import os

def chunk_mp3(input_mp3: str):
    """
    Chunks a .mp3 for easier processing.
    """
    root = get_root_path()
    input_file = f"{root}/data/input/{input_mp3}.mp3"
    if os.path.exists(input_file) is False:
        raise FileNotFoundError(f"File not found: {input_file}")
    mp3 = AudioSegment.from_file(input_file, format="mp3")
    chunk_ms = 10 * 60 * 500
    for i in range(0, len(mp3), chunk_ms):
        part = mp3[i:i+chunk_ms]
        part.export(f"{root}/data/chunks/{input_mp3}_chunk_{i//chunk_ms + 1}.mp3", format="mp3")