import torch
from transformers import AutoTokenizer
from petals import AutoDistributedModelForCausalLM

def load_petals(model_name, use_cuda=True):
    """
    Load a causal language model for text generation.

    Parameters:
    - model_name (str): The name or path of the pre-trained language model.
    - use_cuda (bool): If True, the model will be loaded onto a CUDA device.

    Returns:
    - model: The loaded causal language model.
    - tokenizer: The tokenizer associated with the loaded model.

    Example:
    >>> model, tokenizer = load_causal_lm_model('gpt2', use_cuda=True)
    """

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False, add_bos_token=False)
    model = AutoDistributedModelForCausalLM.from_pretrained(model_name)

    if use_cuda:
        model = model.cuda()

    return model, tokenizer


def generate_text(model, tokenizer, use_cuda=True):
    """
    Generate text using a causal language model.

    Parameters:
    - model (AutoDistributedModelForCausalLM): The loaded causal language model.
    - tokenizer (AutoTokenizer): The tokenizer associated with the loaded model.
    - use_cuda (bool): If True, text generation will be performed on a CUDA device.

    Returns:
    - generated_text (str): The generated text.

    Example:
    >>> model, tokenizer = load_causal_lm_model('gpt2', use_cuda=True)
    >>> generated_text = generate_text(model, tokenizer, use_cuda=True)
    """

    inputs = tokenizer('A cat in French is ', return_tensors="pt")["input_ids"].cpu()

    if use_cuda:
        inputs = inputs.cuda()

    outputs = model.generate(inputs, max_new_tokens=3)
    generated_text = tokenizer.decode(outputs[0])
    return generated_text
