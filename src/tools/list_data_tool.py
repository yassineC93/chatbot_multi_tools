from __future__ import annotations

from pathlib import Path


def tool_list_data() -> str:
    """
    Liste simplement le contenu du dossier data/
    """
    data_dir = Path("data")

    if not data_dir.exists():
        return "Le dossier 'data/' n'existe pas."

    if not data_dir.is_dir():
        return "'data/' n'est pas un dossier."

    items = list(data_dir.iterdir())

    if not items:
        return "Le dossier 'data/' est vide."

    lines = ["Contenu du dossier data/:"]
    for p in items:
        if p.is_dir():
            lines.append(f"- DIR  {p.name}")
        else:
            lines.append(f"- FILE {p.name}")

    return "\n".join(lines)
