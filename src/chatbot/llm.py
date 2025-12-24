from __future__ import annotations

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def load_llm(model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

    dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
    )

    return tokenizer, model


def build_messages(system: str, history: list[tuple[str, str]], user_msg: str):
    """
    Transforme (system + history + user_msg) en liste de messages chat.
    """
    messages = [{"role": "system", "content": system}]
    for u, a in history:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": user_msg})
    return messages


def generate_answer(
    tokenizer,
    model,
    system: str,
    history: list[tuple[str, str]],
    user_msg: str,
    max_new_tokens: int = 256,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> str:
    """
    Génère uniquement la réponse de l'assistant, propre, sans répétitions.
    """
    messages = build_messages(system, history, user_msg)

    # Utilise le chat template du modèle (Qwen Instruct)
    prompt_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt",
    ).to(model.device)

    with torch.inference_mode():
        out_ids = model.generate(
            prompt_ids,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
        )

    # IMPORTANT: ne décoder que la partie nouvellement générée
    new_ids = out_ids[0][prompt_ids.shape[-1]:]
    answer = tokenizer.decode(new_ids, skip_special_tokens=True).strip()

    return answer
