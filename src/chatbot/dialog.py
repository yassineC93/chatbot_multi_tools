from __future__ import annotations

from src.chatbot.router import parse_tool_command, run_tool


def run_console_chat(tokenizer, model, generate_fn) -> None:
    system = "Tu es un assistant utile et concis."
    history: list[tuple[str, str]] = []

    print("Chatbot local (tape 'exit' pour quitter)\n")
    print("Commande tool: utilise_tool_date\n")

    while True:
        user_msg = input("Vous: ").strip()
        if user_msg.lower() in {"exit", "quit"}:
            break

        tool_name, tool_arg = parse_tool_command(user_msg)

        # si commande tool -> exécuter et répondre direct
        if tool_name is not None:
            tool_out = run_tool(tool_name, tool_arg)
            print(f"Bot: {tool_out}\n")
            # on stocke en historique (utile quand on fera l'orchestration)
            history.append((user_msg, tool_out))
            continue

        # sinon -> LLM normal
        answer = generate_fn(tokenizer, model, system, history, user_msg)
        history.append((user_msg, answer))
        print(f"Bot: {answer}\n")
