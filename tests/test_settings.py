import json
import tempfile
import pytest
from pathlib import Path
from obsidian_cli.settings import Settings, settings, DEFAULT_VAULT_PATH, DEFAULT_TEMPLATES_PATH, DEFAULT_CONFIG_PATH

# ───────────────────────────────────────────────
# 🧪 SECTION 1 : Chargement d’un fichier de config
# ───────────────────────────────────────────────

def test_settings_loading():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"
        config_data = {
            "vault_path": "G:/Test/Vault",
            "templates_path": "G:/Test/Templates",
            "debug": True
        }

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f)

        custom_settings = Settings(config_path=config_path)

        assert custom_settings.vault_path == Path("G:/Test/Vault")
        assert custom_settings.templates_path == Path("G:/Test/Templates")
        assert custom_settings.debug is True

# ───────────────────────────────────────────────
# 🧪 SECTION 2 : Valeurs par défaut si config absente
# ───────────────────────────────────────────────

def test_settings_default_when_config_missing():
    fake_path = Path("nonexistent_config.json")
    custom_settings = Settings(config_path=fake_path)

    assert custom_settings.vault_path == DEFAULT_VAULT_PATH
    assert custom_settings.templates_path == DEFAULT_TEMPLATES_PATH
    assert custom_settings.debug is False

# ───────────────────────────────────────────────
# 🧪 SECTION 3 : Vérification d’existence physique des chemins
# ───────────────────────────────────────────────

@pytest.mark.parametrize("path_attr", ["vault_path", "templates_path"])
def test_configured_paths_exist(tmp_path, monkeypatch, path_attr):
    """Vérifie que les chemins configurés existent physiquement (mockés)"""

    fake_path = tmp_path / path_attr
    fake_path.mkdir()

    # Monkeypatch la méthode get_path pour qu’elle retourne notre fake_path
    def fake_get_path(key: str, default: Path) -> Path:
        return fake_path

    monkeypatch.setattr(settings, "get_path", fake_get_path)

    # Test réel
    path = getattr(settings, path_attr)
    assert path.exists()



@pytest.mark.parametrize(
    "input_value,expected",
    [
        (True, True),
        ("true", True),
        ("1", True),
        ("yes", True),
        ("on", True),
        (False, False),
        ("false", False),
        ("0", False),
        ("no", False),
        ("off", False)
    ]
)
def test_get_bool_valid_values(input_value, expected):
    s = Settings(config_path=DEFAULT_CONFIG_PATH)
    s.config = {"flag": input_value}
    assert s.get_bool("flag") == expected

@pytest.mark.parametrize("invalid_value", [
    "peut-être",
    "certainement",
    "",
    None,
    [],
    2,
    0.5,
])
def test_get_bool_invalid_values(invalid_value):
    s = Settings(config_path=DEFAULT_CONFIG_PATH)
    s.config = {"flag": invalid_value}

    with pytest.raises((ValueError, TypeError)):
        s.get_bool("flag")

def test_strict_paths_behavior():
    # Test avec strict_paths = true
    s = Settings(config_path=DEFAULT_CONFIG_PATH)
    s.config = {"strict_paths": "yes"}
    assert s.strict_paths is True

    # Test avec strict_paths = false
    s.config = {"strict_paths": "no"}
    assert s.strict_paths is False

    # Test avec valeur absente (fallback)
    s.config = {}
    assert s.strict_paths is False

def test_strict_paths_invalid_value():
    s = Settings(config_path=DEFAULT_CONFIG_PATH)
    s.config = {"strict_paths": "peut-être"}

    with pytest.raises(ValueError):
        _ = s.strict_paths
