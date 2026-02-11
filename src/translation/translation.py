from src.utils.get_root_path import get_root_path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def translate(text: str):
    """
    Translates a text.
    """
    root = get_root_path()
    local_dir = f"{root}/local_models"
    tokenizer = AutoTokenizer.from_pretrained(local_dir)
    model = AutoModelForSeq2SeqLM.from_pretrained(local_dir)
    input = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**input)
    translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
    return translated_text[0]