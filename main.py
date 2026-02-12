from src.utils.client_factory import create_azure_openai_client, create_translation_client
from src.preprocessing.chunk_mp3 import chunk_mp3
from src.preprocessing.mp4_to_mp3 import mp4_to_mp3
from src.srt_processing.srt_processing import srt_merge, srt_extract, srt_replace_text
from src.utils.get_root_path import get_root_path
import os

def main():
    root = get_root_path()
    azure_openai_client = create_azure_openai_client()
    translation_client = create_translation_client()
    print("Enter the .mp4 file name from data/input:")
    input_file = input()
    mp4_to_mp3(input_file)
    print(f"Converted {input_file}.mp4 to .mp3!")
    chunk_mp3(input_file)
    print(f"Chunked {input_file}.mp3!")
    chunk_path = f"{root}/data/chunks"
    for file in os.listdir(chunk_path):
        if file.endswith(".mp3"):
            name = os.path.splitext(file)[0]
            print(f"Processing file: {file}")
            azure_openai_client.transcribe(name)
            azure_openai_client.translate(name)
    audio_dir = f"{root}/data/chunks"
    audio_files = [
        os.path.join(audio_dir, fname)
        for fname in os.listdir(audio_dir)
        if fname.endswith(".mp3")
    ]
    transcription_dir = f"{root}/data/transcription"
    transcription_files = [
        os.path.join(transcription_dir, fname)
        for fname in os.listdir(transcription_dir)
        if fname.endswith(".srt")
    ]
    srt_merge(transcription_files, audio_files, f"{root}/data/merged/transcription.srt")
    print("Merged all transcription snippets!")
    translation_dir = f"{root}/data/translation"
    translation_files = [
        os.path.join(translation_dir, fname)
        for fname in os.listdir(translation_dir)
        if fname.endswith(".srt")
    ]
    srt_merge(translation_files, audio_files, f"{root}/data/merged/translation.srt")
    print("Merged all translation snippets!")
    print("Created subtitles!")
    texts = srt_extract("translation")
    translated_texts = []
    for text in texts:
        translated_texts.append(translation_client.translate(text))
    srt_replace_text("translation", translated_texts)
    print("Finished!")

if __name__ == "__main__":
    main()