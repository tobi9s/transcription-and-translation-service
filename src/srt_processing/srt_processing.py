import re
from datetime import timedelta
from pydub import AudioSegment
from src.utils.get_root_path import get_root_path
import pysrt
import os

def _parse_srt_time(t):
    """
    Parses srt time.

    Internal use only.
    """
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    return timedelta(hours=int(h), minutes=int(m), seconds=int(s), milliseconds=int(ms))


def _format_srt_time(td):
    """
    Formats srt time.

    Internal use only.
    """
    total_ms = int(td.total_seconds() * 1000)
    h = total_ms // 3_600_000
    total_ms %= 3_600_000
    m = total_ms // 60_000
    total_ms %= 60_000
    s = total_ms // 1_000
    ms = total_ms % 1_000
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def _shift_srt(content, offset_td, start_index):
    """
    Shifts srt.

    Internal use only.
    """
    blocks = re.split(r"\n\s*\n", content.strip())
    out_blocks = []
    idx = start_index
    for b in blocks:
        lines = b.splitlines()
        if len(lines) < 3:
            continue
        time_line = lines[1]
        start_str, end_str = time_line.split(" --> ")
        start = _parse_srt_time(start_str) + offset_td
        end = _parse_srt_time(end_str) + offset_td
        new_time_line = f"{_format_srt_time(start)} --> {_format_srt_time(end)}"
        text_lines = lines[2:]
        out_blocks.append("\n".join([str(idx), new_time_line, *text_lines]))
        idx += 1
    return "\n\n".join(out_blocks), idx

def srt_merge(srt_files, audio_files, output_path):
    """
    Merges srt files.
    """
    durations = [AudioSegment.from_file(a).duration_seconds for a in audio_files]
    offsets = [0]
    for d in durations[:-1]:
        offsets.append(offsets[-1] + d)
    merged_blocks = []
    current_index = 1
    for srt_file, offset_sec in zip(srt_files, offsets):
        with open(srt_file, "r", encoding="utf-8") as f:
            content = f.read()
        shifted, current_index = _shift_srt(content, timedelta(seconds=offset_sec), current_index)
        merged_blocks.append(shifted)
    merged = "\n\n".join(merged_blocks)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(merged)

def srt_extract(srt_file):
    """
    Extracts the text of a .srt file.
    """
    root = get_root_path()
    file = f"{root}/data/merged/{srt_file}.srt"
    if os.path.exists(file) is False:
        raise FileNotFoundError(f"File not found: {file}")
    try:
        srt = pysrt.open(file)
        return [s.text for s in srt]
    except Exception as e:
        print(f"Couldnt extract text from {file}: {str(e)}")