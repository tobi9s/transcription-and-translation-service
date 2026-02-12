import os
from src.azure_openai_client.azure_openai_client import AzureOpenAIClient
from src.translation_client.translation_client import TranslationClient

def create_azure_openai_client():
    """
    Initializes an instance of AzureOpenAIClient.
    """
    return AzureOpenAIClient(
        api_key=os.environ.get("AZURE_OPENAI_KEY"),
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        version=os.environ.get("AZURE_OPENAI_VERSION"),
        model=os.environ.get("AZURE_OPENAI_WHISPER_DEPLOYMENT")
    )

def create_translation_client():
    """
    Initializes an instance of TranslationClient.
    """
    return TranslationClient(
        model=os.environ.get("HF_MODEL")
    )