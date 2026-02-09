from openai import AzureOpenAI
from src.utils.get_root_path import get_root_path
import os

class AzureOpenAIClient:
    def __init__(self, api_key: str, endpoint: str, version: str, model: str):
        self._api_key = api_key
        self._endpoint = endpoint
        self._version = version
        self._model = model
        self._client = AzureOpenAI(
            api_key=self._api_key,
            azure_endpoint=self._endpoint,
            api_version=self._version
        )

    def _save_files(self, file_name: str, suffix: str, result):
        """
        Saves files into a certain directory.

        Internal use only.
        """
        root = get_root_path()
        dir = f"{root}/data/{suffix}/"
        os.makedirs(dir, exist_ok=True)
        file_path = os.path.join(dir, f"{file_name}_{suffix}.srt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result)

    def transcribe(self, file_name: str):
        """
        "Transcribes a .mp3 file.
        """
        root = get_root_path()
        input_file = f"{root}/data/chunks/{file_name}.mp3"
        if os.path.exists(input_file) is False:
            raise FileNotFoundError(f"File not found: {input_file}")
        try:
            with open(input_file, "rb") as audio_file:
                result = self._client.audio.transcriptions.create(
                    model=self._model,
                    file=audio_file,
                    response_format="srt"
                )
                self._save_files(file_name, "transcription", result)
                return result
        except Exception as e:
            print(f"Something went wrong: {str(e)}")
        
    def translate(self, file_name: str):
        """
        "Translates a .mp3 file.
        """
        root = get_root_path()
        input_file = f"{root}/data/chunks/{file_name}.mp3"
        if os.path.exists(input_file) is False:
            raise FileNotFoundError(f"File not found: {input_file}")
        try:
            with open(input_file, "rb") as audio_file:
                result = self._client.audio.translations.create(
                    model=self._model,
                    file=audio_file,
                    response_format="srt"
                )
                self._save_files(file_name, "translation", result)
                return result
        except Exception as e:
            print(f"Something went wrong: {str(e)}")