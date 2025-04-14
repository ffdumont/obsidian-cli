from pathlib import Path
import json
import pytest
from obsidian_cli.scan import scan_vault


def print_index(index: dict):
    print("🗂️ Index complet :")
    for key, entry in index.items():
        print(f"  {key} → {entry['type']} | {entry['title']} ({entry['uuid']})")
        print(f"     ↪︎ {entry['path']}")


def test_scan_single_note(tmp_path_base: Path):
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
    assert "00001" in index

    note = index["00001"]
    assert note["uuid"] == "abc123"
    assert note["type"] == "project"
    assert note["title"] == "Ma Note"
    assert Path(note["path"]).as_posix().endswith("01-Test/001 - Ma Note.md")

    # ✅ Vérification des liens
    assert "links" in note
    assert isinstance(note["links"], list)
    assert note["links"] == []

    # Sauvegarde l’index pour inspection
    index_path = tmp_path_base / "index.json"
    with index_path.open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def test_scan_with_parent_link(tmp_path_base: Path):
    parent_note = tmp_path_base / "01-Projects" / "001 - Mon Projet.md"
    parent_note.parent.mkdir(parents=True)
    parent_note.write_text("""---
uuid: parent123
type: project
title: Mon Projet
---""", encoding="utf-8")

    child_note = tmp_path_base / "02-Tasks" / "002 - Tâche liée.md"
    child_note.parent.mkdir(parents=True)
    child_note.write_text("""---
uuid: child456
type: task
title: Tâche liée
parent: parent123
---""", encoding="utf-8")

    index = scan_vault(tmp_path_base)
    print_index(index)

    assert "00001" in index and "00002" in index

    child = next(v for v in index.values() if v["uuid"] == "child456")
    assert "links" in child
    assert {"type": "parent", "target": "parent123"} in child["links"]

    # Sauvegarde l’index pour inspection
    index_path = tmp_path_base / "index_with_links.json"
    with index_path.open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
