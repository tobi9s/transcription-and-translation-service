# Transcription & Translation Service

Author: Tobias Nguyen

This repository contains the code for an AI-powered transcription and translation service utilizing Azure OpenAIs [Whisper model](https://developers.openai.com/api/docs/guides/speech-to-text/) and [HuggingFace Transformers](https://huggingface.co/docs/transformers/en/index).

The programme takes an input ```.mp4``` file and is able to create subtitles in a ```.srt``` format in the source language, English or a completly different target language that can be burned into the ```.mp4``` with standard video editing software.

## Project structure
```
transcription-and-translation-service/
│── src/
│   │   ├── azure_openai_client/            # Transcription & translation with Azure OpenAI
│   │   │   ├── __init__.py
│   │   │   ├── azure_openai_client.py
│   │   ├── preprocessing/                  # .mp4 file processing
│   │   │   ├── __init__.py
│   │   │   ├── chunk_mp3.py
│   │   │   ├── mp4_to_mp3.py
│   │   ├── srt_processing/                 # .srt file processing
│   │   │   ├── __init__.py
│   │   │   ├── srt_processing.py
│   │   ├── translation_client/             # Translation with HuggingFace Transformers
│   │   │   ├── __init__.py
│   │   │   ├── translation_client.py
│   │   ├── utils/                          # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── client_factory.py
│   │   │   ├── get_env.py
│   │   │   ├── get_root_path.py
│   │   ├── main.py
│── .gitignore
│── .python-version
│── main.py                                 # Programme entry point
│── pyproject.toml
│── README.md
│── uv.lock
```

## Getting started

Before starting on this project, please make sure to have all necessary applications installed.

- [Python 3.12](https://www.python.org/downloads/release/python-3120/) - the programming language this project has been written with.
- [uv](https://docs.astral.sh/uv/) - a high-speed package and project manager for Python.
- [ffmpeg](https://www.ffmpeg.org/) - a framework to work with audio and video formats.

After these three applications have been installed, please follow the next steps:


**Step 1: uv setup**
```bash
# Create a Python virtual environment
uv venv

# Activate the environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Download all the necessary dependencies
uv sync
```

**Step 2: Project setup**

Please create a .env file with the following fields:
```Python
AZURE_OPENAI_ENDPOINT = ""              # The endpoint of the Azure OpenAI instance
AZURE_OPENAI_KEY = ""                   # The API key to the Azure OpenAI instance
AZURE_OPENAI_WHISPER_DEPLOYMENT = ""    # The speech model to use for Azure OpenAI
AZURE_OPENAI_VERSION = ""               # The version of the Azure OpenAI API
HF_MODEL = ""                           # The HuggingFace model to be downloaded and used
```

Additionally. a folder ```data/``` with a subfolder ```input``` is to be created which contains an input ```.mp4``` file.

```
mkdir data
cd data
mkdir input
```

**Put the ```.mp4``` file into the ```input/``` folder, otherwise the programme won't work!**

## Usage

In order to use the project, run the following two commands:

```bash
# Activate the environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Run the main.py file
python main.py
```

Also, there a more functionalities to be aware of:

### Preprocessing

All the methods for transcribing and translating content cannot take ```.mp4``` files as an input which is why the ```.mp4``` files need to be processed into ```.mp3``` files first before being able to be transcribed and translated.

This can be seen when using the programme as it tells the user to preprocess the ```.mp4``` file first before using the other methods.

### AzureOpenAIClient

This project contains a ```AzureOpenAIClient``` class which is essentially a wrapper behind the original ```AzureOpenAI``` class from the ```openai``` library.

The class contains two methods:
```Python
transcribe(self, file_name: str)

translate(self, file_name: str)
```
```transcribe()``` takes a ```.mp3``` file, transcribes it and outputs a ```.srt``` file. For example, if a German audio file is put into this method, a German transcription of that audio will be created.

```translate()``` takes a ```.mp3``` file, translated it into English and outputs a ```.srt``` file. For example, if a German audio file is put into this method, an English transcription of that audio will be created. This method can only create English transcriptions.

### TranslationClient

There is a ```TranslationClient``` class which takes a ```.srt``` file from a certain source language and translates the text from that file into a different target language with the following method:
```
translate(self, text: str)
```
For example, if the source language is English and the target language is German, the expected input is an English ```.srt``` file and a German ```.srt``` file will be created where the German text can replace the English text in order to get a translated transcription.

Ideally, an English transcription should be created first using the ```translate(self, file_name: str)``` method from the ```AzureOpenAIClient``` class and the resulting ```.srt``` output should be used in the ```translate(self, text: str)``` method from the ```TranslationClient``` class as a lot of HuggingFace models expect an English input.

## Good to know

- The programme does not support standard ```pip```.
- The HuggingFace model can be easily replaced, just change the name in the ```.env``` file.
- Although the HuggingFace model can be easily replaced, be careful of potential changes in the expected source language and the outputted target language.
- The ```TranslationClient``` class only works with HuggingFace Models that are compatible with the ```transformers``` library. Other model types such as Fairseq are not supported.
- Beware of the cost associated with calling the Azure OpenAI API.
- **The end result of all transcription and translation methods are ```.srt``` files. If you want to burn them into a ```.mp4``` file, you need to do it in a video editing programme or similar.**