from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
from src.utils.get_root_path import get_root_path
import os

def mp4_with_subtitles(mp4_name: str, srt_name: str):
    """
    Burns .srt subtitles into a .mp4 file.
    """
    root = get_root_path()
    mp4_file = f"{root}/data/input/{mp4_name}.mp4"
    srt_file = f"{root}/data/merged/{srt_name}.srt"
    if os.path.exists(mp4_file) is False or os.path.exists(srt_file) is False:
        raise FileNotFoundError(f"One or both file not found: {mp4_file}, {srt_file}")
    try:
        video = VideoFileClip(mp4_file)
        generator = lambda txt: TextClip(txt, font="arial", fontsize=50, color="white", method='caption', size=video.size)
        subtitles = SubtitlesClip(srt_file, make_textclip=generator)
        result = CompositeVideoClip([video, subtitles])
        result.write_videofile(f"{root}/data/results/{mp4_name}_{srt_name}.mp4")
    except Exception as e:
        print(f"Something went wrong: {str(e)}")