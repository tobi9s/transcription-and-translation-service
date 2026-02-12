from moviepy import VideoFileClip
from src.utils.get_root_path import get_root_path
import os

def mp4_to_mp3(input_mp4_name: str):
    """
    Convert a .mp4 file into a .mp3 file. 
    """
    root = get_root_path()
    input_file = f"{root}/data/input/{input_mp4_name}.mp4"
    if os.path.exists(input_file) is False:
        raise FileNotFoundError(f"File not found: {input_file}")
    try:
        mp4 = VideoFileClip(input_file)
        output_file = f"{root}/data/input/{input_mp4_name}.mp3"
        mp4.audio.write_audiofile(output_file)
    except Exception as e:
        raise RuntimeError(f"Couldnt convert the .mp4 file: {str(e)}")