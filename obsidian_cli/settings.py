from pathlib import Path
import json

ROOT = Path.cwd()
DEFAULT_CONFIG_PATH = ROOT / "config.json"
DEFAULT_VAULT_PATH = ROOT / "vault"
DEFAULT_TEMPLATES_PATH = ROOT / "templates"

class Settings:
    def __init__(self, config_path: Path = DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.config = self.load_config(config_path)

    def load_config(self, path: Path) -> dict:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}

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

# Instance globale à utiliser partout dans le projet
settings = Settings()
