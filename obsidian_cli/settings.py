import os
import json
from pathlib import Path
from typing import Optional

ROOT = Path.cwd()
DEFAULT_LOCAL_CONFIG_PATH = ROOT / "config.json"
DEFAULT_GLOBAL_CONFIG_PATH = Path.home() / ".config" / "obsidian-cli" / "config.json"
DEFAULT_VAULT_PATH = ROOT / "vault"
DEFAULT_TEMPLATES_PATH = ROOT / "templates"

class Settings:
    def __init__(self, config_path: Optional[Path] = None):
        # Résolution du chemin de config
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = self.find_default_config()

        if not self.config_path.exists():
            raise FileNotFoundError(f"❌ Fichier de configuration introuvable : {self.config_path}")

        self.config = self.load_config(self.config_path)

    def find_default_config(self) -> Path:
        """
        Cherche automatiquement la config dans cet ordre :
        - Variable d'environnement OBSIDIAN_CLI_CONFIG
        - ~/.config/obsidian-cli/config.json
        - ./config.json
        """
        env_path = os.getenv("OBSIDIAN_CLI_CONFIG")
        if env_path:
            return Path(env_path)
        if DEFAULT_GLOBAL_CONFIG_PATH.exists():
            return DEFAULT_GLOBAL_CONFIG_PATH
        return DEFAULT_LOCAL_CONFIG_PATH

    def load_config(self, path: Path) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_path(self, key: str, default: Path) -> Path:
        return Path(self.config.get(key, str(default)))

    def get_bool(self, key: str, default: bool = False) -> bool:
        value = self.config.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in ("true", "1", "yes", "on"):
                return True
            if normalized in ("false", "0", "no", "off"):
                return False
            raise ValueError(f"Valeur booléenne invalide pour '{key}' : '{value}'")
        raise TypeError(f"Type non supporté pour '{key}' : {type(value)}")

    @property
    def vault_path(self) -> Path:
        return self.get_path("vault_path", DEFAULT_VAULT_PATH)

    @property
    def templates_path(self) -> Path:
        return self.get_path("templates_path", DEFAULT_TEMPLATES_PATH)

    @property
    def debug(self) -> bool:
        return self.get_bool("debug", False)

    @property
    def strict_paths(self) -> bool:
        return self.get_bool("strict_paths", False)

# Pas d'instance globale ici par défaut, on laisse créer explicitement via Settings(config_path)
