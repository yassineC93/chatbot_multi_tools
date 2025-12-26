from __future__ import annotations


def parse_llm_tool_request(text: str):
    tools = []
    for line in text.splitlines():
        line = line.strip()
        if line == "TOOL: date":
            tools.append("date")
        if line == "TOOL: list_data":
            tools.append("list_data")
    return tools

