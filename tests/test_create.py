import json
from pathlib import Path
import pytest
from obsidian_cli.settings import Settings
from obsidian_cli.ontology import Ontology
from obsidian_cli.commands.create import create_note

def test_create_note(tmp_path_base: Path):
    # Simulation de la config
    config_data = {
        "vault_path": str(tmp_path_base / "vault"),
        "templates_path": str(tmp_path_base / "templates"),
        "structure": ["area", "project", "task"],
        "relationships": {
            "parent": {
                "task": ["project"],
                "project": ["area"]
            },
            "sibling": {
                "url": ["task"],
                "idea": ["project", "task"]
            }
        },
        "namingPattern": {
            "project": "{classifier}-{date} {name}"
        },
        "dateFormat": "%y%m",
        "classificationPath": str(tmp_path_base / "classification.txt"),
        "debug": True
    }

    # Écrit la config
    config_path = tmp_path_base / "config.json"
    config_path.write_text(json.dumps(config_data, indent=2), encoding="utf-8")

    # Écrit un fichier de classifieurs
    classifier_file = tmp_path_base / "classification.txt"
    classifier_file.write_text("1000\tAdministration & Maison\n", encoding="utf-8")

    # Crée un template pour project
    template_dir = tmp_path_base / "templates"
    template_dir.mkdir(parents=True, exist_ok=True)
    (template_dir / "project.md").write_text("# Modèle de projet\n", encoding="utf-8")

    # Initialise les objets
    settings = Settings(config_path=config_path)
    ontology = Ontology(config_data["relationships"])

    # Appel de la fonction à tester
    note_path = create_note(
        note_type="project",
        title="Planification avril",
        classifier_code="1000",
        parent_uuid=None,
        settings=settings,
        ontology=ontology
    )

    # ✅ Assertions
    assert note_path.exists()
    assert note_path.name.startswith("1000-")
    assert "Planification avril" in note_path.name
    assert note_path.suffix == ".md"

    content = note_path.read_text(encoding="utf-8")
    assert "type: project" in content
    assert "title: Planification avril" in content
    assert "classifier: '1000'" in content
