from openai import AzureOpenAI

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

    def transcribe(self, file):
        """
        "Transcribes a .mp3 file.
        """
        with open(file, "rb") as audio_file:
            return self._client.audio.transcriptions.create(
                model=self._model,
                file=audio_file,
                response_format="srt"
            )
        
    def translation(self, file):
        """
        "Translates a .mp3 file.
        """
        with open(file, "rb") as audio_file:
            return self._client.audio.translations.create(
                model=self._model,
                file=audio_file,
                response_format="srt"
            )