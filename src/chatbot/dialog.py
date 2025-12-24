from __future__ import annotations


def run_console_chat(tokenizer, model, generate_fn) -> None:
    system = "Tu es un assistant utile et concis."
    history: list[tuple[str, str]] = []

    print("Chatbot local (tape 'exit' pour quitter)\n")
    while True:
        user_msg = input("Vous: ").strip()
        if user_msg.lower() in {"exit", "quit"}:
            break

        answer = generate_fn(tokenizer, model, system, history, user_msg)
        history.append((user_msg, answer))
        print(f"Bot: {answer}\n")
