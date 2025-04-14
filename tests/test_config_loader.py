import json
import tempfile
from pathlib import Path

from obsidian_cli.config_loader import load_config


def test_load_config():
    data = {
        "vault_path": "G:/Test/Vault",
        "debug": True
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"
        config_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

        result = load_config(config_path)

        assert isinstance(result, dict)
        assert result["vault_path"] == "G:/Test/Vault"
        assert result["debug"] is True


def test_load_config_missing_file():
    missing_path = Path("nonexistent_config.json")

    try:
        load_config(missing_path)
        assert False, "Une exception FileNotFoundError aurait dû être levée"
    except FileNotFoundError:
        pass
