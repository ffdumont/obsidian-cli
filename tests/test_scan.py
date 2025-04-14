import json
import shutil
from pathlib import Path
import pytest
# from obsidian_cli.commands.scan import scan_vault
# from obsidian_cli.commands.scan import print_index  # Si cette fonction existe



def print_index(index: dict):
    print("🗂️ Index complet :")
    for key, entry in index.items():
        print(f"  {key} → {entry['type']} | {entry['title']} ({entry['uuid']})")
        print(f"     ↪︎ {entry['path']}")


def test_scan_single_note(tmp_path: Path):
    note_path = tmp_path / "01-Test" / "001 - Ma Note.md"
    note_path.parent.mkdir(parents=True)
    note_path.write_text("""---
uuid: abc123
type: project
title: Ma Note
---

Contenu de la note.
""", encoding="utf-8")

    index = scan_vault(tmp_path)

    assert isinstance(index, dict)
    assert "00001" in index

    note = index["00001"]
    assert note["uuid"] == "abc123"
    assert note["type"] == "project"
    assert note["title"] == "Ma Note"
    assert note["path"].endswith("01-Test/001 - Ma Note.md")


# @pytest.mark.skip(reason="Test manuel pour explorer l’indexation et les fichiers générés")
import pytest
from pathlib import Path
import tempfile
import json
from obsidian_cli.scan import scan_vault


def print_index(index: dict):
    print("🗂️ Index complet :")
    for key, entry in index.items():
        print(f"  {key} → {entry['type']} | {entry['title']} ({entry['uuid']})")
        print(f"     ↪︎ {entry['path']}")


# @pytest.mark.skip(reason="Test manuel pour explorer l’indexation et les fichiers générés")
import pytest
from pathlib import Path
import tempfile
import json
from obsidian_cli.scan import scan_vault


def print_index(index: dict):
    print("🗂️ Index complet :")
    for key, entry in index.items():
        print(f"  {key} → {entry['type']} | {entry['title']} ({entry['uuid']})")
        print(f"     ↪︎ {entry['path']}")


# @pytest.mark.skip(reason="Test manuel pour explorer l’indexation et les fichiers générés")
def test_debug_scan():
    tmpdir = tempfile.TemporaryDirectory()
    tmp_path = Path(tmpdir.name)

    note_path = tmp_path / "00-Debug" / "001 - Note de test.md"
    note_path.parent.mkdir(parents=True)
    note_path.write_text("""---
uuid: debug123
type: task
title: Note de debug
---

Contenu test
""", encoding="utf-8")

    print("📂 Dossier temporaire :", tmp_path)
    print("📄 Contenu du fichier :", note_path.read_text(encoding="utf-8"))

    index = scan_vault(tmp_path)

    # Affichage formaté
    print_index(index)

    # Affichage JSON brut
    print("\n📝 Index JSON (brut) :")
    print(json.dumps(index, indent=2, ensure_ascii=False))

    # Sauvegarde temporaire pour inspection (sera supprimée ensuite)
    index_file = tmp_path / "index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print("✅ Fin du test. Le répertoire temporaire va être supprimé.")
    tmpdir.cleanup()

# @pytest.mark.skip(reason="Test manuel : génère un index dans un dossier persistant pour inspection")
def test_debug_scan_inspectable():
    # Utilise un chemin fixe sur ton disque
    tmp_path = Path("C:/Temp/debug-scan")
    if tmp_path.exists():
        shutil.rmtree(tmp_path)
    tmp_path.mkdir(parents=True)

    note_path = tmp_path / "00-Debug" / "001 - Note de test.md"
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text("""---
uuid: debug-inspect
type: project
title: Inspection manuelle
---

Ceci est un test manuel de scan.
""", encoding="utf-8")

    print("📂 Dossier de test manuel :", tmp_path)
    print("📄 Contenu de la note :", note_path.read_text(encoding="utf-8"))

    index = scan_vault(tmp_path)
    print_index(index)

    print("\n📝 Index JSON :")
    print(json.dumps(index, indent=2, ensure_ascii=False))

    index_file = tmp_path / "index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Index sauvegardé dans : {index_file}")
    print("🕵️ Tu peux maintenant ouvrir ce dossier dans VSCode ou l’explorateur.")
