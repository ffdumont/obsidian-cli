from pathlib import Path
import frontmatter
from typing import Dict, List
import uuid as uuidlib
from obsidian_cli.helpers.naming import generate_key

KEY_PREFIX = {
    "Epic": "EPI",
    "Story": "STO",
    "Task": "TSK",
}

def generate_uuid() -> str:
    return uuidlib.uuid4().hex[:8]

def scan_vault(
    base_path: Path,
    write: bool = False,
    dry_run: bool = False,
    force: bool = False
) -> Dict[str, dict]:
    index = {}
    used_keys = set()
    modifications = []

    for path in sorted(base_path.rglob("*.md")):
        post = frontmatter.load(path)
        metadata = post.metadata
        modified = False
        changes = []

        note_type = metadata.get("type")
        note_uuid = metadata.get("uuid")
        current_key = metadata.get("key")

        if not note_type:
            continue  # Type obligatoire

        if not note_uuid:
            note_uuid = generate_uuid()
            metadata["uuid"] = note_uuid
            changes.append("+ uuid ajouté")
            modified = True

        expected_key = generate_key(note_type, list(used_keys), prefix_map=KEY_PREFIX)
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
        print("💡 Modifications détectées (dry-run) :")
        for filename, changes in modifications:
            print(f"- {filename}")
            for change in changes:
                print(f"  {change}")

    return index
