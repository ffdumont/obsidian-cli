import pytest
from obsidian_cli.helpers.naming import generate_key

def test_generate_key_starts_at_001():
    key = generate_key("Task", [], prefix_map={"Task": "TSK"})
    assert key == "TSK-001"

def test_generate_key_increments():
    existing = ["TSK-001", "TSK-002"]
    key = generate_key("Task", existing, prefix_map={"Task": "TSK"})
    assert key == "TSK-003"


def test_generate_key_uses_custom_prefix():
    prefix_map = {"Story": "STO"}
    key = generate_key("Story", ["STO-001", "STO-002"], prefix_map)
    assert key == "STO-003"

def test_generate_key_defaults_to_upper():
    key = generate_key("Note", ["NOT-001"])
    assert key == "NOT-002"
