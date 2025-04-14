import json
from pathlib import Path
from typing import Any, Dict


def load_config(config_path: Path) -> Dict[str, Any]:
    """Charge un fichier JSON de configuration en tant que dictionnaire Python."""
    if not config_path.exists():
        raise FileNotFoundError(f"Fichier de configuration introuvable : {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

__all__ = ["load_config"]