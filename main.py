from src.utils.client_factory import create_azure_openai_client, create_translation_client
from src.preprocessing.chunk_mp3 import chunk_mp3
from src.preprocessing.mp4_to_mp3 import mp4_to_mp3
from src.srt_processing.srt_processing import srt_merge, srt_extract, srt_replace_text
from src.utils.get_root_path import get_root_path
import os

def main():
    """
    Runs the main logic of the project.
    """
    root = get_root_path()
    dirs = ["chunks", "merged", "results", "transcription", "translation"]
    for d in dirs:
        if not os.path.exists(f"{root}/data/{d}"):
            os.makedirs(f"{root}/data/{d}")
    while True:
        print("Select operation:")
        print("1 - process a .mp4 into a .mp3 file so all other operations be used - Please use this operation if the other operations have not been used yet.")
        print("2 - transcribe a .mp3 file in its original language into a .srt file.")
        print("3 - translate a .mp3 file from a source language to English into a .srt file.")
        print("4 - translate a .mp3 file from a source language (usually English) to a target language using a HuggingFace Model into a .srt file.")
        print("5 - exit the programme.")
        operation = input()
        match operation:
            case "1":
                print(f"Enter the .mp4 file name from {root}/data/input (without extension)")
                file = input()
                print(f"Proceeding with {file}.mp4")
                mp4_to_mp3(file)
                chunk_mp3(file)
                print(f"Successfully processed {file}.mp4 into .mp3 chunks!")
            case "2":
                azure_openai_client = create_azure_openai_client()
                chunk_path = f"{root}/data/chunks"
                for file in os.listdir(chunk_path):
                    if file.endswith(".mp3"):
                        name = os.path.splitext(file)[0]
                        print(f"Processing file: {file}")
                        azure_openai_client.transcribe(name)
                    audio_dir = f"{root}/data/chunks"
                    audio_files = [os.path.join(audio_dir, fname) for fname in os.listdir(audio_dir) if fname.endswith(".mp3")]
                    transcription_dir = f"{root}/data/transcription"
                    transcription_files = [os.path.join(transcription_dir, fname) for fname in os.listdir(transcription_dir) if fname.endswith(".srt")]
                    srt_merge(transcription_files, audio_files, f"{root}/data/merged/transcription.srt")
                    print("Successfully transcribed .mp3 file into a .srt file!")
                    print(f"The file can be found at {root}/data/merged/transcription.srt!")
            case "3":
                azure_openai_client = create_azure_openai_client()
                chunk_path = f"{root}/data/chunks"
                for file in os.listdir(chunk_path):
                    if file.endswith(".mp3"):
                        name = os.path.splitext(file)[0]
                        print(f"Processing file: {file}")
                        azure_openai_client.translate(name)
                    audio_dir = f"{root}/data/chunks"
                    audio_files = [os.path.join(audio_dir, fname) for fname in os.listdir(audio_dir) if fname.endswith(".mp3")]
                    translation_dir = f"{root}/data/translation"
                    translation_files = [os.path.join(translation_dir, fname) for fname in os.listdir(translation_dir) if fname.endswith(".srt")]
                    srt_merge(translation_files, audio_files, f"{root}/data/merged/translation.srt")
                    print("Successfully translated .mp3 file into a .srt file!")
                    print(f"The file can be found at {root}/data/merged/translation.srt!")
            case "4":
                translation_client = create_translation_client()
                texts = srt_extract("translation")
                translated_texts = []
                for text in texts:
                    translated_texts.append(translation_client.translate(text))
                srt_replace_text("translation", translated_texts)
                print("Successfully translated the .mp3 file into the target language!")
                print(f"The file can be found at {root}/data/results/translation.srt")
            case "5":
                print("Exiting programme")
                return
            case _:
                print(("Invalid operation!"))

if __name__ == "__main__":
    main()