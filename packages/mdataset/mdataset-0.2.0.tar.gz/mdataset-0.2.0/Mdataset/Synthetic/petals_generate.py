import torch
from transformers import AutoTokenizer
from petals import AutoDistributedModelForCausalLM

def generate_text(model_name, use_cuda=True):
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False, add_bos_token=False)
    model = AutoDistributedModelForCausalLM.from_pretrained(model_name)

    if use_cuda:
        model = model.cuda()

    inputs = tokenizer('A cat in French is "', return_tensors="pt")["input_ids"].cpu()

    if use_cuda:
        inputs = inputs.cuda()

    outputs = model.generate(inputs, max_new_tokens=3)
    return tokenizer.decode(outputs[0])