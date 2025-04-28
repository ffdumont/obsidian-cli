# obsidian_cli/helpers/key_prefixes.py

from obsidian_cli.settings import Settings
from typing import Dict

def load_key_prefixes() -> Dict[str, str]:
    """
    Charge les préfixes de clefs pour chaque type de note depuis la configuration.
    """
    settings = Settings()
    return settings.config.get("keyPrefixes", {})
