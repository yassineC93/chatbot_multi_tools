from __future__ import annotations
from datetime import datetime


def tool_date() -> str:
    now = datetime.now()
    return "Date/heure locale: " + now.strftime("%Y-%m-%d %H:%M:%S")
