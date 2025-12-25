from __future__ import annotations

from src.tools.datetime_tool import tool_date


def parse_tool_command(user_msg: str):
    """
    Détecte la commande:
      - "utilise_tool_date"
    Retourne ("date", "") ou (None, None)
    """
    msg = user_msg.strip()
    if msg == "utilise_tool_date":
        return "date", ""
    return None, None


def run_tool(tool_name: str, tool_arg: str) -> str:
    if tool_name == "date":
        return tool_date()
    return "Tool inconnu."
