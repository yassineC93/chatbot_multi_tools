from __future__ import annotations


def llm_wants_tool(text: str):
    """
    Si le LLM renvoie 'TOOL: date', on déclenche le tool.
    Retourne tool_name ou None.
    """
    t = text.strip()
    if t == "TOOL: date":
        return "date"
    return None
