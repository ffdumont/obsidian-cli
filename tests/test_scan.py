from pathlib import Path
import json
import pytest
from obsidian_cli.scan import scan_vault


def print_index(index: dict):
    print("🗂️ Index complet :")
    for key, entry in index.items():
        print(f"  {key} → {entry['type']} | {entry['title']} ({entry['uuid']})")
        print(f"     ↪︎ {entry['path']}")

def test_scan_single_note(tmp_path_base):
    note_path = tmp_path_base / "01-Test" / "001 - Ma Note.md"
    note_path.parent.mkdir(parents=True)
    note_path.write_text("""---
uuid: abc123
type: project
title: Ma Note
--- 

Contenu de la note.
""", encoding="utf-8")

    index = scan_vault(tmp_path_base)

    assert isinstance(index, dict)
    assert "abc123" in index

    note = index["abc123"]
    assert note["type"] == "project"
    assert note["key"].startswith("PRO-")
    assert note["path"] == "01-Test/001 - Ma Note.md"
    assert note["links"] == []

def test_scan_with_parent_link(tmp_path_base):
    # Création de la note parent
    parent_note = tmp_path_base / "01-Projects" / "001 - Mon Projet.md"
    parent_note.parent.mkdir(parents=True)
    parent_note.write_text("""---
uuid: parent123
type: project
title: Mon Projet
---""", encoding="utf-8")

    # Création de la note enfant
    child_note = tmp_path_base / "02-Tasks" / "002 - Tâche liée.md"
    child_note.parent.mkdir(parents=True)
    child_note.write_text("""---
uuid: child456
type: task
title: Tâche liée
parent: parent123
---""", encoding="utf-8")

    # Scan du vault
    index = scan_vault(tmp_path_base)

    # Vérifications
    assert "parent123" in index
    assert "child456" in index

    parent = index["parent123"]
    child = index["child456"]

    assert parent["type"] == "project"
    assert child["type"] == "task"
    assert child["links"] == [{"type": "parent", "target": "parent123"}]
    assert parent["links"] == []
