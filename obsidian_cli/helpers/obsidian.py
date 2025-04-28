from pathlib import Path
import json
from datetime import datetime

def find_daily_notes_folder(vault_path: Path) -> Path:
    """
    Trouve le dossier daily notes configuré dans Obsidian.
    Utilise seulement le chemin jusqu'à YY-MM/YY-MM-DD, sans dupliquer pour le fichier.
    """

    daily_notes_config = vault_path / ".obsidian" / "daily-notes.json"

    if not daily_notes_config.is_file():
        raise FileNotFoundError(f"Fichier de configuration daily-notes.json introuvable à {daily_notes_config}")

    with daily_notes_config.open(encoding="utf-8") as f:
        config = json.load(f)

    daily_folder = config.get("folder")
    daily_format = config.get("format")

    if not daily_folder or not daily_format:
        raise ValueError("La configuration daily-notes.json doit contenir les clés 'folder' et 'format'.")

    strftime_format = convert_moment_to_strftime(daily_format)

    today = datetime.now()

    # Attention ici : si format contient plusieurs niveaux, on prend tout sauf le dernier pour le dossier
    format_parts = strftime_format.split('/')
    if len(format_parts) >= 2:
        folder_format = '/'.join(format_parts[:-1])  # tout sauf la dernière partie
    else:
        folder_format = strftime_format

    folder_subpath = today.strftime(folder_format)

    return vault_path / daily_folder / folder_subpath

def convert_moment_to_strftime(moment_format: str) -> str:
    """Convertit un format Moment.js vers un format Python strftime."""
    return (moment_format
        .replace("YYYY", "%Y")
        .replace("YY", "%y")
        .replace("MM", "%m")
        .replace("DD", "%d")
    )
