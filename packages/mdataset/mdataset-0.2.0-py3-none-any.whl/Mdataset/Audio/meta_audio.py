from transformers import AutoProcessor, SeamlessM4TModel
import torch
from IPython.display import Audio
import os

def load_seamless_m4t_model(model_name):
    processor = AutoProcessor.from_pretrained(model_name)
    model = SeamlessM4TModel.from_pretrained(model_name)
    return processor, model

def text_to_audio(model, processor, text, src_lang="eng", tgt_lang="rus", save_audio_path=None):
    if os.path.isfile(text):
        # Read the entire text from the file
        with open(text, "r", encoding="utf-8") as file:
            text = file.read()

    text_inputs = processor(text=text, src_lang=src_lang, return_tensors="pt")
    audio_array = model.generate(**text_inputs, tgt_lang=tgt_lang)[0].cpu().numpy().squeeze()

    if save_audio_path:
        save_audio(audio_array, save_audio_path)

def save_audio(audio_array, save_path):
    from scipy.io.wavfile import write
    write(save_path, 16060, audio_array)

# model_name = "facebook/hf-seamless-m4t-medium"
# processor, model = load_seamless_m4t_model(model_name)

def generate_translated_text(model, processor, text_inputs, tgt_lang="fra"):
    output_tokens = model.generate(**text_inputs, tgt_lang=tgt_lang, generate_speech=False)
    translated_text = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)
    return translated_text

def text_to_translated_text(model, processor, text_input, tgt_lang="fra", save_translated_text_path=None):
    if os.path.isfile(text_input):
        # If text_input is a file path, read the entire text from the file
        with open(text_input, "r", encoding="utf-8") as file:
            text = file.read()
    else:
        text = text_input

    text_inputs = processor(text=text, src_lang="eng", return_tensors="pt")
    translated_text = generate_translated_text(model, processor, text_inputs, tgt_lang=tgt_lang)

    if save_translated_text_path:
        save_text(translated_text, save_translated_text_path)

    return translated_text

def save_text(text, save_path):
    with open(save_path, "w", encoding="utf-8") as file:
        file.write(text)

