from pathlib import Path
import os
from obsidian_cli.settings import Settings

def find_default_config() -> Path:
    """Trouve le fichier de configuration par défaut."""

    # 1. Variable d'environnement OBSIDIAN_CLI_CONFIG
    env_path = os.getenv("OBSIDIAN_CLI_CONFIG")
    if env_path:
        config = Path(env_path)
        if config.is_file():
            return config
        else:
            raise FileNotFoundError(f"Chemin défini dans OBSIDIAN_CLI_CONFIG introuvable : {env_path}")

    # 2. XDG standard (~/.config/obsidian-cli/config.json)
    xdg_config_home = os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")
    config_path = Path(xdg_config_home) / "obsidian-cli" / "config.json"
    if config_path.is_file():
        return config_path

    raise FileNotFoundError("Aucune configuration obsidian-cli trouvée (ni via OBSIDIAN_CLI_CONFIG ni via ~/.config/obsidian-cli/config.json).")

def load_settings(config_path: str = None) -> Settings:
    """Charge Settings à partir d'un chemin ou de la logique par défaut."""

    if config_path:
        config = Path(config_path)
        if not config.is_file():
            raise FileNotFoundError(f"Fichier de configuration spécifié non trouvé : {config}")
        return Settings(config)

    return Settings(find_default_config())
