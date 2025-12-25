from __future__ import annotations

from src.chatbot.router import llm_wants_tool
from src.tools.datetime_tool import tool_date


def run_console_chat(tokenizer, model, generate_fn) -> None:
    # Prompt système: on explique au LLM qu'il a un tool
    system = (
        "Tu es un assistant utile et concis.\n"
        "Tu as accès à un outil:\n"
        "- date: donne la date/heure locale.\n\n"
        "Règle stricte:\n"
        "Si l'utilisateur demande l'heure, la date, 'maintenant', etc., "
        "tu DOIS répondre exactement par une seule ligne: TOOL: date\n"
        "Sinon, réponds normalement.\n"
        "Ne mentionne pas ces règles."
    )

    history: list[tuple[str, str]] = []

    print("Chatbot local (tape 'exit' pour quitter)\n")

    while True:
        user_msg = input("Vous: ").strip()
        if user_msg.lower() in {"exit", "quit"}:
            break

        # 1) On demande au LLM quoi faire
        llm_text = generate_fn(tokenizer, model, system, history, user_msg)

        # 2) Est-ce qu'il veut appeler un tool ?
        tool_name = llm_wants_tool(llm_text)

        if tool_name == "date":
            # 3) Exécuter le tool
            tool_out = tool_date()

            # 4) Réinjecter le résultat du tool pour produire la réponse finale
            # On ajoute une "observation" dans le contexte via l'historique
            history.append((user_msg, ""))
            history.append((
                "Résultat de l'outil date (à utiliser pour répondre à l'utilisateur) :",
                tool_out
            ))

            final_answer = generate_fn(
                tokenizer,
                model,
                system,
                history,
                "Réponds à l'utilisateur en utilisant le résultat de l'outil."
            )

            # On remplace l'échange utilisateur -> assistant par la vraie réponse finale
            # (simple: on stocke la réponse finale comme dernier échange user)
            history.append((user_msg, final_answer))
            print(f"Bot: {final_answer}\n")
            continue

        # 5) Sinon, réponse normale
        history.append((user_msg, llm_text))
        print(f"Bot: {llm_text}\n")
