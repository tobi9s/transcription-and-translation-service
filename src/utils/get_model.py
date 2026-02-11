import os
import httpx
from src.utils.get_root_path import get_root_path
from huggingface_hub import set_client_factory
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def get_model(model_name: str):
    """
    Downloads the model from HuggingFace.
    """
    root = get_root_path()
    local_dir = f"{root}/local_models"
    os.environ["HF_HUB_CACHE"] = f"{root}/models"
    set_client_factory(client_factory=lambda: httpx.Client(verify=False))
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(local_dir)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.save_pretrained(local_dir)