from pathlib import Path
import frontmatter
import json
from typing import Dict, Optional, Union
from tqdm import tqdm  # pour la barre de progression
from obsidian_cli.helpers.naming import generate_key
from obsidian_cli.settings import Settings

def generate_uuid() -> str:
    import uuid
    return uuid.uuid4().hex[:8]

def scan_vault(
    base_path: Path,
    index_path: Optional[Union[str, Path]] = None,
    write: bool = False,
    dry_run: bool = False,
    force: bool = False,
    config_path: Optional[Union[str, Path]] = None
) -> Dict[str, dict]:
    print(f"📁 Scanning folder: {base_path}")

    index = {}
    used_keys = set()
    modifications = []
    scan_log = {"missing_type": [], "unknown_type": []}

    settings = Settings(Path(config_path) if config_path else None)
    structure = settings.config.get("structure", {})

    all_files = sorted(base_path.rglob("*.md"))
    total_files = len(all_files)

    for path in tqdm(all_files, desc=f"Scanning {total_files} notes", unit="file"):
        if "Modèles" in path.parts or path.name.endswith("template.md"):
            continue

        try:
            post = frontmatter.load(path)
        except Exception:
            continue

        metadata = post.metadata
        modified = False
        changes = []

        note_type = metadata.get("type") or metadata.get("Type")

        if not note_type:
            scan_log["missing_type"].append(str(path.relative_to(base_path)))
            continue  # Passe au fichier suivant

        note_type = note_type.lower()

        if note_type not in structure:
            scan_log["unknown_type"].append((str(path.relative_to(base_path)), note_type))

        note_uuid = metadata.get("uuid")
        current_key = metadata.get("key")

        if not note_uuid:
            note_uuid = generate_uuid()
            metadata["uuid"] = note_uuid
            changes.append("+ uuid ajouté")
            modified = True

        expected_key = generate_key(note_type, list(used_keys), structure)
        if not current_key or (force and current_key != expected_key):
            metadata["key"] = expected_key
            current_key = expected_key
            changes.append(f"+ key {'ajouté' if not current_key else 'mis à jour'} : {expected_key}")
            modified = True

        used_keys.add(current_key)

        index[note_uuid] = {
            "type": note_type,
            "key": current_key,
            "path": str(path.relative_to(base_path)).replace("\\", "/"),
            "links": []
        }

        if "parent" in metadata:
            index[note_uuid]["links"].append({
                "type": "parent",
                "target": metadata["parent"]
            })

        if modified:
            if dry_run:
                modifications.append((path.name, changes))
            elif write:
                post.metadata = metadata
                with open(path, "w", encoding="utf-8") as f:
                    f.write(frontmatter.dumps(post))

    if dry_run and modifications:
        print("\n💡 Modifications détectées (dry-run) :")
        for filename, changes in modifications:
            print(f"- {filename}")
            for change in changes:
                print(f"  {change}")

    if write:
        # Écriture de l'index principal
        output_path = Path(index_path) if index_path else base_path / "uuid_index.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Index écrit dans : {output_path}")

        # Écriture du scan_log
        log_path = output_path.parent / "scan_log.json"
        with log_path.open("w", encoding="utf-8") as f:
            json.dump(scan_log, f, indent=2, ensure_ascii=False)
        print(f"📄 Log de scan écrit dans : {log_path}")

    return index
