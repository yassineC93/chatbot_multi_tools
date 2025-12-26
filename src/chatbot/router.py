from __future__ import annotations


def parse_llm_tool_request(text: str):
    """
    Format accepté:
      TOOL: date
      TOOL: list_data
    """
    t = text.strip()

    if t == "TOOL: date":
        return "date"

    if t == "TOOL: list_data":
        return "list_data"

    return None

