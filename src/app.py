from src.chatbot.llm import load_llm, generate_answer
from src.chatbot.dialog import run_console_chat


def main() -> None:
    # Modèle simple pour commencer (qualité OK, VRAM OK)
    model_name = "Qwen/Qwen2.5-1.5B-Instruct"

    tokenizer, model = load_llm(model_name)
    run_console_chat(tokenizer, model, generate_answer)


if __name__ == "__main__":
    main()
