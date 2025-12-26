from __future__ import annotations

from src.chatbot.router import parse_llm_tool_request
from src.tools.datetime_tool import tool_date
from src.tools.list_data_tool import tool_list_data


def run_console_chat(tokenizer, model, generate_fn) -> None:
    system = (
        "Tu es un assistant utile et concis.\n\n"
        "Tu as accès à des outils:\n"
        "- date: donne la date/heure locale.\n"
        "- list_data: liste les fichiers du dossier data/.\n\n"
        "RÈGLES STRICTES (OBLIGATOIRES):\n"
        "- Tu N'AS PAS LE DROIT de donner l'heure sans utiliser l'outil date.\n"
        "- Tu N'AS PAS LE DROIT de décrire le contenu du dossier data sans utiliser l'outil list_data.\n\n"
        "FORMAT DE DEMANDE D'OUTIL (tu dois respecter EXACTEMENT):\n"
        "- TOOL: date\n"
        "- TOOL: list_data\n"
        "Si tu as besoin des deux, écris deux lignes:\n"
        "TOOL: date\n"
        "TOOL: list_data\n\n"
        "Si aucun outil n'est nécessaire, réponds normalement.\n"
        "Ne réponds JAMAIS avec des informations inventées."
    )

    history: list[tuple[str, str]] = []

    print("Chatbot local (tape 'exit' pour quitter)\n")

    while True:
        user_msg = input("Vous: ").strip()
        if user_msg.lower() in {"exit", "quit"}:
            break

        # 1) Le LLM décide : réponse normale OU demande d'outil(s)
        llm_text = generate_fn(tokenizer, model, system, history, user_msg)

        tools = parse_llm_tool_request(llm_text)  # <-- liste: ["date"], ["list_data"], ["date","list_data"], ou []

        # 2) Si aucun tool n'est demandé => réponse normale
        if not tools:
            history.append((user_msg, llm_text))
            print(f"Bot: {llm_text}\n")
            continue

        # 3) Exécuter les tools demandés
        results = []
        if "date" in tools:
            results.append(tool_date())
        if "list_data" in tools:
            results.append(tool_list_data())

        tool_out = "\n".join(results).strip()

        # 4) Réinjecter le résultat tool dans l'historique
        history.append((user_msg, ""))
        history.append(("Résultat des outils :", tool_out))

        # 5) Demander au LLM la réponse finale (basée sur tool_out)
        final_answer = generate_fn(
            tokenizer,
            model,
            system,
            history,
            "Réponds à l'utilisateur en utilisant STRICTEMENT les résultats des outils."
        )

        # 6) Petit garde-fou: si le LLM redemande un tool au lieu de répondre, on affiche le brut
        # (ça évite les boucles infinies au début)
        if parse_llm_tool_request(final_answer):
            final_answer = tool_out

        history.append((user_msg, final_answer))
        print(f"Bot: {final_answer}\n")
