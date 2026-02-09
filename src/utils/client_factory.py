import os
from openai import AzureOpenAI

def azure_openai_client():
    return AzureOpenAI(
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_KEY"),
        api_version="2024-06-01"
    )