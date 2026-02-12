from src.utils.get_root_path import get_root_path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from huggingface_hub import set_client_factory
import os
import httpx

class TranslationClient:
    def __init__(self, model: str):
        self.model = model
        self._local_dir = os.path.join(
            get_root_path(),
            "local_models",
            self._sanitize_model_name(model)
        )
        if not os.path.exists(self._local_dir):
            self._get_model()
        self._tokenizer = AutoTokenizer.from_pretrained(self._local_dir)
        self._model_instance = AutoModelForSeq2SeqLM.from_pretrained(self._local_dir)

    def _sanitize_model_name(self, model_name):
        """
        Replaces slashes with an underscore.
        
        Internal use only.
        """
        return model_name.replace("/", "_")

    def _get_model(self):
        """
        Downloads the model from HuggingFace.

        Internal use only.
        """
        os.environ["HF_HUB_CACHE"] = f"{get_root_path()}/models"
        set_client_factory(client_factory=lambda: httpx.Client(verify=False))
        tokenizer = AutoTokenizer.from_pretrained(self.model)
        tokenizer.save_pretrained(self._local_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.model)
        model.save_pretrained(self._local_dir)

    def translate(self, text: str):
        """
        Translates a text using the downloaded model.
        """
        inputs = self._tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = self._model_instance.generate(**inputs)
        translated_text = self._tokenizer.batch_decode(translated, skip_special_tokens=True)
        return translated_text[0]