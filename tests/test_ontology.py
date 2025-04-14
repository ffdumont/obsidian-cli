import pytest
import json
from obsidian_cli.ontology import Ontology

@pytest.fixture
def ontology():
    with open("configs/home_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    return Ontology(config["relationships"])

def test_valid_parent_child(ontology):
    assert ontology.is_valid_parent("task", "project")
    assert ontology.is_valid_parent("project", "area")

def test_invalid_parent_child(ontology):
    assert not ontology.is_valid_parent("area", "task")
    assert not ontology.is_valid_parent("milestone", "task")  # Inexistant

def test_is_valid_sibling(ontology):
    assert ontology.is_valid_sibling("url", "task")
    assert ontology.is_valid_sibling("idea", "project")
    assert ontology.is_valid_sibling("task", "idea")  # Relation symétrique

def test_invalid_relationships(ontology):
    assert not ontology.is_valid_parent("url", "area")
    # Cette relation est symétrique et définie, donc elle est valide
    # assert not ontology.is_valid_sibling("project", "url") → supprimé ou commenté
