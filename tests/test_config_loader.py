from pathlib import Path
from obsidian_cli.config_loader import load_config

def test_load_home_config():
    config = load_config(Path("configs/home_config.json"))
    assert config["structure"] == ["area", "project", "task"]
    assert "parent" in config["relationships"]
    assert config["relationships"]["parent"]["project"] == ["area"]
